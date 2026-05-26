"""
MERL Order — Client-Centric Edition

Professional, premium proposal configurator for NGOs, foundations, and donor-funded programs.
Branded for Altamont Group.

Refined architecture (light extraction, same folder):
- config.py: brand constants, PACKAGES, ADDONS, pure helpers
- sheets.py: lazy, strict Google Sheets client with excellent errors
- proposal.py: proposal text generation

`streamlit run app.py` continues to be the only command needed.
"""

import streamlit as st
from datetime import datetime
import random
import html

# === Extracted modules (light modularization, same folder) ===
from config import (
    PAGE_TITLE,
    PAGE_ICON,
    LOGO_PATH,
    PRIMARY_NAVY,
    ACCENT_TEAL,
    LIGHT_TEAL,
    SOFT_TEAL,
    CARD_BORDER,
    BG_LIGHT,
    TEXT_DARK,
    TEXT_MUTED,
    ACCENT_GOLD,
    WHITE,
    PACKAGES,
    ADDONS,
    SECTORS,
    TIMELINE_OPTIONS,
    get_addon_checkbox_key,
    calculate_total,
    validate_order,
)
from sheets import save_order_to_sheet, SheetsConfigurationError
from proposal import generate_proposal_text

# ============================================================================
# CONFIGURATION - All client-facing content and pricing in one place
# ============================================================================

PAGE_TITLE = "Order MERL Support | Altamont Group"
PAGE_ICON = "altamont_logo.png"

# Brand colors — premium consulting aesthetic (deep navy + confident green)
PRIMARY_NAVY = "#0B1426"
ACCENT_TEAL = "#0F766E"
LIGHT_TEAL = "#CCFBF1"
SOFT_TEAL = "#0D9488"
CARD_BORDER = "#E2E8F0"
BG_LIGHT = "#F8FAFC"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#475569"
ACCENT_GOLD = "#854D0E"
WHITE = "#FFFFFF"

LOGO_PATH = "altamont_logo.png"

# ------------------------------------------------------------------------
# CLIENT-CENTRIC BASE PACKAGES
# Reframed around common client situations and outcomes, not internal MERL products.
# Language focuses on what the client gets and why it matters to them.
# ------------------------------------------------------------------------

PACKAGES = {
    "Build Your Foundation": {
        "price": 4850,
        "tagline": "Best for new programs or major redesigns",
        "client_benefit": "Establish clear measures of success and a practical monitoring system so you start strong, measure what matters, and satisfy donor requirements from day one.",
        "includes": [
            "Up to 20 core performance measures with plain-language definitions",
            "Practical monitoring plan tailored to your implementation realities",
            "Results framework that connects activities to outcomes",
            "One focused virtual workshop with your team (90 minutes)",
            "Clean deliverables package + 30 days of email support"
        ]
    },
    "Demonstrate Results": {
        "price": 7250,
        "tagline": "Best for mid-term reviews, final evaluations, or donor accountability",
        "client_benefit": "Receive rigorous, independent evidence of results plus clear recommendations — the kind of professional evaluation that builds donor confidence and guides your next phase.",
        "includes": [
            "Full evaluation design and methodology aligned to your questions",
            "Ready-to-use qualitative and quantitative data collection tools",
            "Sampling strategy and realistic fieldwork timeline",
            "Comprehensive findings report (25–35 pages) with executive summary",
            "Virtual presentation to your team and key stakeholders"
        ]
    },
    "Turn Data into Decisions": {
        "price": 5750,
        "tagline": "Best when you have data but need clearer insights and reporting",
        "client_benefit": "Transform raw data into compelling dashboards, automated reports, and donor-ready communications that make your impact visible and credible.",
        "includes": [
            "Custom interactive dashboard (Power BI or Tableau) branded for you",
            "Up to 6 priority visualizations tied to your key results",
            "Automated quarterly and annual reporting templates",
            "90-minute hands-on training session for your team",
            "90 days of light support and refinements"
        ]
    }
}

# ------------------------------------------------------------------------
# SIMPLE, TRANSPARENT ADD-ONS
# Clear value, minimal jargon, focused on common client pain points.
# ------------------------------------------------------------------------

ADDONS = {
    "Gender, Equity & Inclusion Focus": {
        "price": 1850,
        "desc": "Integrate strong GESI analysis and disaggregated indicators throughout your framework or evaluation so you can credibly report on equity outcomes.",
        "client_value": "Show donors and stakeholders that you are serious about inclusion and leaving no one behind."
    },
    "Donor-Ready Reporting Pack": {
        "price": 1650,
        "desc": "Custom templates and automation for your primary donor’s reporting requirements, plus narrative support that makes your results shine.",
        "client_value": "Cut reporting time dramatically and submit polished, consistent reports every quarter."
    },
    "Stakeholder Data Collection Tools": {
        "price": 1950,
        "desc": "Professionally designed surveys, interview guides, and mobile data collection setup (Kobo/ODK) with enumerator guidance.",
        "client_value": "Collect high-quality data from the field without reinventing the wheel or hiring expensive consultants."
    },
    "Executive Dashboard & Portal": {
        "price": 4250,
        "desc": "Premium interactive dashboard with role-based views, automated email summaries, and a clean executive portal for leadership and boards.",
        "client_value": "Give your leadership and donors an always-on, beautiful view of progress they can trust."
    },
    "Learning Briefs & Knowledge Products": {
        "price": 1450,
        "desc": "Two to three high-quality learning briefs, case studies, or one-pagers with professional design — perfect for sharing with partners and funders.",
        "client_value": "Turn your results into compelling stories that build your reputation and support resource mobilization."
    },
    "Team Capability Workshop": {
        "price": 2250,
        "desc": "Half-day virtual workshop that equips your team with practical skills to maintain and use your new MERL system long after we leave.",
        "client_value": "Build lasting internal capacity instead of remaining dependent on external support."
    }
}

# (SECTORS and TIMELINE_OPTIONS are now imported from config.py)

# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    defaults = {
        "base_package": None,
        "order_submitted": False,
        "proposal_data": None,
        "submit_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def clear_all_selections():
    st.session_state.base_package = None

    for name in ADDONS.keys():
        key = get_addon_checkbox_key(name)
        if key in st.session_state:
            del st.session_state[key]

    form_keys = ["proj_name", "org_name", "contact_email", "sector", "timeline", "num_beneficiaries", "notes"]
    for key in form_keys:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.order_submitted = False
    st.session_state.proposal_data = None
    st.session_state.submit_error = None

def load_example_order():
    """Realistic premium example that showcases the client-centric flow."""
    st.session_state.base_package = "Demonstrate Results"

    example_addons = [
        "Gender, Equity & Inclusion Focus",
        "Donor-Ready Reporting Pack",
        "Learning Briefs & Knowledge Products",
    ]
    for name in ADDONS.keys():
        key = get_addon_checkbox_key(name)
        st.session_state[key] = name in example_addons

    st.session_state.proj_name = "Sahel Resilience & Livelihoods Programme – Phase 2"
    st.session_state.org_name = "Horizon Foundation"
    st.session_state.contact_email = "merl@horizonfdn.org"
    st.session_state.sector = "Climate Resilience & Environment"
    st.session_state.timeline = "6–12 months (multi-phase or complex)"
    st.session_state.num_beneficiaries = 185000
    st.session_state.notes = "Primary donor is FCDO. Strong emphasis on climate adaptation outcomes for women and youth. Need evaluation that can support a potential scale-up decision in 2027. Existing data collection partners in Niger and Mali."

    st.session_state.submit_error = None

# ============================================================================
# HELPERS
# ============================================================================

def get_selected_addons():
    """Return the list of add-on names whose checkboxes are currently checked."""
    selected = []
    for name in ADDONS.keys():
        key = get_addon_checkbox_key(name)
        if st.session_state.get(key, False):
            selected.append(name)
    return selected


# Note: calculate_total, validate_order, and save_order_to_sheet are now imported from config.py / sheets.py
# The old local definitions have been removed to eliminate duplication.

def get_current_form_values():
    return {
        "project_name": st.session_state.get("proj_name", "").strip(),
        "organization": st.session_state.get("org_name", "").strip(),
        "email": st.session_state.get("contact_email", "").strip(),
        "sector": st.session_state.get("sector", ""),
        "timeline": st.session_state.get("timeline", ""),
        "num_beneficiaries": st.session_state.get("num_beneficiaries", 0),
        "notes": st.session_state.get("notes", "").strip(),
    }

# (validate_order is now imported from config.py — old duplicate definition removed)


def capture_proposal_snapshot():
    base = st.session_state.base_package
    addons = get_selected_addons()
    details = get_current_form_values()
    total = calculate_total(base, addons)

    is_valid, error = validate_order(base, details, addons)
    if not is_valid:
        st.session_state.submit_error = error
        return False

    proposal_id = f"ALT-{datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"

    st.session_state.proposal_data = {
        "proposal_id": proposal_id,
        "submitted_at": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        "base_package": base,
        "base_price": PACKAGES[base]["price"],
        "base_tagline": PACKAGES[base]["tagline"],
        "base_benefit": PACKAGES[base]["client_benefit"],
        "base_includes": PACKAGES[base]["includes"],
        "addons": addons,
        "addon_prices": {a: ADDONS[a]["price"] for a in addons},
        "addon_values": {a: ADDONS[a]["client_value"] for a in addons},
        "total": total,
        "details": details,
    }
    st.session_state.order_submitted = True
    st.session_state.submit_error = None
    return True

def generate_proposal_text(data):
    """Professional plain-text proposal for download / email forwarding.
    Updated to align with the prominent 'Copy Proposal & Send to Altamont Group' flow.
    """
    lines = []
    lines.append("=" * 74)
    lines.append("ALTAMONT GROUP")
    lines.append("CONFIDENTIAL CLIENT PROPOSAL")
    lines.append(f"Proposal ID: {data['proposal_id']}")
    lines.append(f"Prepared: {data['submitted_at']}")
    lines.append("=" * 74)
    lines.append("")
    lines.append("ACTION REQUIRED: Use the 'Copy Proposal & Send to Altamont Group' button")
    lines.append("on the proposal screen, then paste into an email to zs@altamontgroup.ca")
    lines.append("We typically respond within 1 business day with next steps.")
    lines.append("")
    lines.append("This document summarizes the scope and investment for the requested")
    lines.append("Monitoring, Evaluation, Research & Learning (MERL) support.")
    lines.append("Final deliverables and pricing will be confirmed after a short scoping call.")
    lines.append("")

    d = data["details"]
    if d.get("organization") or d.get("project_name"):
        lines.append("PREPARED FOR")
        lines.append("-" * 20)
        if d.get("organization"):
            lines.append(f"{d['organization']}")
        if d.get("project_name"):
            lines.append(f"Project: {d['project_name']}")
        if d.get("email"):
            lines.append(f"Contact: {d['email']}")
        lines.append("")

    lines.append("SELECTED ENGAGEMENT")
    lines.append("-" * 20)
    lines.append(f"{data['base_package']}  —  ${data['base_price']:,} USD")
    lines.append(f"Focus: {data['base_tagline']}")
    lines.append("")
    lines.append("What you receive:")
    for item in data["base_includes"]:
        lines.append(f"  • {item}")
    lines.append("")
    lines.append(f"Why this matters: {data['base_benefit']}")
    lines.append("")

    if data["addons"]:
        lines.append("OPTIONAL ENHANCEMENTS SELECTED")
        lines.append("-" * 20)
        for addon in data["addons"]:
            price = data["addon_prices"].get(addon, 0)
            value = data["addon_values"].get(addon, "")
            lines.append(f"+ {addon}  —  ${price:,}")
            if value:
                lines.append(f"   {value}")
        lines.append("")
    else:
        lines.append("OPTIONAL ENHANCEMENTS: None selected")
        lines.append("")

    lines.append("PROJECT CONTEXT")
    lines.append("-" * 20)
    lines.append(f"Sector: {d.get('sector', '—')}")
    lines.append(f"Timeline: {d.get('timeline', '—')}")
    if d.get("num_beneficiaries"):
        lines.append(f"Estimated reach: {d['num_beneficiaries']:,} people")
    if d.get("notes"):
        lines.append(f"Special considerations: {d['notes']}")
    lines.append("")

    lines.append("TOTAL ESTIMATED INVESTMENT")
    lines.append("-" * 20)
    lines.append(f"USD ${data['total']:,}")
    lines.append("One-time professional services fee (no hidden costs).")
    lines.append("Note: This is a transparent estimate. Final quote issued after scoping.")
    lines.append("")

    lines.append("WHAT HAPPENS NEXT")
    lines.append("-" * 20)
    lines.append("1. Click 'Copy Proposal & Send to Altamont Group' on the summary screen.")
    lines.append("2. Paste the text into an email and send to zs@altamontgroup.ca.")
    lines.append("3. Altamont reviews your requirements (usually within 1 business day).")
    lines.append("4. You receive a calendar link for a 30-minute scoping conversation.")
    lines.append("5. We send a formal Statement of Work and refined quote within 48 hours.")
    lines.append("6. Work begins promptly once the agreement is signed.")
    lines.append("")
    lines.append("We pride ourselves on clear communication, rigorous methods, and")
    lines.append("practical deliverables that actually get used.")
    lines.append("")
    lines.append("=" * 74)
    lines.append("Altamont Group")
    lines.append("Strategic advisory for organizations that want measurable impact.")
    lines.append("www.altamontgroup.ca")
    lines.append("=" * 74)

    return "\n".join(lines)

# ============================================================================
# PREMIUM CSS — Generous spacing, strong hierarchy, approachable professionalism
# ============================================================================

def inject_custom_css():
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    :root {{
        --navy: {PRIMARY_NAVY};
        --teal: {ACCENT_TEAL};
        --teal-light: {LIGHT_TEAL};
        --teal-soft: {SOFT_TEAL};
        --border: {CARD_BORDER};
        --bg: {BG_LIGHT};
        --text: {TEXT_DARK};
        --muted: {TEXT_MUTED};
        --gold: {ACCENT_GOLD};
        --white: {WHITE};
    }}

    .stApp {{
        background-color: var(--bg);
        font-feature-settings: "kern" 1, "tnum" 1, "cv05" 1;
    }}
    
    /* Global premium typography & rhythm */
    h1, h2, h3, h4, h5 {{
        color: var(--navy);
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 700;
        letter-spacing: -0.028em;
    }}
    
    .stMarkdown p, .stMarkdown li, .stMarkdown div, .stMarkdown span {{
        color: var(--text);
        font-size: 0.95rem;
        line-height: 1.72;
    }}

    /* Refined inputs — even more premium, taller, better focus */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {{
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        background: var(--white) !important;
        box-shadow: 0 1px 2px rgb(15 23 42 / 0.03) !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {{
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 6px rgba(15, 118, 110, 0.11), 0 1px 2px rgb(15 23 42 / 0.04) !important;
        outline: none !important;
    }}
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {{
        font-weight: 600 !important;
        color: var(--navy) !important;
        font-size: 0.87rem !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.012em;
    }}

    /* Top brand header — refined executive bar */
    .top-brand-bar {{
        background: linear-gradient(90deg, var(--navy) 0%, #0b1426 100%);
        padding: 16px 36px;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 6px solid var(--teal);
        box-shadow: 0 10px 30px -10px rgb(11 20 38 / 0.35);
    }}

    /* HERO — tighter, more commanding presence, reduced excessive whitespace */
    .hero-section {{
        text-align: center;
        padding: 2.35rem 2.1rem 2.0rem;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 22px;
        border: 1px solid var(--border);
        margin-bottom: 1.35rem;
        box-shadow: 0 28px 55px -16px rgb(15 23 42 / 0.09), 0 14px 24px -10px rgb(15 23 42 / 0.05);
        position: relative;
        overflow: hidden;
    }}
    .hero-section::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: linear-gradient(to right, var(--teal), var(--teal-soft));
    }}
    
    .hero-headline {{
        font-size: 2.58rem;
        line-height: 1.02;
        font-weight: 800;
        color: var(--navy);
        margin-bottom: 0.42rem;
        letter-spacing: -0.82px;
    }}
    
    .hero-sub {{
        font-size: 0.98rem;
        color: var(--muted);
        max-width: 640px;
        margin: 0 auto 1.05rem;
        line-height: 1.55;
    }}

    /* Trust bar — tighter, more refined credibility signals */
    .trust-card {{
        background: white;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px 11px 11px;
        text-align: center;
        box-shadow: 0 4px 12px -4px rgb(15 23 42 / 0.05);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .trust-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -6px rgb(15 23 42 / 0.09);
        border-color: #c0c9d9;
    }}
    .trust-num {{
        font-size: 1.42rem;
        font-weight: 800;
        color: var(--teal);
        line-height: 1.0;
        letter-spacing: -0.48px;
    }}

    /* Premium section headers — tighter rhythm */
    .section-header {{
        font-size: 1.12rem;
        font-weight: 800;
        color: var(--navy);
        margin: 1.65rem 0 0.38rem;
        padding-bottom: 7px;
        letter-spacing: -0.32px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .section-header::before {{
        content: "";
        display: inline-block;
        width: 34px;
        height: 3.75px;
        background: linear-gradient(to right, var(--teal), var(--teal-soft));
        border-radius: 4px;
    }}
    .section-caption {{
        color: var(--muted);
        font-size: 0.91rem;
        margin-bottom: 1.1rem;
        line-height: 1.55;
    }}

    /* PREMIUM Package cards — tighter, more commanding, elevated presence */
    .pkg-card {{
        background: white;
        border: 1.75px solid var(--border);
        border-radius: 20px;
        padding: 22px 22px 18px;
        height: 100%;
        transition: all 0.25s cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 6px 16px -4px rgb(15 23 42 / 0.07), 0 3px 6px -2px rgb(15 23 42 / 0.04);
        position: relative;
        display: flex;
        flex-direction: column;
    }}
    .pkg-card:hover {{
        border-color: #c0c9d9;
        box-shadow: 0 14px 28px -8px rgb(15 23 42 / 0.11), 0 6px 12px -3px rgb(15 23 42 / 0.06);
        transform: translateY(-2px);
    }}
    .pkg-card.selected {{
        border-color: var(--teal);
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
        box-shadow: 0 20px 38px -10px rgb(13 148 136 / 0.22), 0 10px 16px -4px rgb(13 148 136 / 0.14);
        transform: translateY(-4px);
    }}
    .pkg-card.selected::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: linear-gradient(to right, var(--teal), var(--teal-soft));
        border-radius: 20px 20px 0 0;
    }}
    .pkg-card.selected::after {{
        content: "SELECTED";
        position: absolute;
        top: 15px;
        right: 16px;
        background: var(--teal);
        color: white;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 1.4px;
        padding: 2px 9px 1px;
        border-radius: 999px;
        box-shadow: 0 2px 5px rgb(13 148 136 / 0.28);
    }}
    .pkg-card h3 {{
        margin: 0 0 2px 0;
        font-size: 1.22rem;
        font-weight: 800;
        color: var(--navy);
        letter-spacing: -0.36px;
    }}
    .pkg-tagline {{
        font-size: 0.74rem;
        color: var(--teal);
        font-weight: 800;
        letter-spacing: 0.4px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }}
    .pkg-benefit {{
        font-size: 0.90rem;
        line-height: 1.48;
        color: var(--text);
        margin-bottom: 12px;
        min-height: 66px;
        flex: 1;
    }}
    .pkg-price {{
        font-size: 2.02rem;
        font-weight: 800;
        color: var(--teal);
        margin: 1px 0 2px;
        letter-spacing: -0.7px;
        line-height: 1;
    }}
    .pkg-includes {{
        margin-top: 2px;
        padding-top: 9px;
        border-top: 1px solid var(--border);
    }}

    /* Premium Add-on cards — tighter, clearer hierarchy, stronger visual integration */
    .addon-card {{
        background: white;
        border: 1.5px solid var(--border);
        border-radius: 16px;
        padding: 15px 16px 13px;
        height: 100%;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 3px 10px -3px rgb(15 23 42 / 0.06);
        display: flex;
        flex-direction: column;
    }}

    .addon-card:hover {{
        border-color: #8fa3b8;
        box-shadow: 0 12px 22px -6px rgb(15 23 42 / 0.11);
        transform: translateY(-2px);
    }}
    .addon-card .stCheckbox {{
        margin-top: auto;
        padding-top: 6px;
    }}
    .addon-title {{
        font-weight: 800;
        font-size: 0.94rem;
        color: var(--navy);
        margin-bottom: 3px;
        letter-spacing: -0.16px;
        line-height: 1.25;
    }}
    .addon-desc {{
        font-size: 0.81rem;
        color: var(--muted);
        line-height: 1.45;
        margin-bottom: 5px;
        flex: 1;
        min-height: 40px;
    }}
    .addon-value {{
        font-size: 0.77rem;
        font-style: italic;
        color: var(--teal);
        margin-bottom: 5px;
        line-height: 1.32;
    }}
    .addon-price {{
        color: var(--teal-soft);
        font-weight: 800;
        font-size: 0.98rem;
        letter-spacing: -0.25px;
        display: block;
        margin-bottom: 1px;
    }}

    /* Sidebar total — more executive, commanding, premium presence */
    .sidebar-total {{
        background: linear-gradient(150deg, var(--navy) 0%, #0a1322 100%);
        color: white !important;
        padding: 18px 20px 16px;
        border-radius: 16px;
        text-align: center;
        margin: 10px 0 8px;
        box-shadow: 0 14px 30px -8px rgb(11 20 38 / 0.48);
        border: 1px solid rgba(255,255,255,0.08);
    }}
    .sidebar-total .label {{
        font-size: 0.62rem;
        opacity: 0.75;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        font-weight: 700;
        color: white !important;
    }}
    .sidebar-total .amount {{
        font-size: 2.28rem;
        font-weight: 800;
        line-height: 1.0;
        margin-top: 2px;
        letter-spacing: -0.85px;
        color: white !important;
    }}
    .sidebar-total > div:last-child {{
        color: rgba(255,255,255,0.72) !important;
    }}

    /* Proposal screen — high-end client document quality */
    .proposal-container {{
        max-width: 1100px;
        margin: 0 auto;
        padding-bottom: 2.2rem;
    }}
    .proposal-banner {{
        background: linear-gradient(135deg, var(--navy) 0%, #1e2937 100%);
        color: white;
        padding: 27px 36px;
        border-radius: 20px;
        margin: 10px 0 26px;
        box-shadow: 0 22px 44px -14px rgb(15 23 42 / 0.34);
        border: 1px solid rgba(255,255,255,0.08);
    }}
    .scope-section {{
        background: #f8fafc;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 17px 21px;
        margin-bottom: 0.95rem;
        box-shadow: 0 2px 6px rgb(15 23 42 / 0.025);
        font-size: 0.94rem;
        line-height: 1.58;
    }}
    .next-steps-box {{
        background: #f0fdfa;
        border-left: 7px solid var(--teal);
        padding: 19px 23px;
        border-radius: 14px;
        margin: 0.95rem 0;
    }}
    .next-steps-box ol {{
        margin: 10px 0 0 18px;
        padding: 0;
    }}
    .next-steps-box li {{
        margin-bottom: 6px;
        line-height: 1.55;
        font-size: 0.93rem;
    }}

    /* Prominent, unmistakable CTA zone for Request My Proposal */
    .submit-cta {{
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 2.75px solid var(--teal);
        border-radius: 24px;
        padding: 32px 38px 30px;
        margin: 2.25rem 0 0.55rem;
        text-align: center;
        box-shadow: 0 28px 48px -16px rgb(13 148 136 / 0.15), 0 14px 18px -7px rgb(13 148 136 / 0.08);
    }}
    .submit-cta h3 {{
        font-size: 1.48rem;
        margin: 0 0 9px;
        color: var(--navy);
        letter-spacing: -0.32px;
    }}
    .submit-cta p {{
        color: var(--muted);
        max-width: 580px;
        margin: 0 auto 22px;
        font-size: 0.96rem;
        line-height: 1.6;
    }}

    /* Premium buttons — more commanding, professional, cohesive presence */
    .stButton > button {{
        border-radius: 14px;
        font-weight: 800;
        padding: 0.72rem 1.85rem;
        letter-spacing: 0.3px;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.95rem;
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(155deg, var(--teal) 0%, var(--teal-soft) 100%);
        border: none;
        box-shadow: 0 12px 26px -7px rgb(13 148 136 / 0.45);
        color: white !important;
        font-weight: 800;
    }}
    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 18px 34px -8px rgb(13 148 136 / 0.52);
        background: linear-gradient(155deg, var(--teal-soft) 0%, var(--teal) 100%);
    }}
    .stButton > button[kind="secondary"] {{
        border: 1.75px solid var(--border);
        background: white;
        color: var(--navy);
        font-weight: 700;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background: #f8fafc;
        border-color: #8fa3b8;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px -3px rgb(15 23 42 / 0.08);
    }}

    /* The example loader gets extra visual weight from placement + emoji label in hero */

    /* Strong email action panel on proposal — clearer, more directive instructions */
    .email-action-panel {{
        background: linear-gradient(180deg, #f0fdfa 0%, #ecfdf5 100%);
        border: 2.5px solid #0f766e;
        border-radius: 18px;
        padding: 22px 26px 20px;
        margin: 0.85rem 0 1.15rem;
        box-shadow: 0 12px 24px -8px rgb(13 148 136 / 0.13);
    }}
    .email-action-panel .instruction {{
        font-size: 0.95rem;
        color: #0f766e;
        line-height: 1.48;
        margin-bottom: 11px;
        font-weight: 600;
    }}

    /* Delivery / important callout */
    .delivery-callout {{
        background: linear-gradient(95deg, #fefce8 0%, #fef9c3 100%);
        border: 1.5px solid #fde047;
        border-radius: 16px;
        padding: 18px 24px;
        margin: 12px 0 18px;
    }}
    .delivery-callout strong {{
        color: #713f12;
    }}

    .small-muted {{
        font-size: 0.76rem;
        color: var(--muted);
    }}
    .premium-note {{
        font-size: 0.81rem;
        color: #64748b;
        text-align: center;
        margin-top: 1.65rem;
        letter-spacing: -0.1px;
    }}

    /* Minor Streamlit polish + spacing */
    .stDivider {{
        margin: 0.95rem 0 !important;
    }}
    .stSuccess {{
        border-radius: 12px;
        border-left: 5px solid var(--teal);
    }}
    .stExpander {{
        border-radius: 12px !important;
    }}
    
    /* Better column & container breathing */
    .stColumn > div {{
        gap: 0.25rem;
    }}

    /* Slightly tighter Streamlit widget spacing for better visual density */
    .stMarkdown, .stTextInput, .stSelectbox, .stNumberInput, .stTextArea {{
        margin-bottom: 0.32rem !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# RENDER FUNCTIONS
# ============================================================================

def render_top_bar():
    """Ultra-premium header bar with prominent, confident logo presence."""
    col_logo, col_text = st.columns([1.35, 6.8])
    
    with col_logo:
        try:
            st.image(LOGO_PATH, width=168)
        except Exception:
            st.markdown(f"<span style='font-size:1.15rem; font-weight:800; color:{PRIMARY_NAVY}; letter-spacing:-0.5px;'>ALTAMONT</span>", unsafe_allow_html=True)
    
    with col_text:
        st.markdown(
            f"""
            <div style="padding-top:6px;">
                <span style="font-size:1.72rem; font-weight:800; color:{PRIMARY_NAVY}; letter-spacing:-0.52px; line-height:1.0;">Altamont Group</span><br>
                <span style="font-size:0.78rem; color:{TEXT_MUTED}; font-weight:600; letter-spacing:-0.005em;">Strategic advisory for measurable impact &nbsp;•&nbsp; Global reach, boutique precision</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""<div style="height:3px; background:linear-gradient(to right, transparent, {ACCENT_TEAL}22, transparent); margin:11px 0 18px 0;"></div>""",
        unsafe_allow_html=True,
    )

def render_hero():
    """Premium, high-impact hero with prominent, attractive example loader."""
    # Hero banner image — 280px (one third of a typical large banner, doubled from previous 140px)
    st.image("images/hero_team.jpg", width=280)

    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-headline">
                High-quality MERL support,<br>without the RFP headache.
            </div>
            <div class="hero-sub">
                NGOs, foundations, and donor-funded programs use Altamont Group to get clear, 
                fixed-scope proposals for monitoring, evaluation, and learning — delivered with 
                professional rigor and zero surprises.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Prominent, attractive "Load a Realistic Example" — now highly visible
    c1, c2, c3 = st.columns([1.0, 2.6, 1.0])
    with c2:
        if st.button(
            "✨  Load a Realistic Example",
            type="secondary",
            use_container_width=True,
            help="Load a complete, high-quality sample order from a real foundation to explore the experience",
        ):
            load_example_order()
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:0.25rem; margin-bottom:0.6rem;">
            <span class="small-muted">See exactly how a strong order looks • 48-hour proposal turnaround • No obligation</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_trust_bar():
    """Credibility signals that matter to clients."""
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    
    items = [
        ("20+", "countries of experience"),
        ("120+", "MERL engagements"),
        ("48 hrs", "proposal turnaround"),
        ("Boutique", "personal attention, global reach"),
    ]
    
    for col, (num, label) in zip([c1, c2, c3, c4], items):
        with col:
            st.markdown(
                f"""
                <div class="trust-card">
                    <div class="trust-num">{num}</div>
                    <div class="small-muted" style="margin-top:2px;">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

def render_package_selection():
    """Client-first package selection — situations and benefits, not features."""
    st.markdown('<div class="section-header">1. Choose the best starting point for your situation</div>', unsafe_allow_html=True)
    st.caption("All three options include a kickoff call, clear deliverables, one round of revisions, and direct access to senior MERL advisors. No hidden fees.")

    pkg_names = list(PACKAGES.keys())
    cols = st.columns(3, gap="medium")

    for i, name in enumerate(pkg_names):
        info = PACKAGES[name]
        is_selected = st.session_state.base_package == name

        with cols[i]:
            card_class = "pkg-card selected" if is_selected else "pkg-card"
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

            st.markdown(f"<h3>{name}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='pkg-tagline'>{info['tagline']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='pkg-benefit'>{info['client_benefit']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='pkg-price'>${info['price']:,}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='pkg-includes'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.77rem; font-weight:600; color:#334155; margin-bottom:5px; letter-spacing:0.01em;'>YOU RECEIVE</div>", unsafe_allow_html=True)
            for item in info["includes"]:
                st.markdown(f"<div style='font-size:0.81rem; line-height:1.42; margin-bottom:2.5px; color:#334155;'>• {item}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            btn_label = "Selected" if is_selected else "Select this package"
            if st.button(
                btn_label,
                key=f"select_pkg_{i}",
                disabled=is_selected,
                use_container_width=True,
                type="primary" if not is_selected else "secondary",
            ):
                st.session_state.base_package = name
                st.rerun()

def render_addon_selection():
    """Premium, interactive add-on cards with full visual consistency and client value."""
    st.markdown('<div class="section-header">2. Add targeted enhancements (optional)</div>', unsafe_allow_html=True)
    st.caption("Select only what you need. Every add-on is priced as a one-time enhancement and can be discussed in more detail during scoping.")

    addon_names = list(ADDONS.keys())
    cols_per_row = 2

    for row_start in range(0, len(addon_names), cols_per_row):
        row_cols = st.columns(cols_per_row, gap="medium")
        for j, col in enumerate(row_cols):
            idx = row_start + j
            if idx >= len(addon_names):
                break
            name = addon_names[idx]
            info = ADDONS[name]
            key = get_addon_checkbox_key(name)

            with col:
                # Fully custom premium card (matches package card quality)
                st.markdown(f'<div class="addon-card">', unsafe_allow_html=True)

                # Small matching icon for the add-on
                addon_images = {
                    "Gender, Equity & Inclusion Focus": "images/gesi_focus.jpg",
                    "Donor-Ready Reporting Pack": "images/donor_reporting.jpg",
                    "Stakeholder Data Collection Tools": "images/data_collection.jpg",
                    "Executive Dashboard & Portal": "images/executive_dashboard.jpg",
                    "Learning Briefs & Knowledge Products": "images/learning_briefs.jpg",
                    "Team Capability Workshop": "images/team_workshop.jpg",
                }
                if name in addon_images:
                    st.image(addon_images[name], width=126)  # triple original size

                st.markdown(f"<div class='addon-title'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='addon-desc'>{info['desc']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='addon-value'>{info['client_value']}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='addon-price'>+ ${info['price']:,}</span>", unsafe_allow_html=True)

                st.checkbox(
                    "Add to my order",
                    key=key,
                    value=st.session_state.get(key, False),
                )
                st.markdown("</div>", unsafe_allow_html=True)

def render_project_details():
    """Short, respectful, relevant questions only."""
    st.markdown('<div class="section-header">3. Tell us a little about your project</div>', unsafe_allow_html=True)
    st.caption("This helps us prepare a precise proposal. We only ask what we genuinely need at this stage.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.text_input(
            "Project or Programme Name *",
            key="proj_name",
            placeholder="e.g. Sahel Resilience & Livelihoods Programme – Phase 2",
            help="The name your team and donors use for this work.",
        )
        st.text_input(
            "Organization Name",
            key="org_name",
            placeholder="e.g. Horizon Foundation or Ministry of Agriculture",
        )
        st.text_input(
            "Work Email *",
            key="contact_email",
            placeholder="you@yourorganization.org",
            help="Required for proposal delivery and scoping coordination. We never share your email.",
        )

    with col2:
        st.selectbox(
            "Primary Sector / Focus Area *",
            options=[""] + SECTORS,
            key="sector",
            index=0,
        )
        st.selectbox(
            "Expected Timeline",
            options=TIMELINE_OPTIONS,
            key="timeline",
            index=1,
        )
        st.number_input(
            "Rough number of people who will benefit",
            min_value=0,
            max_value=5000000,
            value=25000,
            step=5000,
            key="num_beneficiaries",
            help="Helps us understand scale. Approximate is fine.",
        )

    st.text_area(
        "Anything else we should know? (donor requirements, tight deadlines, existing data systems, geographic constraints, etc.)",
        key="notes",
        placeholder="Example: FCDO is the primary donor. We have baseline data from 2023. Strong preference for remote data collection in two conflict-affected regions. Need the evaluation to feed directly into a 2027 scale-up decision.",
        height=92,
        help="The more specific you are here, the better our initial proposal will be.",
    )


def render_sidebar_summary():
    with st.sidebar:
        st.markdown("### Your Live Estimate")
        st.caption("Updates instantly • Transparent pricing • No obligation")

        base = st.session_state.base_package
        addons = get_selected_addons()
        total = calculate_total(base, addons)

        # Cleaner, more executive base package block
        if base:
            st.markdown(
                f"""
                <div style="background:#f8fafc; border:1.25px solid #e2e8f0; border-radius:10px; padding:9px 12px; margin:6px 0 4px;">
                    <div style="font-size:0.68rem; color:#64748b; font-weight:600; letter-spacing:0.3px;">BASE PACKAGE</div>
                    <div style="font-weight:700; color:#0f172a; font-size:0.95rem; line-height:1.15; margin-top:1px;">{base}</div>
                    <div style="color:#0d9488; font-weight:700; font-size:0.88rem;">${PACKAGES[base]['price']:,}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Tighter enhancements list
        if addons:
            st.markdown("<div style='margin:4px 0 2px; font-size:0.82rem; font-weight:700; color:#334155;'>Enhancements</div>", unsafe_allow_html=True)
            for a in addons:
                st.markdown(f"<div style='font-size:0.82rem; line-height:1.35; margin-bottom:1px;'>• {a} <span style='color:#0d9488; font-weight:600;'>+${ADDONS[a]['price']:,}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:0.78rem; color:#64748b; margin:2px 0 4px;'>No enhancements selected</div>", unsafe_allow_html=True)

        # Stronger, more executive total block
        st.markdown("### Estimated Total Investment")
        st.markdown(
            f"""
            <div style="background: linear-gradient(145deg, #0f172a 0%, #0a1322 100%); border:1px solid rgba(15,23,42,0.08); padding:15px 18px; border-radius:12px; text-align:center; margin:8px 0 4px; box-shadow: 0 10px 22px -8px rgb(11 20 38 / 0.35);">
                <div style="font-size:0.66rem; color:#94a3b8; font-weight:700; letter-spacing:1.2px;">ONE-TIME PROFESSIONAL FEE</div>
                <div style="font-size:2.22rem; font-weight:800; color:white; margin-top:3px; letter-spacing:-1px;">${total:,} <span style="font-size:0.9rem; font-weight:600; color:#cbd5e1;">USD</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='font-size:0.72rem; color:#64748b; margin-bottom:8px;'>Final pricing confirmed after scoping call.</div>", unsafe_allow_html=True)

        # More prominent, trustworthy primary CTA in the sidebar
        if st.button("Request My Proposal", type="primary", use_container_width=True):
            # CRITICAL: Validate first. Only save to Sheets after the snapshot succeeds.
            success = capture_proposal_snapshot()
            if success:
                try:
                    save_order_to_sheet({
                        "project_name": st.session_state.get("proj_name", ""),
                        "organization": st.session_state.get("org_name", ""),
                        "email": st.session_state.get("contact_email", ""),
                        "package": st.session_state.get("base_package", ""),
                        "addons": ", ".join(get_selected_addons()),
                        "timeline": st.session_state.get("timeline", ""),
                        "beneficiaries": st.session_state.get("num_beneficiaries", ""),
                        "notes": st.session_state.get("notes", ""),
                        "total_price": total
                    })
                except SheetsConfigurationError as e:
                    st.session_state.submit_error = str(e)
                st.rerun()

        if st.session_state.submit_error:
            st.error(st.session_state.submit_error)

        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        if st.button("Start Over — Clear Everything", use_container_width=True, type="secondary"):
            clear_all_selections()
            st.rerun()

def render_config_interface():
    """Main client flow with generous premium spacing."""
    render_top_bar()
    render_hero()
    render_trust_bar()

    render_package_selection()
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    render_addon_selection()
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    render_project_details()

   
    st.markdown(
        "<div class='premium-note'>Your selections update live in the sidebar. All information stays private in this browser session.</div>",
        unsafe_allow_html=True,
    )

def render_proposal_screen():
    """Clean, professional confirmation screen after successful submission.

    The order has already been saved to Google Sheets.
    We show a simple, reassuring thank-you message and next steps.
    The heavy manual copy flow has been removed per the new requirements.
    """
    data = st.session_state.proposal_data
    if not data:
        st.error("No proposal data found.")
        if st.button("Start a New Request"):
            clear_all_selections()
            st.rerun()
        return

    # We still generate the text so the Download button works
    proposal_text = generate_proposal_text(data)

    # Clean, calm success message
    st.success("Thank you. Your request has been received.")

    # Clean success graphic for emotional reassurance
    st.image("images/confirmation_success.jpg", width=120)  # increased for better visibility

    st.markdown(
        """
        <div style="max-width: 620px; margin: 1.2rem auto 0.6rem; text-align: center;">
            <h2 style="font-size: 1.72rem; color: #0f172a; margin-bottom: 0.55rem; font-weight: 800;">
                We've received your MERL request.
            </h2>
            <p style="font-size: 1.08rem; color: #334155; line-height: 1.55; max-width: 560px; margin: 0 auto;">
                Altamont Group will review your submission and contact you within 
                <strong>one business day</strong> to schedule a short scoping conversation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Light recap so the client feels heard (kept deliberately compact)
    st.markdown(
        f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; 
                    padding:14px 18px; max-width: 580px; margin: 1.1rem auto 1.4rem; text-align:center;">
            <span style="color:#475569; font-size:0.93rem;">
                <strong>Submitted:</strong> {data['base_package']} — ${data['total']:,} USD
            </span><br>
            <span style="color:#64748b; font-size:0.82rem;">
                A copy has been saved for your records (download below).
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Secondary actions — Download + Edit (kept as options, not the main story)
    c1, c2 = st.columns([1.35, 1.35])
    with c1:
        st.download_button(
            label="Download Proposal (.txt)",
            data=proposal_text,
            file_name=f"{data['proposal_id']}_Altamont_MERL_Proposal.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download a copy for your records",
        )
    with c2:
        if st.button("Edit My Selections", type="secondary", use_container_width=True):
            st.session_state.order_submitted = False
            st.rerun()

    st.markdown(
        "<div style='text-align:center; margin-top: 2.1rem; font-size:0.82rem; color:#64748b;'>"
        "Questions? Email <strong>zs@altamontgroup.ca</strong> or visit <strong>altamontgroup.ca</strong>"
        "</div>",
        unsafe_allow_html=True,
    )

# ============================================================================
# MAIN
# ============================================================================

def main():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()
    inject_custom_css()

    if st.session_state.order_submitted and st.session_state.proposal_data:
        render_proposal_screen()
    else:
        render_config_interface()
        render_sidebar_summary()

if __name__ == "__main__":
    main()
