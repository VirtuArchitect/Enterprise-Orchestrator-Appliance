from __future__ import annotations

import hashlib
import json
from pathlib import Path

from enterprise_orchestrator.audit_service import AuditStore
from enterprise_orchestrator.evidence_service import EvidenceStore
from enterprise_orchestrator.governance_engine import GovernanceEvaluator
from enterprise_orchestrator.json_store import read_json, write_json
from enterprise_orchestrator.paths import ensure_state_dir
from enterprise_orchestrator.llm_adapter import DeterministicPlanner, OllamaClient

from .contract import validate_model_output
from .models import (
    Confidence,
    EvidenceReference,
    GovernanceDecision,
    OrchestrationRequest,
    OrchestrationStatus,
    PlanDict,
    RiskTier,
)


APPROVAL_TIERS = {RiskTier.T1, RiskTier.T2, RiskTier.T3}
DISRUPTIVE_TIERS = {RiskTier.T2, RiskTier.T3}


def submit_plan(request: OrchestrationRequest, model_output: PlanDict) -> dict[str, object]:
    """Validate and govern a model-generated plan draft.

    The returned envelope is the Phase 1 API contract. It is suitable for an
    HTTP wrapper later, but is dependency-free for the first implementation.
    """

    validate_model_output(model_output)
    governance = GovernanceEvaluator().evaluate(model_output)
    decision = _decide(request, model_output, governance.blocking_findings)

    return {
        "request_id": request.request_id,
        "tenant": request.tenant,
        "submitted_by": request.submitted_by,
        "status": decision.status.value,
        "plan_hash": hash_plan(model_output),
        "evidence_hash": hash_evidence(
            [reference.__dict__ for reference in request.evidence]
        ),
        "plan": model_output,
        "governance_decision": {
            "risk_tier": decision.risk_tier.value,
            "confidence": decision.confidence.value,
            "requires_approval": decision.requires_approval,
            "blockers": list(decision.blockers),
            "next_validation_steps": list(decision.next_validation_steps),
            "approval_reason": decision.approval_reason,
            "rules_passed": governance.passed,
            "applied_rules": list(governance.applied_rules),
            "warnings": list(governance.warnings),
        },
    }


def generate_and_submit_plan(
    request: OrchestrationRequest,
    evidence_ids: list[str] | None = None,
    prompt_path: Path | None = None,
    evidence_store: EvidenceStore | None = None,
    audit_store: AuditStore | None = None,
) -> dict[str, object]:
    evidence_store = evidence_store or EvidenceStore()
    audit_store = audit_store or AuditStore()
    evidence = evidence_store.get_many(evidence_ids or [], tenant=request.tenant)
    request = OrchestrationRequest(
        request_id=request.request_id,
        submitted_by=request.submitted_by,
        task=request.task,
        tenant=request.tenant,
        evidence=tuple(
            EvidenceReference(
                source=item.get("source", ""),
                classification=item.get("classification", "operator_provided"),
                summary=item.get("summary", ""),
            )
            for item in evidence
        ),
        requested_action_boundary=request.requested_action_boundary,
    )
    prompt = _load_prompt(prompt_path)
    requested_boundary = request.requested_action_boundary.value

    planner = OllamaClient()
    if planner.available():
        try:
            result = planner.generate_plan(
                system_prompt=prompt,
                task=request.task,
                evidence=evidence,
                requested_action_boundary=requested_boundary,
            )
        except RuntimeError:
            result = DeterministicPlanner().generate_plan(
                task=request.task,
                evidence=evidence,
                requested_action_boundary=requested_boundary,
            )
    else:
        result = DeterministicPlanner().generate_plan(
            task=request.task,
            evidence=evidence,
            requested_action_boundary=requested_boundary,
        )

    envelope = submit_plan(request, result.plan)
    envelope["evidence_hash"] = hash_evidence(evidence)
    envelope["model"] = {"provider": result.provider, "name": result.model}
    _persist_request(envelope)
    audit_store.append(
        "plan.generated",
        tenant=request.tenant,
        actor=request.submitted_by,
        payload={
            "request_id": request.request_id,
            "plan_hash": envelope["plan_hash"],
            "status": envelope["status"],
            "model": envelope["model"],
        },
    )
    return envelope


def hash_plan(plan: PlanDict) -> str:
    encoded = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def hash_evidence(evidence: list[dict[str, object]]) -> str:
    encoded = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _decide(
    request: OrchestrationRequest,
    plan: PlanDict,
    governance_blockers: tuple[str, ...] = (),
) -> GovernanceDecision:
    plan_tier = RiskTier(plan["risk_tier"])
    confidence = Confidence(plan["confidence"])
    max_tier = _max_tier([request.requested_action_boundary, plan_tier, *_action_tiers(plan)])
    blockers: list[str] = list(governance_blockers)

    if confidence is Confidence.LOW:
        blockers.append("LOW_CONFIDENCE_REQUIRES_MORE_EVIDENCE")

    if max_tier in DISRUPTIVE_TIERS:
        if not plan["rollback"]:
            blockers.append("DISRUPTIVE_ACTION_REQUIRES_ROLLBACK")
        if not plan["validation"]:
            blockers.append("DISRUPTIVE_ACTION_REQUIRES_VALIDATION")

    action_requires_approval = any(
        action["requires_approval"] for action in plan["recommended_actions"]
    )
    requires_approval = max_tier in APPROVAL_TIERS or action_requires_approval

    if blockers:
        return GovernanceDecision(
            status=OrchestrationStatus.NEEDS_EVIDENCE,
            risk_tier=max_tier,
            confidence=confidence,
            requires_approval=requires_approval,
            blockers=tuple(blockers),
            next_validation_steps=tuple(plan["validation"] or plan["required"]),
        )

    if requires_approval:
        return GovernanceDecision(
            status=OrchestrationStatus.READY_FOR_APPROVAL,
            risk_tier=max_tier,
            confidence=confidence,
            requires_approval=True,
            blockers=(),
            next_validation_steps=tuple(plan["validation"]),
            approval_reason=f"{max_tier.value} action requires governed approval",
        )

    return GovernanceDecision(
        status=OrchestrationStatus.READY_FOR_T0_EXECUTION,
        risk_tier=max_tier,
        confidence=confidence,
        requires_approval=False,
        blockers=(),
        next_validation_steps=tuple(plan["validation"]),
    )


def _action_tiers(plan: PlanDict) -> list[RiskTier]:
    return [RiskTier(action["risk_tier"]) for action in plan["recommended_actions"]]


def _max_tier(tiers: list[RiskTier]) -> RiskTier:
    order = {
        RiskTier.T0: 0,
        RiskTier.T1: 1,
        RiskTier.T2: 2,
        RiskTier.T3: 3,
    }
    return max(tiers, key=lambda tier: order[tier])


def _load_prompt(prompt_path: Path | None = None) -> str:
    path = prompt_path or Path(__file__).resolve().parents[3] / "prompts" / "enterprise-orchestrator-v5.6.md"
    return path.read_text(encoding="utf-8")


def _persist_request(envelope: dict[str, object]) -> None:
    path = ensure_state_dir() / "requests.json"
    records = read_json(path, [])
    records.append(envelope)
    write_json(path, records)
