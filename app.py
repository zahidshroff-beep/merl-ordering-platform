
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random
import html

# ==================== GOOGLE SHEETS SETUP (Safe for both local + Cloud) ====================
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    if "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], 
            scopes=SCOPE
        )
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
except Exception:
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)

client = gspread.authorize(creds)

SHEET_NAME = "MERL Orders - Module 2"
sheet = client.open(SHEET_NAME).sheet1

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

SECTORS = [
    "Global Health & Nutrition",
    "Education & Youth Development",
    "Agriculture, Food Security & Livelihoods",
    "Climate Resilience & Environment",
    "Democratic Governance & Accountability",
    "Economic Development & Private Sector",
    "Humanitarian Response & Protection",
    "Water, Sanitation & Hygiene (WASH)",
    "Gender Equality & Social Inclusion",
    "Other / Multiple Sectors"
]

TIMELINE_OPTIONS = [
    "1–3 months (rapid or focused scope)",
    "3–6 months (standard engagement)",
    "6–12 months (multi-phase or complex)",
    "12+ months (long-term partnership)"
]

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
        key = f"cb_{name.replace(' ', '_').replace('&', 'and').replace(',', '')}"
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
        key = f"cb_{name.replace(' ', '_').replace('&', 'and').replace(',', '')}"
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
    selected = []
    for name in ADDONS.keys():
        key = f"cb_{name.replace(' ', '_').replace('&', 'and').replace(',', '')}"
        if st.session_state.get(key, False):
            selected.append(name)
    return selected

def calculate_total(base_package, selected_addons):
    if not base_package or base_package not in PACKAGES:
        return 0
    total = PACKAGES[base_package]["price"]
    for addon in selected_addons:
        if addon in ADDONS:
            total += ADDONS[addon]["price"]
    return total
def save_order_to_sheet(data):
    """Save order to Google Sheet"""
    try:
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("project_name", ""),
            data.get("organization", ""),
            data.get("email", ""),
            data.get("package", ""),
            data.get("addons", ""),
            data.get("timeline", ""),
            data.get("beneficiaries", ""),
            data.get("notes", ""),
            data.get("total_price", "")
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Failed to save order: {e}")
        return False

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

def validate_order(base_package, details, selected_addons):
    if not base_package:
        return False, "Please select one of the three starting packages above."
    if not details.get("project_name"):
        return False, "Project or program name is required so we can prepare your proposal accurately."
    if not details.get("sector"):
        return False, "Please select the primary sector or focus area."
    email = (details.get("email") or "").strip()
    if not email:
        return False, "Your work email is required so we can send your custom proposal and schedule a scoping call."
    # Basic email sanity check
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Please enter a valid work email address (e.g. you@yourorganization.org)."
    return True, None


def capture_proposal_snapshot():
    base = st.session_state.get("base_package")
    addons = get_selected_addons()
    total = calculate_total(base, addons) if base else 0
    details = get_current_form_values()

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

    /* HERO — significantly more premium, breathing room, modern presence */
    .hero-section {{
        text-align: center;
        padding: 3.15rem 2.6rem 2.75rem;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 28px;
        border: 1px solid var(--border);
        margin-bottom: 1.85rem;
        box-shadow: 0 35px 70px -18px rgb(15 23 42 / 0.10), 0 18px 30px -12px rgb(15 23 42 / 0.06);
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
        font-size: 2.84rem;
        line-height: 1.03;
        font-weight: 700;
        color: var(--navy);
        margin-bottom: 0.52rem;
        letter-spacing: -0.78px;
    }}
    
    .hero-sub {{
        font-size: 1.05rem;
        color: var(--muted);
        max-width: 680px;
        margin: 0 auto 1.35rem;
        line-height: 1.65;
    }}

    /* Trust bar — elegant, elevated credibility */
    .trust-card {{
        background: white;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 16px 13px 14px;
        text-align: center;
        box-shadow: 0 6px 18px -5px rgb(15 23 42 / 0.06);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .trust-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 16px 28px -8px rgb(15 23 42 / 0.10);
        border-color: #cbd5e1;
    }}
    .trust-num {{
        font-size: 1.56rem;
        font-weight: 700;
        color: var(--teal);
        line-height: 1.0;
        letter-spacing: -0.42px;
    }}

    /* Premium section headers */
    .section-header {{
        font-size: 1.19rem;
        font-weight: 700;
        color: var(--navy);
        margin: 2.25rem 0 0.52rem;
        padding-bottom: 10px;
        letter-spacing: -0.3px;
        display: flex;
        align-items: center;
        gap: 15px;
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

    /* PREMIUM Package cards — luxurious depth, refined selection, generous spacing */
    .pkg-card {{
        background: white;
        border: 1.5px solid var(--border);
        border-radius: 22px;
        padding: 28px 26px 24px;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 8px 20px -6px rgb(15 23 42 / 0.08), 0 4px 8px -3px rgb(15 23 42 / 0.05);
        position: relative;
        display: flex;
        flex-direction: column;
    }}
    .pkg-card:hover {{
        border-color: #cbd5e1;
        box-shadow: 0 18px 35px -10px rgb(15 23 42 / 0.11), 0 8px 14px -4px rgb(15 23 42 / 0.06);
        transform: translateY(-3px);
    }}
    .pkg-card.selected {{
        border-color: var(--teal);
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
        box-shadow: 0 26px 42px -12px rgb(13 148 136 / 0.20), 0 14px 18px -7px rgb(13 148 136 / 0.12);
        transform: translateY(-5px);
    }}
    .pkg-card.selected::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: linear-gradient(to right, var(--teal), var(--teal-soft));
        border-radius: 22px 22px 0 0;
    }}
    .pkg-card.selected::after {{
        content: "SELECTED";
        position: absolute;
        top: 19px;
        right: 20px;
        background: var(--teal);
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 1.25px;
        padding: 3px 10px 2px;
        border-radius: 999px;
        box-shadow: 0 2px 4px rgb(13 148 136 / 0.25);
    }}
    .pkg-card h3 {{
        margin: 0 0 4px 0;
        font-size: 1.26rem;
        font-weight: 700;
        color: var(--navy);
        letter-spacing: -0.32px;
    }}
    .pkg-tagline {{
        font-size: 0.79rem;
        color: var(--teal);
        font-weight: 700;
        letter-spacing: 0.2px;
        margin-bottom: 13px;
        text-transform: uppercase;
    }}
    .pkg-benefit {{
        font-size: 0.93rem;
        line-height: 1.55;
        color: var(--text);
        margin-bottom: 16px;
        min-height: 78px;
        flex: 1;
    }}
    .pkg-price {{
        font-size: 2.18rem;
        font-weight: 700;
        color: var(--teal);
        margin: 2px 0 2px;
        letter-spacing: -0.65px;
        line-height: 1;
    }}
    .pkg-price small {{
        font-size: 0.68rem;
        font-weight: 500;
        color: #64748b;
        letter-spacing: normal;
    }}
    .pkg-includes {{
        margin-top: 4px;
        padding-top: 10px;
        border-top: 1px solid var(--border);
    }}

    /* Premium Add-on cards — fully realized, interactive, consistent with packages */
    .addon-card {{
        background: white;
        border: 1.25px solid var(--border);
        border-radius: 18px;
        padding: 18px 19px 16px;
        height: 100%;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px -3px rgb(15 23 42 / 0.05);
        display: flex;
        flex-direction: column;
    }}
    .addon-card:hover {{
        border-color: #94a3b8;
        box-shadow: 0 16px 26px -8px rgb(15 23 42 / 0.10);
        transform: translateY(-2px);
    }}
    .addon-card .stCheckbox {{
        margin-top: auto;
        padding-top: 8px;
    }}
    .addon-title {{
        font-weight: 700;
        font-size: 0.97rem;
        color: var(--navy);
        margin-bottom: 5px;
        letter-spacing: -0.14px;
        line-height: 1.3;
    }}
    .addon-desc {{
        font-size: 0.83rem;
        color: var(--muted);
        line-height: 1.52;
        margin-bottom: 7px;
        flex: 1;
        min-height: 46px;
    }}
    .addon-value {{
        font-size: 0.79rem;
        font-style: italic;
        color: var(--teal);
        margin-bottom: 7px;
        line-height: 1.38;
    }}
    .addon-price {{
        color: var(--teal-soft);
        font-weight: 700;
        font-size: 1.04rem;
        letter-spacing: -0.2px;
        display: block;
        margin-bottom: 2px;
    }}

    /* Sidebar total — executive, clean, trustworthy */
    .sidebar-total {{
        background: linear-gradient(155deg, var(--navy) 0%, #0a1322 100%);
        color: white !important;
        padding: 21px 24px 19px;
        border-radius: 18px;
        text-align: center;
        margin: 16px 0 10px;
        box-shadow: 0 16px 32px -10px rgb(11 20 38 / 0.42);
        border: 1px solid rgba(255,255,255,0.06);
    }}
    .sidebar-total .label {{
        font-size: 0.66rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        font-weight: 600;
        color: white !important;
    }}
    .sidebar-total .amount {{
        font-size: 2.36rem;
        font-weight: 700;
        line-height: 1.0;
        margin-top: 3px;
        letter-spacing: -0.78px;
        color: white !important;
    }}
    .sidebar-total > div:last-child {{
        color: rgba(255,255,255,0.78) !important;
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

    /* Premium buttons — stronger presence, modern interaction */
    .stButton > button {{
        border-radius: 14px;
        font-weight: 700;
        padding: 0.68rem 1.7rem;
        letter-spacing: 0.2px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.94rem;
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(160deg, var(--teal) 0%, var(--teal-soft) 100%);
        border-color: var(--teal);
        box-shadow: 0 10px 24px -6px rgb(13 148 136 / 0.42);
        color: white !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-2.5px);
        box-shadow: 0 16px 30px -7px rgb(13 148 136 / 0.48);
        background: linear-gradient(160deg, var(--teal-soft) 0%, var(--teal) 100%);
    }}
    .stButton > button[kind="secondary"] {{
        border: 1.75px solid var(--border);
        background: white;
        color: var(--navy);
    }}
    .stButton > button[kind="secondary"]:hover {{
        background: #f8fafc;
        border-color: #94a3b8;
        transform: translateY(-1px);
    }}

    /* The example loader gets extra visual weight from placement + emoji label in hero */

    /* Strong email action panel on proposal — clear next step */
    .email-action-panel {{
        background: linear-gradient(180deg, #f0fdfa 0%, #ecfdf5 100%);
        border: 2px solid #14b8a6;
        border-radius: 20px;
        padding: 26px 32px;
        margin: 1.05rem 0 1.4rem;
        box-shadow: 0 14px 28px -9px rgb(13 148 136 / 0.14);
    }}
    .email-action-panel .instruction {{
        font-size: 0.97rem;
        color: #0f766e;
        line-height: 1.52;
        margin-bottom: 14px;
        font-weight: 500;
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
        margin: 1.2rem 0 !important;
    }}
    .stSuccess {{
        border-radius: 14px;
        border-left: 5px solid var(--teal);
    }}
    .stExpander {{
        border-radius: 14px !important;
    }}
    
    /* Better column & container breathing */
    .stColumn > div {{
        gap: 0.35rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# RENDER FUNCTIONS
# ============================================================================

def render_top_bar():
    """Ultra-premium header bar with elevated executive presence."""
    col_logo, col_text, col_spacer = st.columns([0.95, 5.4, 0.9])
    
    with col_logo:
        try:
            st.image(LOGO_PATH, width=132)
        except Exception:
            st.markdown(f"<span style='font-size:1.08rem; font-weight:700; color:{PRIMARY_NAVY};'>ALTAMONT GROUP</span>", unsafe_allow_html=True)
    
    with col_text:
        st.markdown(
            f"""
            <div style="padding-top:1px;">
                <span style="font-size:1.58rem; font-weight:700; color:{PRIMARY_NAVY}; letter-spacing:-0.42px;">Altamont Group</span><br>
                <span style="font-size:0.82rem; color:{TEXT_MUTED}; font-weight:500; letter-spacing:-0.01em;">Strategic advisory for measurable impact &nbsp;•&nbsp; Global reach, boutique precision</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""<div style="height:1px; background:linear-gradient(to right, transparent, {CARD_BORDER}, transparent); margin:13px 0 20px 0;"></div>""",
        unsafe_allow_html=True,
    )

def render_hero():
    """Premium, high-impact hero with prominent, attractive example loader."""
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
            key = f"cb_{name.replace(' ', '_').replace('&', 'and').replace(',', '')}"

            with col:
                # Fully custom premium card (matches package card quality)
                st.markdown(f'<div class="addon-card">', unsafe_allow_html=True)
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

if st.session_state.get("base_package"):
    st.markdown("### Your Order Summary")

    base = st.session_state.get("base_package")
    addons = get_selected_addons()
    total = calculate_total(base, addons) if base else 0

    if base:
        st.markdown(f"**Selected Package:** {base} — ${PACKAGES[base]['price']:,}")
    else:
        st.info("Please select a package above.")

    if addons:
        st.markdown("**Selected Enhancements:**")
        for a in addons:
            st.markdown(f"- {a} (+${ADDONS[a]['price']:,})")
    else:
        st.caption("No enhancements selected.")

    st.markdown(f"### Total Estimated Investment: **${total:,} USD**")
    st.caption("One-time professional fee. Final pricing confirmed after scoping call.")

    st.markdown("---")

    if st.button("Request My Proposal", type="primary", use_container_width=True):
        save_order_to_sheet({
            "project_name": st.session_state.get("proj_name", ""),
            "organization": st.session_state.get("org_name", ""),
            "email": st.session_state.get("contact_email", ""),
            "package": base,
            "addons": ", ".join(addons),
            "timeline": st.session_state.get("timeline", ""),
            "beneficiaries": st.session_state.get("num_beneficiaries", ""),
            "notes": st.session_state.get("notes", ""),
            "total_price": total
        })
        success = capture_proposal_snapshot()
        if success:
            st.rerun()

    if st.session_state.get("submit_error"):
        st.error(st.session_state.submit_error)

    st.markdown("---")

    if st.button("Start Over — Clear Everything", use_container_width=True, type="secondary"):
        clear_all_selections()
        st.rerun()

def render_proposal_screen():
    """Premium, client-ready Proposal Summary screen.
    Major improvements:
    - Prominent 'Copy Proposal & Send to Altamont Group' as the primary action.
    - Clear, explicit instruction for pasting into email to zs@altamontgroup.ca.
    - Significantly more polished, trustworthy document presentation.
    - Easy secondary actions (download, start over).
    """
    data = st.session_state.proposal_data
    if not data:
        st.error("No proposal data found.")
        if st.button("Start a New Request"):
            clear_all_selections()
            st.rerun()
        return

    proposal_text = generate_proposal_text(data)

    # Gentle confirmation banner when arriving at the summary (improves perceived completion)
    st.success("Proposal generated successfully. Review the details below, then copy or download to send to Altamont Group.")

    st.markdown('<div class="proposal-container">', unsafe_allow_html=True)

    # === Top brand row with logo (more refined) ===
    logo_col, info_col = st.columns([0.85, 5.4])
    with logo_col:
        try:
            st.image(LOGO_PATH, width=112)
        except Exception:
            st.markdown(f"<span style='font-weight:700; color:{PRIMARY_NAVY}; font-size:1.08rem;'>ALTAMONT</span>", unsafe_allow_html=True)
    with info_col:
        st.markdown(
            f"""
            <div style="padding-top:1px;">
                <span style="font-size:1.44rem; font-weight:700; color:{PRIMARY_NAVY}; letter-spacing:-0.36px;">ALTAMONT GROUP</span><br>
                <span style="font-size:0.81rem; color:{TEXT_MUTED};">Strategic Advisory for Measurable Impact  •  www.altamontgroup.ca</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Professional proposal header banner — elevated document header
    banner_html = f"""
<div style="
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 12px 0 24px 0;
">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
        <div>
            <div style="font-size:0.7rem; letter-spacing:1.5px; color:#64748b; margin-bottom:6px;">CONFIDENTIAL CLIENT PROPOSAL</div>
            <div style="font-size:1.6rem; font-weight:700; color:#0f172a; line-height:1.1;">{data['proposal_id']}</div>
        </div>
        <div style="text-align:right; font-size:0.85rem; color:#475569; line-height:1.4;">
            <div>Prepared {data['submitted_at']}</div>
            <div style="margin-top:2px;">Altamont Group • Professional MERL Advisory</div>
        </div>
    </div>
</div>
"""

    st.markdown(banner_html, unsafe_allow_html=True)

    # === PRIMARY EMAIL ACTION — clear, high-priority document action ===
    st.markdown(
        f"""
        <div class="email-action-panel">
            <div style="font-weight:700; font-size:1.06rem; color:#0f766e; margin-bottom:5px;">
                Your proposal is ready to send.
            </div>
            <div class="instruction">
                <strong>Click the button below to copy this proposal, then paste it into an email to zs@altamontgroup.ca.</strong><br>
                We typically respond within one business day with a calendar link for your 30-minute scoping call.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hidden source element holding the clean proposal text.
    # This enables a robust copy button that never embeds user content in JS attributes,
    # preventing any HTML/JS leakage into the page even if proposal text contains quotes,
    # backticks, $, newlines, or other special characters.
    st.markdown(
        f'<div id="proposal-text-source" style="display:none; white-space:pre;">{html.escape(proposal_text)}</div>',
        unsafe_allow_html=True,
    )

    # Three action buttons — primary copy dominates, others secondary but clear
    col_copy, col_dl, col_back = st.columns([2.15, 1.3, 1.2], gap="medium")

    with col_copy:
        st.markdown(
            f"""
            <button onclick="
                (function(btn){{
                    const src = document.getElementById('proposal-text-source');
                    const txt = src ? (src.textContent || src.innerText || '') : '';
                    if (!txt) {{
                        alert('Nothing to copy.');
                        return;
                    }}
                    navigator.clipboard.writeText(txt).then(() => {{
                        const orig = btn.innerHTML;
                        btn.innerHTML = '✓ Copied — now email to zs@altamontgroup.ca';
                        btn.style.background = '#14532d';
                        setTimeout(() => {{
                            btn.innerHTML = orig;
                            btn.style.background = 'linear-gradient(155deg, #166534 0%, #14532d 100%)';
                        }}, 3200);
                    }}).catch(() => {{
                        alert('Copy failed. Please select the full text below and press Ctrl/Cmd + C.');
                    }});
                }})(this);
            " style="
                width: 100%;
                background: linear-gradient(155deg, #166534 0%, #14532d 100%);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 17px 18px;
                font-size: 0.99rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 12px 26px -7px rgb(21 128 61 / 0.42);
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                letter-spacing: 0.18px;
            ">Copy Proposal &amp; Send to Altamont Group</button>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align:center; font-size:0.75rem; color:#166534; margin-top:5px; font-weight:600;'>One-click copy • Paste into your email client</div>",
            unsafe_allow_html=True,
        )

    with col_dl:
        st.download_button(
            label="Download .txt",
            data=proposal_text,
            file_name=f"{data['proposal_id']}_Altamont_MERL_Proposal.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download the full proposal text for your records or to attach to email",
        )

    with col_back:
        if st.button("Edit My Selections", type="secondary", use_container_width=True, help="Return to the configurator to adjust package, add-ons, or details"):
            st.session_state.order_submitted = False
            st.rerun()

    st.divider()

    # === Two-column clean summary — document-quality review area ===
    st.markdown('<div style="background:#fafbfc; border:1px solid #e2e8f0; border-radius:18px; padding:22px 24px 18px; margin:6px 0 4px;">', unsafe_allow_html=True)
    left, right = st.columns([1.08, 1], gap="large")

    with left:
        st.markdown("#### Selected Engagement")
        st.markdown(f"**{data['base_package']}** — ${data['base_price']:,} USD")
        st.caption(data['base_tagline'])

        with st.expander("What you receive", expanded=True):
            for item in data["base_includes"]:
                st.markdown(f"• {item}")

        st.markdown(
            f"<div style='font-size:0.87rem; background:#f0fdfa; padding:12px 15px; border-radius:12px; border:1px solid #99f6e4; margin-top:10px;'><strong>Why this matters for you:</strong> {data['base_benefit']}</div>",
            unsafe_allow_html=True,
        )

        if data["addons"]:
            st.markdown("#### Selected Enhancements")
            for addon in data["addons"]:
                price = data["addon_prices"].get(addon, 0)
                value = data["addon_values"].get(addon, "")
                st.markdown(f"**{addon}** — +${price:,}")
                if value:
                    st.caption(value)
        else:
            st.markdown("#### Enhancements")
            st.caption("None selected")

        st.markdown("#### Total Estimated Investment")
        st.markdown(
            f"<span style='font-size:2.22rem; font-weight:700; color:{ACCENT_TEAL};'>${data['total']:,}</span> <span style='color:#64748b; font-size:0.92rem;'>USD</span>",
            unsafe_allow_html=True,
        )
        st.caption("One-time professional services fee. Final quote after scoping call.")

    with right:
        st.markdown("#### Project Context")
        d = data["details"]

        scope_bits = []
        if d.get("project_name"):
            scope_bits.append(f"<strong>{html.escape(d['project_name'])}</strong>")
        if d.get("sector"):
            scope_bits.append(f"<strong>{html.escape(d['sector'])}</strong> sector")
        if d.get("timeline"):
            scope_bits.append(f"Timeline: <strong>{html.escape(d['timeline'])}</strong>")
        if d.get("num_beneficiaries"):
            scope_bits.append(f"~<strong>{d['num_beneficiaries']:,}</strong> beneficiaries")

        scope_html = "  •  ".join(scope_bits) if scope_bits else "Details captured for scoping."
        st.markdown(f"<div class='scope-section'>{scope_html}</div>", unsafe_allow_html=True)

        if d.get("organization"):
            st.markdown(f"**Organization:** {d['organization']}")
        if d.get("email"):
            st.markdown(f"**Contact email:** {d['email']}")

        if d.get("notes"):
            st.markdown("**Additional notes captured:**")
            st.info(d["notes"])

        st.markdown("#### What Happens Next")
        st.markdown(
            """
            <div class="next-steps-box">
            <ol>
                <li><strong>Copy &amp; email</strong> the proposal to <strong>zs@altamontgroup.ca</strong></li>
                <li><strong>Review (1 business day)</strong> — we prepare questions or clarifications</li>
                <li><strong>30-min scoping call</strong> — refine scope, timeline, and deliverables together</li>
                <li><strong>Formal SOW + quote</strong> — delivered within 48 hours</li>
                <li><strong>Kickoff</strong> — work begins promptly once signed</li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div style='font-size:0.78rem; color:{TEXT_MUTED}; margin-top:8px;'>This estimate is valid for 30 days. We can adjust scope to match your budget or timeline.</div>",
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)  # close document-quality review wrapper

    # === Full text for manual review / copy fallback ===
    st.divider()
    with st.expander("View full proposal text (for manual copy or records)", expanded=False):
        st.text_area(
            "Full proposal content",
            value=proposal_text,
            height=440,
            key="proposal_text_view",
            label_visibility="collapsed",
        )
        st.caption("Select all (Ctrl/Cmd+A) and copy manually if the button above does not work in your browser.")

    st.markdown(
        "<div style='text-align:center; margin-top:16px; font-size:0.78rem; color:#64748b;'>"
        "Questions? Email <strong>zs@altamontgroup.ca</strong> or visit <strong>altamontgroup.ca</strong>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()
