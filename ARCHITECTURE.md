# Architecture

FastAPI is the HTTP boundary. The triage service orchestrates seven MCP tools.
The MCP layer owns CRM, knowledge-base, ticketing and audit capabilities so those
adapters can later be replaced by real enterprise connectors without rewriting policy.

Flow:
Client -> FastAPI -> Triage Service -> MCP Tools -> decision -> PostgreSQL audit/state
