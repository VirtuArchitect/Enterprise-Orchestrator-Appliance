# LLM Adapter

Local model runtime boundary.

Implemented:

- Ollama-compatible `/api/generate` client using standard-library HTTP.
- `EOA_OLLAMA_URL` and `EOA_OLLAMA_MODEL` configuration.
- Deterministic offline fallback planner for smoke tests and disconnected
  appliances.

Future targets:

- llama.cpp server
- vLLM
