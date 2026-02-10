# Skylark Drones — Operations Coordinator AI Agent

Conversational AI agent for pilot roster, assignments, drone inventory, and conflict detection, with optional 2-way sync to Google Sheets. Built with **Streamlit** for the UI.

## Architecture overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Streamlit UI (app.py)                                           │
│  Chat input → agent.handle_message() → display reply             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Agent (agent.py)                                                │
│  Intent detection (keywords/regex) → call ops / sheets_sync     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Ops (ops.py)                                                    │
│  Roster, assignments, drone inventory, conflicts,               │
│  urgent reassignment logic                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Sheets sync (sheets_sync.py)                                    │
│  read_pilot_roster | read_drone_fleet | read_missions            │
│  write_pilot_roster | write_drone_fleet                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
  Google Sheets (if configured)            Local CSV (data/)
  PILOT_SHEET_ID, DRONE_SHEET_ID,         pilot_roster.csv,
  MISSIONS_SHEET_ID + credentials          drone_fleet.csv, missions.csv
```

- **app.py** — Streamlit chat interface; sends user message to the agent and shows markdown replies.
- **agent.py** — Maps natural language to actions (roster queries, status updates, assignments, drones, conflicts, urgent reassignment) and calls `ops` and `sheets_sync`.
- **ops.py** — Core logic: pilot/drone queries, matching pilots to projects, assign/unassign, conflict checks (double booking, skill/cert mismatch, drone in maintenance, location mismatch), and urgent reassignment suggestions.
- **sheets_sync.py** — Reads from and writes to Google Sheets when env is set; otherwise uses local CSVs in `data/`.
- **config.py** — Loads `.env` and decides whether to use Google Sheets.

## Features

| Area | Capabilities |
|------|----------------|
| **Roster** | Query by skill, certification, location, status; view assignments; update pilot status (syncs to Sheet) |
| **Assignments** | Match pilots to project; track assignments; assign/unassign with double-booking check |
| **Drone inventory** | Query by capability, location, status; maintenance due; update drone status (syncs to Sheet) |
| **Conflicts** | Double-booking, skill/cert mismatch, drone in maintenance assigned, pilot–project location mismatch |
| **Urgent reassignment** | Suggest pilots and drones for a project and list conflicts to resolve |

## Run locally

```bash
cd skylark
pip install -r requirements.txt
# Optional: copy .env.example to .env and set Google Sheet IDs + credentials path
streamlit run app.py
```

Open the URL shown (e.g. http://localhost:8501).

## Google Sheets setup (2-way sync)

1. Create a Google Cloud project and enable Google Sheets API; create a **Service Account** and download its JSON key.
2. Save the JSON as `credentials.json` in the project root (or set `GOOGLE_CREDENTIALS_JSON` in `.env`).
3. Create three Google Sheets (e.g. “Pilot Roster”, “Drone Fleet”, “Missions”). Upload the CSVs from `data/` so the first row is the header.
4. Share each sheet with the **service account email** (e.g. `…@….iam.gserviceaccount.com`) with Editor access.
5. Copy each sheet’s ID from the URL: `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit`.
6. In `.env` set:
   - `PILOT_SHEET_ID=...`
   - `DRONE_SHEET_ID=...`
   - `MISSIONS_SHEET_ID=...`

Pilot status and assignment updates, and drone status updates, will then sync back to the respective sheets.

## Deploy (e.g. Streamlit Community Cloud)

1. Push the repo to GitHub.
2. In [share.streamlit.io](https://share.streamlit.io), connect the repo and set **Main file path** to `app.py`.
3. Add **Secrets** (same as `.env`): `PILOT_SHEET_ID`, `DRONE_SHEET_ID`, `MISSIONS_SHEET_ID`, and either the JSON content or a path to the service account key. Without secrets, the app uses local CSV data only.

## Sample prompts

- *Who is available?* / *Pilots with Mapping skill in Bangalore*
- *Current assignments*
- *Set P001 status to On Leave*
- *Match pilots to PRJ001* / *Assign P003 to PRJ001*
- *Drones due for maintenance* / *Update D002 to Available*
- *Any conflicts?*
- *Urgent reassignment for PRJ002*

## Files

- `app.py` — Streamlit app
- `agent.py` — Conversational agent
- `ops.py` — Business logic
- `sheets_sync.py` — Google Sheets / CSV I/O
- `config.py` — Config and env
- `data/*.csv` — Local data fallback
- `DECISION_LOG.md` — Assumptions, trade-offs, “urgent reassignments” interpretation
