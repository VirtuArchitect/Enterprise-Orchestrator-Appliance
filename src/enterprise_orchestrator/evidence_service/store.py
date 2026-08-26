from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
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
            "created_at": datetime.now(UTC).isoformat(),
        }
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
