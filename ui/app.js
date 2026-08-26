const state = {
  evidence: [],
  currentRequest: null,
};

const $ = (id) => document.getElementById(id);
const THEME_KEY = "enterprise-orchestrator-theme";

function applyTheme(theme) {
  const mode = theme === "dark" ? "dark" : "light";
  document.documentElement.dataset.theme = mode;
  const toggle = $("themeToggle");
  if (toggle) {
    toggle.textContent = mode === "dark" ? "Light mode" : "Dark mode";
    toggle.setAttribute("aria-pressed", String(mode === "dark"));
  }
}

function initializeTheme() {
  applyTheme(localStorage.getItem(THEME_KEY) || "light");
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || `HTTP ${response.status}`);
  }
  return payload;
}

function renderEvidence() {
  const list = $("evidenceList");
  if (!state.evidence.length) {
    list.innerHTML = '<div class="empty">No evidence attached.</div>';
    return;
  }
  list.innerHTML = state.evidence
    .map(
      (item) => `
        <div class="item">
          <strong>${escapeHtml(item.summary)}</strong>
          <small>${escapeHtml(item.evidence_id)} · ${escapeHtml(item.source)}</small>
        </div>
      `,
    )
    .join("");
}

function renderPlan(envelope) {
  const decision = envelope.governance_decision;
  $("planSummary").innerHTML = `
    <div class="pillRow">
      <span class="pill">Status: ${escapeHtml(envelope.status)}</span>
      <span class="pill">Risk: ${escapeHtml(decision.risk_tier)}</span>
      <span class="pill">Confidence: ${escapeHtml(decision.confidence)}</span>
      <span class="pill">Approval: ${decision.requires_approval ? "required" : "not required"}</span>
      <span class="pill">Model: ${escapeHtml(envelope.model.provider)} / ${escapeHtml(envelope.model.name)}</span>
    </div>
  `;
  $("planJson").textContent = JSON.stringify(envelope, null, 2);
  $("dryRun").disabled = envelope.status === "needs_evidence";
}

async function refreshApprovals() {
  const payload = await api(`/api/approvals?tenant=${encodeURIComponent($("tenant").value)}`);
  const list = $("approvalList");
  if (!payload.approvals.length) {
    list.innerHTML = '<div class="empty">No approvals pending.</div>';
    return;
  }
  list.innerHTML = payload.approvals
    .map(
      (approval) => `
        <div class="item">
          <strong>${escapeHtml(approval.risk_tier)} · ${escapeHtml(approval.status)}</strong>
          <small>${escapeHtml(approval.approval_id)} · ${escapeHtml(approval.reason)}</small>
          ${
            approval.status === "pending"
              ? `<button data-approval="${escapeHtml(approval.approval_id)}">Approve</button>`
              : ""
          }
        </div>
      `,
    )
    .join("");
  list.querySelectorAll("button[data-approval]").forEach((button) => {
    button.addEventListener("click", async () => {
      await api("/api/approvals/decide", {
        method: "POST",
        body: JSON.stringify({
          approval_id: button.dataset.approval,
          status: "approved",
          decided_by: $("operator").value,
          decision_note: "Approved from local operator UI.",
        }),
      });
      await refreshApprovals();
      await refreshAudit();
    });
  });
}

async function refreshHistory() {
  const payload = await api(`/api/requests?tenant=${encodeURIComponent($("tenant").value)}`);
  const list = $("historyList");
  if (!payload.requests.length) {
    list.innerHTML = '<div class="empty">No requests yet.</div>';
    return;
  }
  list.innerHTML = payload.requests
    .slice()
    .reverse()
    .slice(0, 6)
    .map(
      (request) => `
        <div class="item">
          <strong>${escapeHtml(request.status)} · ${escapeHtml(request.governance_decision.risk_tier)}</strong>
          <small>${escapeHtml(request.request_id)} · ${escapeHtml(request.plan.summary)}</small>
        </div>
      `,
    )
    .join("");
}

async function refreshAudit() {
  const payload = await api(`/api/audit?tenant=${encodeURIComponent($("tenant").value)}`);
  $("auditState").textContent = payload.chain_valid
    ? "Audit chain valid"
    : "Audit chain invalid";
  const list = $("auditList");
  if (!payload.events.length) {
    list.innerHTML = '<div class="empty">No audit events yet.</div>';
    return;
  }
  list.innerHTML = payload.events
    .slice()
    .reverse()
    .map(
      (event) => `
        <div class="item">
          <strong>${escapeHtml(event.event_type)}</strong>
          <small>${escapeHtml(event.created_at)} · ${escapeHtml(event.event_id)}</small>
        </div>
      `,
    )
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

$("addEvidence").addEventListener("click", async () => {
  const payload = await api("/api/evidence", {
    method: "POST",
    body: JSON.stringify({
      tenant: $("tenant").value,
      submitted_by: $("operator").value,
      source: $("evidenceSource").value,
      summary: $("evidenceSummary").value,
      content: $("evidenceContent").value,
    }),
  });
  state.evidence.push(payload.evidence);
  renderEvidence();
  await refreshAudit();
});

$("submitRequest").addEventListener("click", async () => {
  const payload = await api("/api/requests", {
    method: "POST",
    body: JSON.stringify({
      submitted_by: $("operator").value,
      tenant: $("tenant").value,
      task: $("task").value,
      requested_action_boundary: $("boundary").value,
      evidence_ids: state.evidence.map((item) => item.evidence_id),
    }),
  });
  state.currentRequest = payload.request;
  renderPlan(payload.request);
  await refreshApprovals();
  await refreshAudit();
  await refreshHistory();
});

$("dryRun").addEventListener("click", async () => {
  if (!state.currentRequest) return;
  const payload = await api("/api/execute/dry-run", {
    method: "POST",
    body: JSON.stringify({
      actor: $("operator").value,
      request: state.currentRequest,
    }),
  });
  $("planJson").textContent = JSON.stringify(
    { request: state.currentRequest, execution: payload.execution },
    null,
    2,
  );
  await refreshAudit();
  await refreshHistory();
});

$("searchEvidence").addEventListener("click", async () => {
  const payload = await api(
    `/api/evidence/search?tenant=${encodeURIComponent($("tenant").value)}&q=${encodeURIComponent($("evidenceSearch").value)}`,
  );
  state.evidence = payload.evidence;
  renderEvidence();
});

$("modelHealth").addEventListener("click", async () => {
  $("opsJson").textContent = JSON.stringify(await api("/api/model/health"), null, 2);
});

$("backupState").addEventListener("click", async () => {
  $("opsJson").textContent = JSON.stringify(
    await api("/api/backup", {
      method: "POST",
      body: JSON.stringify({
        tenant: $("tenant").value,
        requested_by: $("operator").value,
      }),
    }),
    null,
    2,
  );
  await refreshAudit();
});

$("connectorPlan").addEventListener("click", async () => {
  const domains = state.currentRequest?.plan?.domains || ["nutanix", "storage"];
  $("opsJson").textContent = JSON.stringify(
    await api("/api/connectors/read-only-plan", {
      method: "POST",
      body: JSON.stringify({ domains }),
    }),
    null,
    2,
  );
});

$("stageUpdate").addEventListener("click", async () => {
  $("opsJson").textContent = JSON.stringify(
    await api("/api/updates/stage", {
      method: "POST",
      body: JSON.stringify({
        tenant: $("tenant").value,
        requested_by: $("operator").value,
        version: "0.2.0-local",
        artifact_path: "internal-artifact-repository/enterprise-orchestrator.tar.gz",
        sha256: "replace-with-verified-sha256-before-transfer",
        notes: "Sample staged request; apply is disabled.",
      }),
    }),
    null,
    2,
  );
  await refreshAudit();
});

$("themeToggle").addEventListener("click", () => {
  const current = document.documentElement.dataset.theme === "dark" ? "dark" : "light";
  const next = current === "dark" ? "light" : "dark";
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
});

async function boot() {
  initializeTheme();
  const health = await api("/api/health");
  $("runtimeStatus").textContent = `${health.status} · ${health.runtime.llm_provider} · ${health.runtime.model}`;
  renderEvidence();
  await refreshApprovals();
  await refreshAudit();
  await refreshHistory();
}

boot().catch((error) => {
  $("runtimeStatus").textContent = error.message;
});
