# OpenWebUI-Compatible Console Roadmap

The Enterprise Orchestrator Appliance should feel familiar to operators who have
used OpenWebUI, but it should not become a generic chatbot surface. The product
target is an OpenWebUI-compatible operator experience with EAAP-governed control
plane semantics.

## Adopt

- Conversation history scoped by tenant and operator.
- Model health and model settings visibility.
- Prompt policy pack visibility with version and contract status.
- Evidence and knowledge library with upload, search, provenance, and signature
  status.
- File attachment workflow that stores hashes and evidence metadata.
- Admin settings for appliance status, model endpoint, demo status, and release
  gates.
- Light and dark operator console modes.

## Govern Or Defer

- Tool calling must route through the execution gateway.
- Connectors must declare read-only, dry-run, approval, rollback, and audit
  boundaries.
- Web search must be disabled by default for air-gapped operation.
- Code execution must remain disabled until sandboxing, approval, and audit are
  implemented.
- Plugin-style extensions must be signed, allowlisted, and tenant-scoped.

## Do Not Clone Blindly

The appliance should not copy unrestricted public plugin marketplaces, arbitrary
tool execution, casual web search, or ungoverned file execution. Those features
weaken the infrastructure-operations boundary unless they are explicitly
governed.

## Priority Backlog

1. Add operator conversations with governed request history.
2. Add evidence library views with signature and semantic-search status.
3. Add prompt policy pack viewer.
4. Add model/runtime settings page.
5. Add admin release-gate and support-bundle page.
6. Add signed connector registry.
