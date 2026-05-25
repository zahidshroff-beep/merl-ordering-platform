"""
MERL Order — Client-Centric Edition
Professional, premium proposal configurator for NGOs, foundations, and donor-funded programs.
Branded for Altamont Group. Built from the client's perspective: clarity, convenience, low risk, professionalism.
"""

import streamlit as st
from datetime import datetime
import random

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
    }}
    
    /* Global premium typography */
    h1, h2, h3, h4, h5 {{
        color: var(--navy);
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 700;
        letter-spacing: -0.025em;
    }}
    
    .stMarkdown p, .stMarkdown li, .stMarkdown div, .stMarkdown span {{
        color: var(--text);
        font-size: 0.95rem;
        line-height: 1.68;
    }}

    /* Refined inputs with premium focus rings */
    .stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {{
        border: 1.5px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 11px 15px !important;
        font-size: 0.96rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        background: var(--white) !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {{
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 5px rgba(15, 118, 110, 0.10) !important;
        outline: none !important;
    }}
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {{
        font-weight: 600 !important;
        color: var(--navy) !important;
        font-size: 0.88rem !important;
        margin-bottom: 7px !important;
        letter-spacing: -0.01em;
    }}

    /* Top brand header - elevated executive feel */
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

    /* Hero - significantly more premium and impactful */
    .hero-section {{
        text-align: center;
        padding: 2.9rem 2.25rem 2.55rem;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 28px;
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        box-shadow: 0 30px 60px -15px rgb(15 23 42 / 0.09), 0 15px 25px -10px rgb(15 23 42 / 0.05);
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
        font-size: 2.72rem;
        line-height: 1.05;
        font-weight: 700;
        color: var(--navy);
        margin-bottom: 0.55rem;
        letter-spacing: -0.72px;
    }}
    
    .hero-sub {{
        font-size: 1.06rem;
        color: var(--muted);
        max-width: 660px;
        margin: 0 auto 1.25rem;
        line-height: 1.62;
    }}

    /* Trust bar - refined, more elegant */
    .trust-card {{
        background: white;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 15px 12px 13px;
        text-align: center;
        box-shadow: 0 6px 16px -4px rgb(15 23 42 / 0.06);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .trust-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 14px 25px -6px rgb(15 23 42 / 0.09);
        border-color: #cbd5e1;
    }}
    .trust-num {{
        font-size: 1.52rem;
        font-weight: 700;
        color: var(--teal);
        line-height: 1.0;
        letter-spacing: -0.4px;
    }}

    /* Premium section headers with refined accent */
    .section-header {{
        font-size: 1.18rem;
        font-weight: 700;
        color: var(--navy);
        margin: 2.1rem 0 0.55rem;
        padding-bottom: 9px;
        letter-spacing: -0.28px;
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .section-header::before {{
        content: "";
        display: inline-block;
        width: 32px;
        height: 3.5px;
        background: linear-gradient(to right, var(--teal), var(--teal-soft));
        border-radius: 4px;
    }}
    .section-caption {{
        color: var(--muted);
        font-size: 0.91rem;
        margin-bottom: 1.05rem;
        line-height: 1.52;
    }}

    /* SIGNIFICANTLY IMPROVED Package cards - luxurious, clear selection */
    .pkg-card {{
        background: white;
        border: 1.75px solid var(--border);
        border-radius: 22px;
        padding: 26px 24px 22px;
        height: 100%;
        transition: all 0.28s cubic-bezier(0.4, 0.0, 0.2, 1);
        box-shadow: 0 6px 16px -4px rgb(15 23 42 / 0.07), 0 3px 6px -2px rgb(15 23 42 / 0.04);
        position: relative;
    }}
    .pkg-card.selected {{
        border-color: var(--teal);
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
        box-shadow: 0 22px 35px -10px rgb(13 148 136 / 0.18), 0 12px 14px -6px rgb(13 148 136 / 0.10);
        transform: translateY(-4px);
    }}
    .pkg-card.selected::after {{
        content: "SELECTED";
        position: absolute;
        top: 16px;
        right: 18px;
        background: var(--teal);
        color: white;
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 1.1px;
        padding: 2px 9px 1px;
        border-radius: 999px;
    }}
    .pkg-card h3 {{
        margin: 0 0 5px 0;
        font-size: 1.24rem;
        font-weight: 700;
        color: var(--navy);
        letter-spacing: -0.3px;
    }}
    .pkg-tagline {{
        font-size: 0.81rem;
        color: var(--teal);
        font-weight: 700;
        letter-spacing: 0.18px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }}
    .pkg-benefit {{
        font-size: 0.93rem;
        line-height: 1.52;
        color: var(--text);
        margin-bottom: 15px;
        min-height: 82px;
    }}
    .pkg-price {{
        font-size: 2.12rem;
        font-weight: 700;
        color: var(--teal);
        margin: 4px 0 3px;
        letter-spacing: -0.6px;
        line-height: 1;
    }}
    .pkg-price small {{
        font-size: 0.7rem;
        font-weight: 500;
        color: #64748b;
        letter-spacing: normal;
    }}

    /* Greatly improved Add-on cards - clean, trustworthy, interactive feel */
    .addon-card {{
        background: white;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 19px 20px 17px;
        height: 100%;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .addon-card:hover {{
        border-color: #94a3b8;
        box-shadow: 0 14px 24px -8px rgb(15 23 42 / 0.08);
    }}
    .addon-title {{
        font-weight: 700;
        font-size: 0.98rem;
        color: var(--navy);
        margin-bottom: 4px;
        letter-spacing: -0.15px;
    }}
    .addon-desc {{
        font-size: 0.84rem;
        color: var(--muted);
        line-height: 1.5;
        margin-bottom: 8px;
        min-height: 54px;
    }}
    .addon-value {{
        font-size: 0.8rem;
        font-style: italic;
        color: var(--teal);
        margin-bottom: 6px;
        line-height: 1.35;
    }}
    .addon-price {{
        color: var(--teal-soft);
        font-weight: 700;
        font-size: 1.02rem;
        letter-spacing: -0.2px;
    }}

    /* Sidebar total - executive dark card */
    .sidebar-total {{
        background: linear-gradient(160deg, var(--navy) 0%, #0b1426 100%);
        color: white;
        padding: 20px 22px;
        border-radius: 18px;
        text-align: center;
        margin: 18px 0 12px;
        box-shadow: 0 14px 28px -8px rgb(11 20 38 / 0.38);
    }}
    .sidebar-total .label {{
        font-size: 0.68rem;
        opacity: 0.78;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-weight: 600;
    }}
    .sidebar-total .amount {{
        font-size: 2.28rem;
        font-weight: 700;
        line-height: 1.0;
        margin-top: 2px;
        letter-spacing: -0.7px;
    }}

    /* Proposal screen - document quality */
    .proposal-container {{
        max-width: 1080px;
        margin: 0 auto;
        padding-bottom: 2rem;
    }}
    .proposal-banner {{
        background: linear-gradient(135deg, var(--navy) 0%, #1e2937 100%);
        color: white;
        padding: 26px 34px;
        border-radius: 20px;
        margin: 12px 0 24px;
        box-shadow: 0 20px 40px -12px rgb(15 23 42 / 0.32);
    }}
    .scope-section {{
        background: #f8fafc;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 6px rgb(15 23 42 / 0.025);
        font-size: 0.94rem;
        line-height: 1.55;
    }}
    .next-steps-box {{
        background: #f0fdfa;
        border-left: 7px solid var(--teal);
        padding: 18px 22px;
        border-radius: 14px;
        margin: 0.95rem 0;
    }}
    .next-steps-box ol {{
        margin: 10px 0 0 18px;
        padding: 0;
    }}
    .next-steps-box li {{
        margin-bottom: 6px;
        line-height: 1.52;
        font-size: 0.93rem;
    }}

    /* Prominent final CTA zone after form - now much stronger */
    .submit-cta {{
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 2.5px solid var(--teal);
        border-radius: 24px;
        padding: 30px 36px 28px;
        margin: 2.1rem 0 0.6rem;
        text-align: center;
        box-shadow: 0 25px 40px -15px rgb(13 148 136 / 0.13), 0 12px 14px -6px rgb(13 148 136 / 0.07);
    }}
    .submit-cta h3 {{
        font-size: 1.42rem;
        margin: 0 0 8px;
        color: var(--navy);
        letter-spacing: -0.3px;
    }}
    .submit-cta p {{
        color: var(--muted);
        max-width: 560px;
        margin: 0 auto 20px;
        font-size: 0.96rem;
        line-height: 1.58;
    }}

    /* Premium primary buttons */
    .stButton > button {{
        border-radius: 14px;
        font-weight: 700;
        padding: 0.65rem 1.55rem;
        letter-spacing: 0.18px;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(155deg, var(--teal) 0%, var(--teal-soft) 100%);
        border-color: var(--teal);
        box-shadow: 0 8px 20px -5px rgb(13 148 136 / 0.38);
        color: white !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 14px 26px -6px rgb(13 148 136 / 0.42);
        background: linear-gradient(155deg, var(--teal-soft) 0%, var(--teal) 100%);
    }}
    .stButton > button[kind="secondary"] {{
        border: 1.75px solid var(--border);
        background: white;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background: #f8fafc;
        border-color: #94a3b8;
    }}

    /* Strong email action panel on proposal */
    .email-action-panel {{
        background: linear-gradient(180deg, #f0fdfa 0%, #ecfdf5 100%);
        border: 2px solid #14b8a6;
        border-radius: 20px;
        padding: 26px 30px;
        margin: 1.1rem 0 1.35rem;
        box-shadow: 0 12px 25px -8px rgb(13 148 136 / 0.12);
    }}
    .email-action-panel .instruction {{
        font-size: 0.97rem;
        color: #0f766e;
        line-height: 1.5;
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
        font-size: 0.77rem;
        color: var(--muted);
    }}
    .premium-note {{
        font-size: 0.81rem;
        color: #64748b;
        text-align: center;
        margin-top: 1.55rem;
        letter-spacing: -0.1px;
    }}

    /* Minor Streamlit polish */
    .stDivider {{
        margin: 1.15rem 0 !important;
    }}
    .stSuccess {{
        border-radius: 14px;
        border-left: 5px solid var(--teal);
    }}
    .stExpander {{
        border-radius: 14px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# RENDER FUNCTIONS
# ============================================================================

def render_top_bar():
    """Premium, trustworthy header with prominent, high-visibility logo."""
    col_logo, col_text, col_spacer = st.columns([1.0, 5.1, 1.2])
    
    with col_logo:
        try:
            st.image(LOGO_PATH, width=138)
        except Exception:
            st.markdown(f"<span style='font-size:1.12rem; font-weight:700; color:{PRIMARY_NAVY};'>ALTAMONT GROUP</span>", unsafe_allow_html=True)
    
    with col_text:
        st.markdown(
            f"""
            <div style="padding-top: 3px;">
                <span style="font-size:1.52rem; font-weight:700; color:{PRIMARY_NAVY}; letter-spacing:-0.38px;">Altamont Group</span><br>
                <span style="font-size:0.84rem; color:{TEXT_MUTED}; font-weight:500;">Strategic advisory for measurable impact • Global reach, boutique attention</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""<div style="height:1px; background:{CARD_BORDER}; margin:14px 0 18px 0;"></div>""",
        unsafe_allow_html=True,
    )

def render_hero():
    """Strong, client-centric opening with premium presence."""
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

    # Centered example loader — secondary but easy to find
    c1, c2, c3 = st.columns([1.15, 2.3, 1.15])
    with c2:
        if st.button(
            "Load a realistic foundation example",
            type="secondary",
            use_container_width=True,
            help="See a complete, high-quality order that a real foundation might submit",
        ):
            load_example_order()
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:0.35rem;">
            <span class="small-muted">Typical turnaround: proposal in your inbox within 48 hours • Clear next steps always provided</span>
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
            st.markdown("<div style='font-size:0.78rem; font-weight:600; color:#334155; margin:6px 0 4px;'>You receive:</div>", unsafe_allow_html=True)

            for item in info["includes"]:
                st.markdown(f"<div style='font-size:0.82rem; line-height:1.38; margin-bottom:2px;'>• {item}</div>", unsafe_allow_html=True)

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
    """Clean, transparent add-ons with client value."""
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
                with st.container(border=True):
                    st.markdown(f"<div class='addon-title'>{name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='addon-desc'>{info['desc']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='addon-value'>{info['client_value']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='addon-price'>+ ${info['price']:,}</span>", unsafe_allow_html=True)

                    st.checkbox(
                        "Add to my order",
                        key=key,
                        value=st.session_state.get(key, False),
                    )

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


def render_submit_cta():
    """Prominent, clear 'Request My Proposal' button placed directly after the form.
    This is the primary, obvious submission action the user was missing.
    """
    st.markdown('<div class="submit-cta">', unsafe_allow_html=True)
    st.markdown("### Ready to receive your custom proposal?", unsafe_allow_html=True)
    st.markdown(
        "Review your selections in the sidebar, then click below. We will instantly generate a professional, "
        "client-ready proposal summary with exact pricing, scope, and clear next steps for Altamont Group.",
        unsafe_allow_html=True,
    )

    # Large, centered, unmistakable primary action
    col_l, col_btn, col_r = st.columns([1.35, 3.1, 1.35])
    with col_btn:
        submitted = st.button(
            "Request My Proposal",
            type="primary",
            use_container_width=True,
            help="Validates your selections and generates a detailed proposal ready to send to zs@altamontgroup.ca",
        )

    st.markdown(
        "<div style='margin-top:14px; font-size:0.82rem; color:#64748b;'>Your information is private to this session • No commitment until you email the proposal</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        success = capture_proposal_snapshot()
        if success:
            st.rerun()
        else:
            if st.session_state.submit_error:
                st.error(st.session_state.submit_error)
                if st.button("Dismiss", key="dismiss_cta_err", use_container_width=True):
                    st.session_state.submit_error = None
                    st.rerun()


def render_sidebar_summary():
    """Clean, premium live order summary that feels trustworthy."""
    with st.sidebar:
        st.markdown("### Your Live Estimate")
        st.caption("Updates instantly as you select options")

        base = st.session_state.base_package
        addons = get_selected_addons()
        total = calculate_total(base, addons)
        details = get_current_form_values()

        if base:
            st.success(f"**{base}**")
            st.markdown(f"<div style='font-size:0.9rem; color:#64748B; margin-top:-4px;'>${PACKAGES[base]['price']:,}</div>", unsafe_allow_html=True)
        else:
            st.info("Select a starting package to begin")

        if addons:
            st.markdown("**Enhancements**")
            for a in addons:
                st.markdown(f"• {a} <span style='color:#0D9488; font-weight:600;'>+${ADDONS[a]['price']:,}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='small-muted'>No enhancements selected</span>", unsafe_allow_html=True)

        if details.get("project_name"):
            st.markdown(f"**Project:** {details['project_name'][:48]}{'…' if len(details['project_name']) > 48 else ''}")

        st.divider()

        st.markdown(
            f"""
            <div class="sidebar-total">
                <div class="label">Estimated Total Investment</div>
                <div class="amount">${total:,}</div>
                <div style="font-size:0.72rem; opacity:0.75; margin-top:4px;">USD • one-time professional fee</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Transparent estimate. Final pricing confirmed after a 30-minute scoping call.")

        # Keep sidebar submit for power users, but label matches the main CTA and points to the new flow
        submitted = st.button(
            "Request My Proposal",
            type="primary",
            use_container_width=True,
            help="Validates your selections and opens the professional proposal summary (same as the button below the form).",
        )

        if submitted:
            success = capture_proposal_snapshot()
            if success:
                st.rerun()

        if st.session_state.submit_error:
            st.error(st.session_state.submit_error)
            if st.button("Dismiss", key="dismiss_err", use_container_width=True):
                st.session_state.submit_error = None
                st.rerun()

        st.divider()

        if st.button("Start Over — Clear Everything", use_container_width=True, type="secondary"):
            clear_all_selections()
            st.rerun()

        st.markdown(
            "<div class='small-muted' style='text-align:center; line-height:1.35; margin-top:10px;'>"
            "Altamont Group<br>"
            "<span style='font-size:0.7rem;'>Boutique advisory • Global reach</span></div>",
            unsafe_allow_html=True,
        )

def render_config_interface():
    """Main client flow."""
    render_top_bar()
    render_hero()
    render_trust_bar()

    render_package_selection()
    st.markdown("<br>", unsafe_allow_html=True)

    render_addon_selection()
    st.markdown("<br>", unsafe_allow_html=True)

    render_project_details()

    # Prominent, clear call-to-action right after the form (the key missing piece)
    render_submit_cta()

    st.markdown(
        "<div class='premium-note'>Your selections update live in the sidebar. All information stays private in this browser session.</div>",
        unsafe_allow_html=True,
    )

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
    safe_text = proposal_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

    # Gentle confirmation banner when arriving at the summary (improves perceived completion)
    st.success("Proposal generated successfully. Review the details below, then use the copy button to send it to Altamont Group.")

    st.markdown('<div class="proposal-container">', unsafe_allow_html=True)

    # === Top brand row with logo (more refined) ===
    logo_col, info_col = st.columns([0.9, 5.2])
    with logo_col:
        try:
            st.image(LOGO_PATH, width=118)
        except Exception:
            st.markdown(f"<span style='font-weight:700; color:{PRIMARY_NAVY}; font-size:1.1rem;'>ALTAMONT</span>", unsafe_allow_html=True)
    with info_col:
        st.markdown(
            f"""
            <div style="padding-top:2px;">
                <span style="font-size:1.42rem; font-weight:700; color:{PRIMARY_NAVY}; letter-spacing:-0.35px;">ALTAMONT GROUP</span><br>
                <span style="font-size:0.82rem; color:{TEXT_MUTED};">Strategic Advisory for Measurable Impact  •  www.altamontgroup.ca</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Professional proposal header banner
    st.markdown(
        f"""
        <div class="proposal-banner">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px;">
                <div>
                    <div style="font-size:0.68rem; letter-spacing:2.2px; opacity:0.7; margin-bottom:4px;">CONFIDENTIAL CLIENT PROPOSAL</div>
                    <div style="font-size:1.78rem; font-weight:700; line-height:1.02; margin-top:1px;">{data['proposal_id']}</div>
                </div>
                <div style="text-align:right; font-size:0.84rem; line-height:1.38; opacity:0.92;">
                    <div>Prepared {data['submitted_at']}</div>
                    <div style="margin-top:1px;">Altamont Group • Professional MERL Advisory</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # === PRIMARY EMAIL ACTION - The key improvement ===
    # This panel + button directly addresses "no easy way to send" and the exact requirement.
    st.markdown(
        f"""
        <div class="email-action-panel">
            <div style="font-weight:700; font-size:1.08rem; color:#0f766e; margin-bottom:6px;">
                Your proposal is ready to send.
            </div>
            <div class="instruction">
                <strong>Please paste this into an email and send it to zs@altamontgroup.ca to proceed with your order.</strong><br>
                We typically respond within one business day with a calendar link for a scoping call.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # The exact required button - large, primary, unmistakable
    col_copy, col_dl, col_back = st.columns([2.05, 1.35, 1.25], gap="medium")

    with col_copy:
        st.markdown(
            f"""
            <button onclick="
                const txt = `{safe_text}`;
                navigator.clipboard.writeText(txt).then(() => {{
                    const b = this;
                    const orig = b.innerHTML;
                    b.innerHTML = '✓ Copied! Now email to zs@altamontgroup.ca';
                    b.style.background = '#166534';
                    setTimeout(() => {{ b.innerHTML = orig; b.style.background = ''; }}, 2800);
                }}).catch(() => {{
                    alert('Copy failed. Please select the full text below and press Ctrl/Cmd + C.');
                }});
            " style="
                width: 100%;
                background: linear-gradient(155deg, #166534 0%, #14532d 100%);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 20px;
                font-size: 1.01rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 10px 22px -6px rgb(21 128 61 / 0.38);
                transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
                letter-spacing: 0.15px;
            ">Copy Proposal &amp; Send to Altamont Group</button>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align:center; font-size:0.78rem; color:#166534; margin-top:6px; font-weight:500;'>One-click copy • Paste into your email client</div>",
            unsafe_allow_html=True,
        )

    with col_dl:
        st.download_button(
            label="Download as .txt File",
            data=proposal_text,
            file_name=f"{data['proposal_id']}_Altamont_MERL_Proposal.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download the full proposal text for your records or to attach to email",
        )

    with col_back:
        if st.button("Edit My Selections", type="secondary", use_container_width=True, help="Return to the configurator to adjust package, add-ons, or details"):
            # Note: we do NOT clear data so they can come back easily, but for simplicity we allow re-entry to form
            st.session_state.order_submitted = False
            st.rerun()

    st.divider()

    # === Two-column clean summary (kept for review before sending) ===
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
            scope_bits.append(f"**{d['project_name']}**")
        if d.get("sector"):
            scope_bits.append(f"**{d['sector']}** sector")
        if d.get("timeline"):
            scope_bits.append(f"Timeline: **{d['timeline']}**")
        if d.get("num_beneficiaries"):
            scope_bits.append(f"~**{d['num_beneficiaries']:,}** beneficiaries")

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
        render_sidebar_summary()

if __name__ == "__main__":
    main()
