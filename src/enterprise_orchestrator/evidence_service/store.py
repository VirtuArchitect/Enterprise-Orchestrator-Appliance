from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
import hashlib
import hmac
import json
from pathlib import Path
import secrets
import math
from typing import Any

from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir


class EvidenceStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or ensure_state_dir() / "evidence.json"

    def add(
        self,
        tenant: str,
        source: str,
        summary: str,
        content: str,
        classification: str = "operator_provided",
    ) -> dict[str, Any]:
        records = self.list()
        record = {
            "evidence_id": new_id("evd"),
            "tenant": tenant,
            "source": source,
            "summary": summary,
            "classification": classification,
            "content": content,
            "content_sha256": _sha256_text(content),
            "created_at": datetime.now(UTC).isoformat(),
        }
        record["signature"] = _sign_record(record)
        records.append(record)
        write_json(self.path, records)
        return record

    def list(self, tenant: str | None = None) -> list[dict[str, Any]]:
        records = read_json(self.path, [])
        if tenant is None:
            return records
        return [record for record in records if record.get("tenant") == tenant]

    def get_many(self, evidence_ids: list[str], tenant: str) -> list[dict[str, Any]]:
        wanted = set(evidence_ids)
        return [
            record
            for record in self.list(tenant=tenant)
            if record.get("evidence_id") in wanted
        ]

    def search(self, tenant: str, query: str, limit: int = 10) -> list[dict[str, Any]]:
        terms = [term for term in query.lower().split() if term]
        if not terms:
            return self.list(tenant=tenant)[:limit]
        scored: list[tuple[int, dict[str, Any]]] = []
        for record in self.list(tenant=tenant):
            haystack = " ".join(
                [
                    record.get("source", ""),
                    record.get("summary", ""),
                    record.get("classification", ""),
                    record.get("content", ""),
                ]
            ).lower()
            score = sum(haystack.count(term) for term in terms)
            if score:
                scored.append((score, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:limit]]

    def semantic_search(
        self, tenant: str, query: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        query_vector = _text_vector(query)
        if not query_vector:
            return self.list(tenant=tenant)[:limit]
        scored: list[tuple[float, dict[str, Any]]] = []
        for record in self.list(tenant=tenant):
            text = " ".join(
                [
                    record.get("source", ""),
                    record.get("summary", ""),
                    record.get("classification", ""),
                    record.get("content", ""),
                ]
            )
            score = _cosine_similarity(query_vector, _text_vector(text))
            if score > 0:
                enriched = dict(record)
                enriched["similarity"] = round(score, 4)
                scored.append((score, enriched))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:limit]]

    def verify(self, record: dict[str, Any]) -> bool:
        signature = record.get("signature", "")
        content_hash = record.get("content_sha256", "")
        if not signature or content_hash != _sha256_text(record.get("content", "")):
            return False
        return hmac.compare_digest(signature, _sign_record(record))

    def verify_all(self, tenant: str | None = None) -> dict[str, Any]:
        records = self.list(tenant=tenant)
        invalid = [
            record.get("evidence_id", "unknown")
            for record in records
            if not self.verify(record)
        ]
        return {
            "records": len(records),
            "valid": not invalid,
            "invalid_evidence_ids": invalid,
        }


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sign_record(record: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key not in {"signature", "similarity"}
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hmac.new(_signing_key(), canonical.encode("utf-8"), hashlib.sha256).hexdigest()


def _signing_key() -> bytes:
    path = ensure_state_dir() / "evidence-signing.key"
    if not path.exists():
        path.write_text(secrets.token_hex(32), encoding="utf-8")
    return path.read_text(encoding="utf-8").strip().encode("utf-8")


def _text_vector(value: str) -> Counter[str]:
    terms = [
        term
        for term in "".join(
            character.lower() if character.isalnum() else " "
            for character in value
        ).split()
        if len(term) > 2
    ]
    return Counter(terms)


def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    shared = set(left) & set(right)
    numerator = sum(left[term] * right[term] for term in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)
