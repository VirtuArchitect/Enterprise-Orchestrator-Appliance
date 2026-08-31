from __future__ import annotations

import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from enterprise_orchestrator.appliance_api import appliance_status
from enterprise_orchestrator.appliance_api.operations import create_backup, list_updates, stage_update
from enterprise_orchestrator.appliance_api.settings import admin_settings
from enterprise_orchestrator.approval_workflow import ApprovalQueue
from enterprise_orchestrator.audit_service import AuditStore
from enterprise_orchestrator.conversation_service import ConversationStore
from enterprise_orchestrator.eaap_integration import ControlPlaneClient
from enterprise_orchestrator.evidence_service.attachments import EvidenceAttachmentStore
from enterprise_orchestrator.evidence_service import EvidenceStore
from enterprise_orchestrator.execution_gateway.connectors import ReadOnlyDiagnosticConnector
from enterprise_orchestrator.execution_gateway import DryRunExecutionGateway
from enterprise_orchestrator.ids import new_id
from enterprise_orchestrator.identity_service import IdentityService
from enterprise_orchestrator.llm_adapter import OllamaClient
from enterprise_orchestrator.orchestrator_api.history import list_requests
from enterprise_orchestrator.orchestrator_api.models import OrchestrationRequest, RiskTier
from enterprise_orchestrator.orchestrator_api.service import generate_and_submit_plan


ROOT = Path(__file__).resolve().parents[2]
UI_DIR = ROOT / "ui"


class EnterpriseOrchestratorHandler(BaseHTTPRequestHandler):
    server_version = "EnterpriseOrchestrator/0.4"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._json(appliance_status(ROOT))
            return
        if parsed.path == "/api/evidence":
            tenant = parse_qs(parsed.query).get("tenant", [None])[0]
            self._json({"evidence": EvidenceStore().list(tenant=tenant)})
            return
        if parsed.path == "/api/evidence/attachments":
            query = parse_qs(parsed.query)
            actor = query.get("operator", ["operator@example.local"])[0]
            tenant = query.get("tenant", ["default"])[0]
            IdentityService().require(actor, "evidence_attachment:read", tenant)
            self._json({"attachments": EvidenceAttachmentStore().list(tenant=tenant)})
            return
        if parsed.path == "/api/evidence/search":
            query = parse_qs(parsed.query).get("q", [""])[0]
            tenant = parse_qs(parsed.query).get("tenant", ["default"])[0]
            self._json({"evidence": EvidenceStore().search(tenant=tenant, query=query)})
            return
        if parsed.path == "/api/evidence/semantic-search":
            query = parse_qs(parsed.query).get("q", [""])[0]
            tenant = parse_qs(parsed.query).get("tenant", ["default"])[0]
            self._json({"evidence": EvidenceStore().semantic_search(tenant=tenant, query=query)})
            return
        if parsed.path == "/api/evidence/verify":
            tenant = parse_qs(parsed.query).get("tenant", [None])[0]
            self._json(EvidenceStore().verify_all(tenant=tenant))
            return
        if parsed.path == "/api/requests":
            tenant = parse_qs(parsed.query).get("tenant", [None])[0]
            self._json({"requests": list_requests(tenant=tenant)})
            return
        if parsed.path == "/api/conversations":
            query = parse_qs(parsed.query)
            tenant = query.get("tenant", ["default"])[0]
            operator = query.get("operator", [None])[0]
            actor = operator or "operator@example.local"
            IdentityService().require(actor, "conversation:read", tenant)
            self._json(
                {"conversations": ConversationStore().list(tenant=tenant, operator=operator)}
            )
            return
        if parsed.path == "/api/approvals":
            tenant = parse_qs(parsed.query).get("tenant", [None])[0]
            self._json({"approvals": ApprovalQueue().list(tenant=tenant)})
            return
        if parsed.path == "/api/model/health":
            self._json(OllamaClient().health())
            return
        if parsed.path == "/api/connectors":
            self._json(ReadOnlyDiagnosticConnector().capabilities())
            return
        if parsed.path == "/api/integrations/eaap":
            self._json(ControlPlaneClient().status())
            return
        if parsed.path == "/api/integrations/eaap/validation-plan":
            self._json(ControlPlaneClient().validation_plan())
            return
        if parsed.path == "/api/identity/status":
            from enterprise_orchestrator.identity_service.adapters import identity_adapter_status

            self._json(identity_adapter_status())
            return
        if parsed.path == "/api/admin/settings":
            query = parse_qs(parsed.query)
            actor = query.get("operator", ["operator@example.local"])[0]
            tenant = query.get("tenant", ["default"])[0]
            IdentityService().require(actor, "settings:read", tenant)
            self._json(admin_settings(ROOT))
            return
        if parsed.path == "/api/prompt-policy":
            prompt = _prompt_text()
            self._json(
                {
                    "status": "production-oriented policy pack",
                    "path": "prompts/enterprise-orchestrator-v5.6.md",
                    "sha256": _sha256(prompt),
                    "required_clauses": [
                        "Evidence first",
                        "Contract first",
                        "Governance first",
                        "Fail closed",
                        "No invention",
                        "No secrets",
                        "No direct mutation",
                    ],
                }
            )
            return
        if parsed.path == "/api/release/status":
            self._json(
                {
                    "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
                    "demo_url": _optional_file("DEMO_URL"),
                    "demo_status": _optional_file("DEMO_STATUS"),
                    "publication": "public",
                    "fastapi_runtime": "optional",
                    "appliance_image": "planned_not_validated",
                }
            )
            return
        if parsed.path == "/api/updates":
            self._json({"updates": list_updates()})
            return
        if parsed.path == "/api/audit":
            tenant = parse_qs(parsed.query).get("tenant", [None])[0]
            audit = AuditStore()
            self._json({"chain_valid": audit.verify_chain(), "events": audit.list(tenant=tenant)})
            return
        self._serve_static(parsed.path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
            if parsed.path == "/api/evidence":
                self._create_evidence(payload)
                return
            if parsed.path == "/api/evidence/attachments":
                self._create_evidence_attachment(payload)
                return
            if parsed.path == "/api/requests":
                self._create_request(payload)
                return
            if parsed.path == "/api/conversations":
                self._create_conversation(payload)
                return
            if parsed.path == "/api/conversations/messages":
                self._append_conversation_message(payload)
                return
            if parsed.path == "/api/approvals/decide":
                self._decide_approval(payload)
                return
            if parsed.path == "/api/execute/dry-run":
                self._execute_dry_run(payload)
                return
            if parsed.path == "/api/connectors/read-only-plan":
                self._connector_plan(payload)
                return
            if parsed.path == "/api/backup":
                self._create_backup(payload)
                return
            if parsed.path == "/api/updates/stage":
                self._stage_update(payload)
                return
            self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
        except Exception as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _create_evidence(self, payload: dict[str, Any]) -> None:
        actor = payload.get("submitted_by", "operator")
        tenant = payload.get("tenant", "default")
        IdentityService().require(actor, "evidence:create", tenant)
        record = EvidenceStore().add(
            tenant=tenant,
            source=payload["source"],
            summary=payload.get("summary", payload["source"]),
            content=payload.get("content", ""),
            classification=payload.get("classification", "operator_provided"),
        )
        AuditStore().append(
            "evidence.created",
            tenant=record["tenant"],
            actor=actor,
            payload={"evidence_id": record["evidence_id"], "source": record["source"]},
        )
        self._json({"evidence": record}, HTTPStatus.CREATED)

    def _create_evidence_attachment(self, payload: dict[str, Any]) -> None:
        actor = payload.get("submitted_by", "operator")
        tenant = payload.get("tenant", "default")
        IdentityService().require(actor, "evidence_attachment:create", tenant)
        attachment = EvidenceAttachmentStore().add(
            tenant=tenant,
            submitted_by=actor,
            filename=payload["filename"],
            content_base64=payload["content_base64"],
            classification=payload.get("classification", "operator_provided"),
        )
        AuditStore().append(
            "evidence.attachment.created",
            tenant=tenant,
            actor=actor,
            payload={
                "attachment_id": attachment["attachment_id"],
                "filename": attachment["filename"],
                "sha256": attachment["sha256"],
            },
        )
        self._json({"attachment": attachment}, HTTPStatus.CREATED)

    def _create_request(self, payload: dict[str, Any]) -> None:
        IdentityService().require(
            payload.get("submitted_by", "operator"),
            "request:create",
            payload.get("tenant", "default"),
        )
        request = OrchestrationRequest(
            request_id=payload.get("request_id") or new_id("req"),
            submitted_by=payload.get("submitted_by", "operator"),
            tenant=payload.get("tenant", "default"),
            task=payload["task"],
            requested_action_boundary=RiskTier(payload.get("requested_action_boundary", "T0")),
        )
        envelope = generate_and_submit_plan(
            request,
            evidence_ids=payload.get("evidence_ids", []),
        )
        decision = envelope["governance_decision"]
        approval = None
        if decision["requires_approval"] and envelope["status"] == "ready_for_approval":
            approval = ApprovalQueue().create(
                request_id=request.request_id,
                tenant=request.tenant,
                requested_by=request.submitted_by,
                risk_tier=decision["risk_tier"],
                reason=decision.get("approval_reason") or "Approval required by risk tier",
                plan_hash=envelope["plan_hash"],
            )
            AuditStore().append(
                "approval.requested",
                tenant=request.tenant,
                actor=request.submitted_by,
                payload={
                    "request_id": request.request_id,
                    "approval_id": approval["approval_id"],
                    "plan_hash": envelope["plan_hash"],
                },
            )
        self._json({"request": envelope, "approval": approval}, HTTPStatus.CREATED)

    def _create_conversation(self, payload: dict[str, Any]) -> None:
        actor = payload.get("operator", payload.get("submitted_by", "operator"))
        tenant = payload.get("tenant", "default")
        IdentityService().require(actor, "conversation:create", tenant)
        conversation = ConversationStore().create(
            tenant=tenant,
            operator=actor,
            title=payload.get("title", "Untitled conversation"),
        )
        AuditStore().append(
            "conversation.created",
            tenant=tenant,
            actor=actor,
            payload={"conversation_id": conversation["conversation_id"]},
        )
        self._json({"conversation": conversation}, HTTPStatus.CREATED)

    def _append_conversation_message(self, payload: dict[str, Any]) -> None:
        actor = payload.get("operator", payload.get("submitted_by", "operator"))
        tenant = payload.get("tenant", "default")
        IdentityService().require(actor, "conversation:append", tenant)
        conversation = ConversationStore().append(
            conversation_id=payload["conversation_id"],
            tenant=tenant,
            operator=actor,
            role=payload["role"],
            content=payload["content"],
            metadata=payload.get("metadata", {}),
        )
        AuditStore().append(
            "conversation.message.appended",
            tenant=tenant,
            actor=actor,
            payload={
                "conversation_id": conversation["conversation_id"],
                "role": payload["role"],
            },
        )
        self._json({"conversation": conversation})

    def _decide_approval(self, payload: dict[str, Any]) -> None:
        IdentityService().require(
            payload.get("decided_by", "operator"),
            "approval:decide",
            payload.get("tenant", "default"),
        )
        record = ApprovalQueue().decide(
            approval_id=payload["approval_id"],
            status=payload["status"],
            decided_by=payload.get("decided_by", "operator"),
            decision_note=payload.get("decision_note", ""),
        )
        AuditStore().append(
            f"approval.{record['status']}",
            tenant=record["tenant"],
            actor=record["decided_by"] or "operator",
            payload={"approval_id": record["approval_id"], "request_id": record["request_id"]},
        )
        self._json({"approval": record})

    def _execute_dry_run(self, payload: dict[str, Any]) -> None:
        request = payload["request"]
        IdentityService().require(
            payload.get("actor", "operator"),
            "execution:dry_run",
            request.get("tenant", "default"),
        )
        plan = request["plan"]
        approved = ApprovalQueue().approved_for(
            request_id=request["request_id"],
            plan_hash=request["plan_hash"],
        )
        result = DryRunExecutionGateway().execute(
            request_id=request["request_id"],
            tenant=request["tenant"],
            actor=payload.get("actor", "operator"),
            plan=plan,
            approved=approved,
        )
        AuditStore().append(
            "execution.dry_run.completed",
            tenant=result["tenant"],
            actor=result["actor"],
            payload={
                "execution_id": result["execution_id"],
                "request_id": result["request_id"],
                "mode": result["mode"],
            },
        )
        self._json({"execution": result})

    def _connector_plan(self, payload: dict[str, Any]) -> None:
        IdentityService().require(
            payload.get("requested_by", "operator"),
            "connector:plan",
            payload.get("tenant", "default"),
        )
        domains = payload.get("domains", [])
        self._json({"commands": ReadOnlyDiagnosticConnector().plan(domains)})

    def _create_backup(self, payload: dict[str, Any]) -> None:
        actor = payload.get("requested_by", "operator")
        IdentityService().require(actor, "backup:create", payload.get("tenant", "default"))
        backup = create_backup()
        AuditStore().append(
            "appliance.backup.created",
            tenant=payload.get("tenant", "default"),
            actor=actor,
            payload={"backup_id": backup["backup_id"], "path": backup["path"]},
        )
        self._json({"backup": backup}, HTTPStatus.CREATED)

    def _stage_update(self, payload: dict[str, Any]) -> None:
        actor = payload.get("requested_by", "operator")
        IdentityService().require(actor, "update:stage", payload.get("tenant", "default"))
        update = stage_update(
            artifact_path=payload["artifact_path"],
            sha256=payload["sha256"],
            requested_by=actor,
            version=payload.get("version", "unknown"),
            notes=payload.get("notes", ""),
        )
        AuditStore().append(
            "appliance.update.staged",
            tenant=payload.get("tenant", "default"),
            actor=actor,
            payload={"update_id": update["update_id"], "apply_enabled": False},
        )
        self._json({"update": update}, HTTPStatus.CREATED)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body or "{}")

    def _json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_static(self, path: str) -> None:
        relative = "index.html" if path in {"", "/"} else path.lstrip("/")
        target = (UI_DIR / relative).resolve()
        if not str(target).startswith(str(UI_DIR.resolve())) or not target.exists():
            self._json({"error": "not_found"}, HTTPStatus.NOT_FOUND)
            return
        data = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "text/plain")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run(host: str = "127.0.0.1", port: int = 8085) -> None:
    server = ThreadingHTTPServer((host, port), EnterpriseOrchestratorHandler)
    print(f"Enterprise Orchestrator Appliance listening on http://{host}:{port}")
    server.serve_forever()


def _prompt_text() -> str:
    return (ROOT / "prompts" / "enterprise-orchestrator-v5.6.md").read_text(
        encoding="utf-8"
    )


def _sha256(value: str) -> str:
    import hashlib

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _optional_file(name: str) -> str:
    path = ROOT / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


if __name__ == "__main__":
    run(
        host=os.environ.get("EOA_HOST", "127.0.0.1"),
        port=int(os.environ.get("EOA_PORT", "8085")),
    )
