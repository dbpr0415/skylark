# Decision Log — Skylark Ops Coordinator Agent

## Key assumptions

- **Data source:** Pilot roster, drone fleet, and missions are the single source of truth. We assume `current_assignment` on pilots uses the same ID as `project_id` in missions (e.g. PRJ001) so that overlap and conflict checks work. Sample data uses "Project-A" for one pilot; for full conflict detection, roster assignments should use project_id (PRJ001, PRJ002, etc.).
- **Google Sheets:** 2-way sync means: (1) all reads come from Sheets when configured, (2) pilot status and assignment updates are written back to the Pilot Roster sheet, and (3) drone status updates are written back to the Drone Fleet sheet. Missions are read-only from the agent’s perspective (no write to missions).
- **Empty value:** Empty assignment/cells are normalized to "–" (en-dash) for consistency between CSV and Sheets.
- **Conversational interface:** The agent works without an LLM using intent/keyword matching so it runs with no API key. Optional OpenAI can be added later for freer language.

## Trade-offs

- **Intent-based agent vs full LLM:** We chose keyword/regex intents so the prototype works offline and without API keys. Trade-off: less flexible phrasing; user must use natural but recognizable phrases. With more time we’d add an optional LLM layer for open-ended questions.
- **Single worksheet per sheet:** We assume one worksheet per Google Sheet (default "Sheet1"). Multiple tabs would require sheet names in env or UI.
- **Conflict “double booking”:** With one `current_assignment` per pilot, true double booking only appears when assigning a pilot to a second project with overlapping dates. We block that at assignment time and run conflict checks that compare project dates and roster state.

## “Urgent reassignments” — interpretation

We interpret **urgent reassignments** as: *when a project needs immediate coverage (e.g. pilot unavailable, drone in maintenance), the agent should suggest alternative pilots and drones and surface conflicts that could block the reassignment.*

Implementation:

- **`suggest_urgent_reassignment(project_id)`** returns:
  - Suggested pilots (available, same location, matching skills/certs, available by project start).
  - Suggested drones (available, same location, matching capabilities).
  - Count of drones in maintenance.
  - Full conflict summary (double booking, skill/cert mismatch, drone in maintenance, location mismatch).

The user can then say e.g. *“Urgent reassignment for PRJ002”* and get a single response with who can be assigned, which drones to use, and what to fix (conflicts) before confirming.

## What we’d do differently with more time

- Add optional **OpenAI (or local LLM)** for true conversational understanding and follow-up questions.
- **Missions sheet writes:** Allow creating/updating mission rows from the agent (e.g. new project, date change) with sync back to Sheets.
- **Audit log:** Log all status and assignment changes with timestamp and user for accountability.
- **Tests:** Unit tests for `ops` and `sheets_sync`, and integration tests with mock Sheets.
- **Richer matching:** Consider pilot preference, travel cost, and drone–pilot compatibility in suggestions.
