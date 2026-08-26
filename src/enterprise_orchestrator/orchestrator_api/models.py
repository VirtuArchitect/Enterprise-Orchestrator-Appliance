from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RiskTier(StrEnum):
    T0 = "T0"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"


class Confidence(StrEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class OrchestrationStatus(StrEnum):
    REJECTED = "rejected"
    NEEDS_EVIDENCE = "needs_evidence"
    READY_FOR_APPROVAL = "ready_for_approval"
    READY_FOR_T0_EXECUTION = "ready_for_t0_execution"
    EXECUTED_DRY_RUN = "executed_dry_run"


@dataclass(frozen=True)
class EvidenceReference:
    source: str
    classification: str = "operator_provided"
    summary: str = ""


@dataclass(frozen=True)
class OrchestrationRequest:
    request_id: str
    submitted_by: str
    task: str
    tenant: str = "default"
    evidence: tuple[EvidenceReference, ...] = field(default_factory=tuple)
    requested_action_boundary: RiskTier = RiskTier.T0


@dataclass(frozen=True)
class GovernanceDecision:
    status: OrchestrationStatus
    risk_tier: RiskTier
    confidence: Confidence
    requires_approval: bool
    blockers: tuple[str, ...]
    next_validation_steps: tuple[str, ...]
    approval_reason: str | None = None


PlanDict = dict[str, Any]


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str
    request_id: str
    tenant: str
    requested_by: str
    risk_tier: RiskTier
    status: str
    reason: str


@dataclass(frozen=True)
class ExecutionResult:
    execution_id: str
    request_id: str
    tenant: str
    mode: str
    status: str
    actions: tuple[str, ...]
