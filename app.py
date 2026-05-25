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
    """Professional plain-text proposal for download / email forwarding."""
    lines = []
    lines.append("=" * 74)
    lines.append("ALTAMONT GROUP")
    lines.append("CONFIDENTIAL CLIENT PROPOSAL")
    lines.append(f"Proposal ID: {data['proposal_id']}")
    lines.append(f"Prepared: {data['submitted_at']}")
    lines.append("=" * 74)
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
    lines.append("1. Altamont reviews your requirements (usually within 1 business day).")
    lines.append("2. You receive a calendar link for a 30-minute scoping conversation.")
    lines.append("3. We send a formal Statement of Work and refined quote within 48 hours.")
    lines.append("4. Work begins promptly once the agreement is signed.")
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');

    .stApp {{
        background-color: {BG_LIGHT};
    }}
    
    h1, h2, h3, h4, h5 {{
        color: {PRIMARY_NAVY};
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    
    .stMarkdown p, .stMarkdown li, .stMarkdown div {{
        color: {TEXT_DARK};
        font-size: 0.96rem;
        line-height: 1.55;
    }}

    /* Top professional bar */
    .top-brand-bar {{
        background: {PRIMARY_NAVY};
        padding: 10px 28px;
        border-radius: 0;
        margin: -1rem -1rem 1.25rem -1rem;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 4px solid {ACCENT_TEAL};
    }}
    
    .brand-left {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    
    .brand-name {{
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.4px;
        color: white;
    }}
    
    .brand-tag {{
        font-size: 0.78rem;
        opacity: 0.75;
        margin-top: -2px;
    }}

    /* Hero — client-first and premium */
    .hero-section {{
        text-align: center;
        padding: 2.1rem 1.4rem 2.25rem;
        background: white;
        border-radius: 20px;
        border: 1px solid {CARD_BORDER};
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }}
    
    .hero-headline {{
        font-size: 2.35rem;
        line-height: 1.12;
        font-weight: 700;
        color: {PRIMARY_NAVY};
        margin-bottom: 0.55rem;
        letter-spacing: -0.6px;
    }}
    
    .hero-sub {{
        font-size: 1.08rem;
        color: {TEXT_MUTED};
        max-width: 620px;
        margin: 0 auto 1rem;
        line-height: 1.5;
    }}

    /* Trust bar */
    .trust-row {{
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 0.6rem;
    }}
    .trust-pill {{
        background: {LIGHT_TEAL};
        color: {ACCENT_TEAL};
        font-size: 0.82rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 999px;
        white-space: nowrap;
    }}

    /* Section headers */
    .section-header {{
        font-size: 1.18rem;
        font-weight: 700;
        color: {PRIMARY_NAVY};
        margin: 1.6rem 0 0.35rem;
        padding-bottom: 8px;
        border-bottom: 3px solid {LIGHT_TEAL};
        letter-spacing: -0.3px;
    }}
    
    .section-caption {{
        color: {TEXT_MUTED};
        font-size: 0.9rem;
        margin-bottom: 0.9rem;
    }}

    /* Package cards — generous and clear */
    .pkg-card {{
        background: white;
        border: 2px solid {CARD_BORDER};
        border-radius: 16px;
        padding: 22px 20px 18px;
        height: 100%;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }}
    .pkg-card.selected {{
        border-color: {ACCENT_TEAL};
        background: {LIGHT_TEAL};
        box-shadow: 0 10px 28px rgba(13, 148, 136, 0.18);
        transform: translateY(-2px);
    }}
    .pkg-card h3 {{
        margin: 0 0 4px 0;
        font-size: 1.18rem;
        font-weight: 700;
    }}
    .pkg-tagline {{
        font-size: 0.82rem;
        color: {ACCENT_TEAL};
        font-weight: 600;
        margin-bottom: 10px;
    }}
    .pkg-benefit {{
        font-size: 0.92rem;
        line-height: 1.45;
        color: {TEXT_DARK};
        margin-bottom: 12px;
        min-height: 72px;
    }}
    .pkg-price {{
        font-size: 1.85rem;
        font-weight: 700;
        color: {ACCENT_TEAL};
        margin: 8px 0 4px;
    }}
    .pkg-includes {{
        font-size: 0.82rem;
        line-height: 1.42;
    }}
    .pkg-includes li {{
        margin-bottom: 3px;
    }}

    /* Add-on cards — clean and scannable */
    .addon-card {{
        background: white;
        border: 1px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 16px 17px;
        height: 100%;
        transition: all 0.2s ease;
    }}
    .addon-card:hover {{
        border-color: #94a3b8;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }}
    .addon-title {{
        font-weight: 700;
        font-size: 0.98rem;
        color: {PRIMARY_NAVY};
        margin-bottom: 4px;
    }}
    .addon-desc {{
        font-size: 0.84rem;
        color: {TEXT_MUTED};
        line-height: 1.4;
        margin-bottom: 8px;
        min-height: 52px;
    }}
    .addon-value {{
        font-size: 0.81rem;
        font-style: italic;
        color: {ACCENT_TEAL};
        margin-bottom: 6px;
    }}
    .addon-price {{
        color: {SOFT_TEAL};
        font-weight: 700;
        font-size: 0.98rem;
    }}

    /* Sidebar premium summary */
    .sidebar-total {{
        background: {PRIMARY_NAVY};
        color: white;
        padding: 16px 18px;
        border-radius: 12px;
        text-align: center;
        margin: 14px 0 8px;
    }}
    .sidebar-total .label {{
        font-size: 0.75rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .sidebar-total .amount {{
        font-size: 1.95rem;
        font-weight: 700;
        line-height: 1.05;
        margin-top: 2px;
    }}

    /* Proposal screen — feels like a real client document */
    .proposal-container {{
        max-width: 1080px;
        margin: 0 auto;
    }}
    .proposal-header {{
        background: linear-gradient(135deg, {PRIMARY_NAVY} 0%, #1E2937 100%);
        color: white;
        padding: 22px 32px;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }}
    .proposal-meta {{
        font-size: 0.8rem;
        opacity: 0.75;
        letter-spacing: 0.5px;
    }}
    .scope-section {{
        background: white;
        border: 1px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 1rem;
    }}
    .next-steps-box {{
        background: #F0FDFA;
        border-left: 6px solid {ACCENT_TEAL};
        padding: 18px 22px;
        border-radius: 10px;
        margin: 1rem 0;
    }}
    .next-steps-box ol {{
        margin: 10px 0 0 18px;
        padding: 0;
    }}
    .next-steps-box li {{
        margin-bottom: 6px;
    }}

    /* Misc polish */
    .stButton > button {{
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.1rem;
    }}
    .stButton > button[kind="primary"] {{
        background-color: {ACCENT_TEAL};
        border-color: {ACCENT_TEAL};
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: {SOFT_TEAL};
    }}
    .small-muted {{
        font-size: 0.78rem;
        color: {TEXT_MUTED};
    }}
    .premium-note {{
        font-size: 0.82rem;
        color: {TEXT_MUTED};
        text-align: center;
        margin-top: 1.25rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# RENDER FUNCTIONS
# ============================================================================

def render_top_bar():
    """Premium, trustworthy header with prominent logo."""
    col_logo, col_text, col_spacer = st.columns([0.9, 4.2, 1.5])
    
    with col_logo:
        try:
            st.image(LOGO_PATH, width=138)  # Prominent but not oversized for the 160px source
        except Exception:
            st.markdown(f"<span style='font-size:1.1rem; font-weight:700; color:{PRIMARY_NAVY};'>ALTAMONT GROUP</span>", unsafe_allow_html=True)
    
    with col_text:
        st.markdown(
            f"""
            <div style="padding-top: 6px;">
                <span class="brand-name" style="font-size:1.48rem; color:{PRIMARY_NAVY};">Altamont Group</span><br>
                <span style="font-size:0.88rem; color:{TEXT_MUTED}; font-weight:500;">Strategic advisory for measurable impact</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""<div style="height:1px; background:{CARD_BORDER}; margin:14px 0 18px 0;"></div>""",
        unsafe_allow_html=True,
    )

def render_hero():
    """Strong, client-centric opening."""
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

    # Prominent Load Example + subtle how-it-works hint
    c1, c2, c3 = st.columns([1.1, 2.4, 1.1])
    with c2:
        if st.button(
            "📋  Load a Realistic Example",
            type="secondary",
            use_container_width=True,
            help="See a complete, high-quality order that a real foundation might submit",
        ):
            load_example_order()
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align:center; margin-top:0.4rem;">
            <span class="small-muted">Typical turnaround: proposal in your inbox within 48 hours • Clear next steps always provided</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_trust_bar():
    """Credibility signals that matter to clients."""
    c1, c2, c3, c4 = st.columns(4, gap="small")
    
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
                <div style="background:white; border:1px solid {CARD_BORDER}; border-radius:12px; padding:9px 8px; text-align:center;">
                    <div style="font-size:1.32rem; font-weight:700; color:{ACCENT_TEAL}; line-height:1.1;">{num}</div>
                    <div class="small-muted" style="margin-top:1px;">{label}</div>
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

            btn_label = "✓ Selected" if is_selected else "Select this option"
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
            "Work Email (for proposal delivery)",
            key="contact_email",
            placeholder="you@yourorganization.org",
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
    """Clean, premium live order summary that feels trustworthy."""
    with st.sidebar:
        st.markdown("### Your Estimate")
        st.caption("Live pricing • Updates instantly")

        base = st.session_state.base_package
        addons = get_selected_addons()
        total = calculate_total(base, addons)
        details = get_current_form_values()

        if base:
            st.success(f"**{base}**", icon="✅")
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

        submitted = st.button(
            "Submit & Receive Proposal →",
            type="primary",
            use_container_width=True,
            help="Generates a professional, client-ready proposal document. Nothing is sent to Altamont yet.",
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

    st.markdown(
        "<div class='premium-note'>Your selections stay in this browser session only. Use the sidebar to review pricing and request your proposal.</div>",
        unsafe_allow_html=True,
    )

def render_proposal_screen():
    """Premium, client-ready proposal that feels like a real document from a top advisory firm."""
    data = st.session_state.proposal_data
    if not data:
        st.error("No proposal data found.")
        if st.button("Start a New Request"):
            clear_all_selections()
            st.rerun()
        return

    # === Professional Proposal Header ===
    st.markdown('<div class="proposal-container">', unsafe_allow_html=True)

    # Logo + firm name row
    logo_col, info_col = st.columns([0.85, 5.2])
    with logo_col:
        try:
            st.image(LOGO_PATH, width=115)
        except Exception:
            st.markdown("**ALTAMONT GROUP**")
    with info_col:
        st.markdown(
            f"""
            <div style="margin-top:5px;">
                <span style="font-size:1.38rem; font-weight:700; color:{PRIMARY_NAVY};">ALTAMONT GROUP</span><br>
                <span style="font-size:0.84rem; color:{TEXT_MUTED};">Strategic Advisory for Measurable Impact</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Dark proposal banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(90deg, {PRIMARY_NAVY} 0%, #1E2937 100%); color:white; padding:20px 28px; border-radius:14px; margin:16px 0 20px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="font-size:0.72rem; letter-spacing:1.5px; opacity:0.65; margin-bottom:2px;">CONFIDENTIAL CLIENT PROPOSAL</div>
                    <div style="font-size:1.72rem; font-weight:700; line-height:1.05; margin-top:2px;">{data['proposal_id']}</div>
                </div>
                <div style="text-align:right; font-size:0.85rem; line-height:1.35; opacity:0.9;">
                    <div>Prepared {data['submitted_at']}</div>
                    <div style="margin-top:3px;">Altamont Group • www.altamontgroup.ca</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Thank you + reassurance
    st.success(
        "Thank you. Your request has been captured. A senior member of the Altamont MERL team will contact you within one business day to schedule a short scoping conversation.",
        icon="✉️",
    )

    # Two-column layout
    left, right = st.columns([1.08, 1], gap="large")

    with left:
        st.markdown("#### Selected Engagement")
        st.markdown(f"**{data['base_package']}** — ${data['base_price']:,} USD")
        st.caption(data['base_tagline'])

        with st.expander("What is included", expanded=True):
            for item in data["base_includes"]:
                st.markdown(f"• {item}")
        
        st.markdown(f"<div style='font-size:0.88rem; background:#F8FAFC; padding:10px 13px; border-radius:8px; border:1px solid {CARD_BORDER}; margin-top:8px;'><strong>Why this matters for you:</strong> {data['base_benefit']}</div>", unsafe_allow_html=True)

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
            st.caption("None selected — you can always add these later.")

        st.markdown("#### Total Estimated Investment")
        st.markdown(
            f"<span style='font-size:2.05rem; font-weight:700; color:{ACCENT_TEAL};'>${data['total']:,}</span> <span style='color:#64748B; font-size:0.95rem;'>USD</span>",
            unsafe_allow_html=True,
        )
        st.caption("One-time professional services fee. Final pricing confirmed after scoping.")

    with right:
        st.markdown("#### Project Context")
        d = data["details"]

        scope_bits = []
        if d.get("project_name"):
            scope_bits.append(f"**{d['project_name']}**")
        if d.get("sector"):
            scope_bits.append(f"in the **{d['sector']}** sector")
        if d.get("timeline"):
            scope_bits.append(f"Timeline: **{d['timeline']}**")
        if d.get("num_beneficiaries"):
            scope_bits.append(f"Reach: approximately **{d['num_beneficiaries']:,}** people")

        scope_html = " • ".join(scope_bits) if scope_bits else "Details captured for scoping."
        st.markdown(f"<div class='scope-section'>{scope_html}</div>", unsafe_allow_html=True)

        if d.get("organization"):
            st.markdown(f"**Organization:** {d['organization']}")
        if d.get("email"):
            st.markdown(f"**Primary contact:** {d['email']}")

        if d.get("notes"):
            st.markdown("**Additional context captured:**")
            st.info(d["notes"])

        st.markdown("#### Clear Next Steps")
        st.markdown(
            """
            <div class="next-steps-box">
            <ol>
                <li><strong>Review (1 business day)</strong> — We study your requirements and prepare any clarifying questions.</li>
                <li><strong>30-minute scoping call</strong> — We refine scope, timeline, deliverables, and approach together.</li>
                <li><strong>Formal SOW + Quote</strong> — You receive a detailed Statement of Work and final pricing within 48 hours.</li>
                <li><strong>Agreement & Kickoff</strong> — Work begins promptly once everything is signed.</li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div style='font-size:0.8rem; color:{TEXT_MUTED}; margin-top:10px;'>This estimate is valid for 30 days. We are happy to adjust scope to fit your budget or timeline.</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # Actions
    colA, colB, colC = st.columns([1.15, 1.15, 1])
    with colA:
        proposal_text = generate_proposal_text(data)
        st.download_button(
            label="📥 Download Professional Proposal (.txt)",
            data=proposal_text,
            file_name=f"{data['proposal_id']}_Altamont_MERL_Proposal.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with colB:
        if st.button("Start a New Request", type="secondary", use_container_width=True):
            clear_all_selections()
            st.rerun()

    with colC:
        st.markdown(
            "<div style='padding-top:8px; font-size:0.78rem; color:#64748B; text-align:right;'>Questions? Email your Altamont contact or use the form on altamontgroup.ca</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # close proposal-container

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
