# MERL Order — Module 1

**Professional, customer-facing web app for configuring and ordering MERL (Monitoring, Evaluation, Research & Learning) services.**

Built with Streamlit as a clean, guided, modern frontend experience similar to Domino’s or Tesla configurators.

## What Was Built (Module 1 Scope)

- Exact package structure specified:
  - **Entry-Level Packages**: MERL Starter Kit, Quick Evaluation Pack, Dashboard Lite
  - **Add-on Modules**: 6 layered upsells (Advanced Indicator Framework, Data Collection Tools, Custom Dashboard, Automated Reporting, Learning Products, Full MERL System Design)
- Complete 6-step user flow with live pricing
- Professional calm color palette (deep navy + teal)
- Fully dynamic price calculator (base + any combination of add-ons)
- Persistent state via `st.session_state`
- Clean Proposal Summary screen with generated scope narrative + downloadable .txt proposal
- No backend, no payments, no auth — pure frontend prototype ready for Module 2 (AI features, etc.)

## Project Structure

```
MERL-Ordering-App/
├── app.py                 # The complete single-file Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## How to Run Locally

### 1. Create & activate a virtual environment (recommended)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Key Features

- **Live pricing** — Updates instantly when you select/deselect anything
- **Sidebar summary** — Always-visible order cart + big Submit button
- **Guided but non-linear** — Change package or add-ons at any time before submitting
- **Professional cards** — Clear inclusions for every package and add-on
- **Validation** — Prevents submission without required fields
- **Proposal generation** — Beautiful summary view + one-click .txt download
- **Easy to customize** — All pricing and descriptions live at the top of `app.py` in two clean dictionaries (`PACKAGES` and `ADDONS`)

## Customization Guide (for future changes)

Edit the top of `app.py`:

```python
PACKAGES = {
    "MERL Starter Kit": {
        "price": 3950,           # ← change price
        "short_desc": "...",
        "includes": ["...", ...] # ← edit bullet list
    },
    ...
}

ADDONS = { ... }   # same pattern
```

Prices, descriptions, and inclusions can be changed without touching any UI logic.

## Out of Scope (Module 1 — Completed)

- Payment processing
- Real backend / database / order persistence
- User accounts or authentication
- AI-powered proposal generation (planned for Module 2)
- Email sending (simulated only)

## Next Steps / Module 2 Ideas (Not Implemented)

- AI-generated detailed proposal narrative (using LLM)
- Real email confirmation (SendGrid / Resend / etc.)
- Persistent orders (Supabase, Airtable, or Postgres)
- User login / saved carts
- Multi-step wizard with progress stepper component
- Quote PDF generation (WeasyPrint / ReportLab)
- Admin dashboard to view submitted orders

## Tech Notes

- Single-file architecture for simplicity and easy deployment
- Heavy use of `st.session_state` + widget keys for state
- Custom CSS injected for premium consulting-firm aesthetic
- Fully responsive (works on tablet; acceptable on mobile)
- Zero external API calls

---

**Built as Module 1 of the MERL Ordering Platform — April 2026**

Questions or feedback on the flow? Open an issue or start a conversation with the team.
