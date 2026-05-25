"""
MERL Order - Module 1 (Improved)
Professional customer-facing web app for configuring and ordering MERL services.
Branded for Altamont Group with logo integration and premium UX polish.
Built with Streamlit.
"""

import streamlit as st
from datetime import datetime
import random

# ============================================================================
# CONFIGURATION - Easy to modify pricing, packages, and descriptions
# ============================================================================

PAGE_TITLE = "MERL Order | Altamont Group"
PAGE_ICON = "altamont_logo.png"

# Brand colors (calm, professional consulting palette)
PRIMARY_BLUE = "#1E3A5F"      # Deep navy blue
ACCENT_TEAL = "#0F766E"       # Teal / sea green
LIGHT_TEAL = "#CCFBF1"        # Very light teal bg
SOFT_GREEN = "#059669"        # Success / selected green
CARD_BORDER = "#CBD5E1"       # Slate gray for cards
BG_LIGHT = "#F8FAFC"          # App background
TEXT_DARK = "#1E293B"         # Main text
TEXT_MUTED = "#64748B"        # Secondary text

# Logo path (assumes file is in the same directory as app.py)
LOGO_PATH = "altamont_logo.png"

# Entry-level packages (low-ticket entry points)
PACKAGES = {
    "MERL Starter Kit": {
        "price": 3950,
        "short_desc": "Basic indicator framework + simple monitoring plan",
        "includes": [
            "Up to 15 core indicators defined",
            "Basic monitoring & data collection plan",
            "One virtual review & feedback cycle",
            "Standard deliverables package",
            "Email support throughout project"
        ]
    },
    "Quick Evaluation Pack": {
        "price": 6750,
        "short_desc": "Evaluation design + data collection plan + summary report",
        "includes": [
            "Full evaluation design & methodology",
            "Data collection instruments & protocol",
            "Sampling strategy and timeline",
            "Summary findings report (20-25 pages)",
            "One stakeholder presentation"
        ]
    },
    "Dashboard Lite": {
        "price": 5250,
        "short_desc": "Clean dashboard setup with basic reporting",
        "includes": [
            "Power BI or Tableau dashboard (up to 5 pages)",
            "Core indicator visualization suite",
            "Data refresh & automation guide",
            "1-hour user training session",
            "3 months light maintenance support"
        ]
    }
}

# Layered add-on modules (upsells)
ADDONS = {
    "Advanced Indicator Framework": {
        "price": 2250,
        "desc": "Expanded indicator library, results framework alignment, and target-setting workshop.",
        "includes": ["30+ indicators", "Theory of change integration", "Target setting & workshop"]
    },
    "Data Collection Tools & Templates": {
        "price": 1850,
        "desc": "Ready-to-deploy survey instruments, interview guides, and mobile data collection setup.",
        "includes": ["ODK/KoboToolbox forms", "Qualitative tools", "Enumerator training pack"]
    },
    "Custom Dashboard Development": {
        "price": 4500,
        "desc": "Fully bespoke interactive dashboard with your branding, roles, and automated reporting.",
        "includes": ["Unlimited pages & views", "Role-based access", "Scheduled exports & alerts"]
    },
    "Automated Reporting & Insights": {
        "price": 2950,
        "desc": "Automated quarterly and annual report generation with narrative, charts, and insights.",
        "includes": ["Report templates", "Narrative drafting support", "Delivery automation setup"]
    },
    "Learning Products & Knowledge Products": {
        "price": 1650,
        "desc": "High-quality learning briefs, case studies, one-pagers, and training modules.",
        "includes": ["2-3 knowledge products", "Professional visuals", "Facilitator notes"]
    },
    "Full MERL System Design": {
        "price": 7500,
        "desc": "End-to-end MERL system architecture for your program or entire organization.",
        "includes": ["Comprehensive M&E plan", "All tools + dashboards", "Capacity building roadmap"]
    }
}

SECTORS = [
    "Global Health",
    "Education & Youth Development",
    "Agriculture & Food Security",
    "Climate Change & Environment",
    "Democratic Governance & Accountability",
    "Economic Development & Livelihoods",
    "Humanitarian Assistance & Protection",
    "Water, Sanitation & Hygiene (WASH)",
    "Other / Multiple Sectors"
]

TIMELINE_OPTIONS = [
    "1-3 months",
    "3-6 months",
    "6-12 months",
    "12+ months"
]

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables on first load."""
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
    """Reset the entire ordering flow (used by 'Start New Order' and Clear button)."""
    # Clear package
    st.session_state.base_package = None

    # Clear all addon checkboxes
    for name in ADDONS.keys():
        key = f"cb_{name.replace(' ', '_').replace('&', 'and')}"
        if key in st.session_state:
            del st.session_state[key]

    # Clear project form fields
    form_keys = ["proj_name", "org_name", "contact_email", "sector", "timeline", "num_indicators", "notes"]
    for key in form_keys:
        if key in st.session_state:
            del st.session_state[key]

    # Reset order flow
    st.session_state.order_submitted = False
    st.session_state.proposal_data = None
    st.session_state.submit_error = None


def load_example_order():
    """Prefill the form with a realistic example order for demo purposes."""
    # Select a base package
    st.session_state.base_package = "Quick Evaluation Pack"

    # Select 2-3 add-ons
    example_addons = [
        "Advanced Indicator Framework",
        "Data Collection Tools & Templates",
        "Automated Reporting & Insights",
    ]
    for name in ADDONS.keys():
        key = f"cb_{name.replace(' ', '_').replace('&', 'and')}"
        st.session_state[key] = name in example_addons

    # Fill project details
    st.session_state.proj_name = "USAID Health Resilience Initiative - Phase II"
    st.session_state.org_name = "Ministry of Health - Republic of Kenya"
    st.session_state.contact_email = "merl@health.go.ke"
    st.session_state.sector = "Global Health"
    st.session_state.timeline = "6-12 months"
    st.session_state.num_indicators = 45
    st.session_state.notes = "Strong emphasis on gender and youth indicators. Data collection must be feasible in remote counties. Dashboard should integrate with DHIS2."

    st.session_state.submit_error = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_selected_addons():
    """Return list of currently selected add-on names based on checkbox states."""
    selected = []
    for name in ADDONS.keys():
        key = f"cb_{name.replace(' ', '_').replace('&', 'and')}"
        if st.session_state.get(key, False):
            selected.append(name)
    return selected


def calculate_total(base_package, selected_addons):
    """Calculate live total price from base + selected add-ons."""
    if not base_package or base_package not in PACKAGES:
        return 0
    total = PACKAGES[base_package]["price"]
    for addon in selected_addons:
        if addon in ADDONS:
            total += ADDONS[addon]["price"]
    return total


def get_current_form_values():
    """Read current values from all project detail widgets."""
    return {
        "project_name": st.session_state.get("proj_name", "").strip(),
        "organization": st.session_state.get("org_name", "").strip(),
        "email": st.session_state.get("contact_email", "").strip(),
        "sector": st.session_state.get("sector", ""),
        "timeline": st.session_state.get("timeline", ""),
        "num_indicators": st.session_state.get("num_indicators", 0),
        "notes": st.session_state.get("notes", "").strip(),
    }


def validate_order(base_package, details, selected_addons):
    """Return (is_valid, error_message)."""
    if not base_package:
        return False, "Please select a base package."
    if not details.get("project_name"):
        return False, "Project / Program name is required."
    if not details.get("sector"):
        return False, "Please select a primary sector / focus area."
    return True, None


def capture_proposal_snapshot():
    """Freeze current selections + form data into proposal_data for the summary screen."""
    base = st.session_state.base_package
    addons = get_selected_addons()
    details = get_current_form_values()
    total = calculate_total(base, addons)

    is_valid, error = validate_order(base, details, addons)
    if not is_valid:
        st.session_state.submit_error = error
        return False

    proposal_id = f"MERL-{datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"

    st.session_state.proposal_data = {
        "proposal_id": proposal_id,
        "submitted_at": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        "base_package": base,
        "base_price": PACKAGES[base]["price"],
        "base_includes": PACKAGES[base]["includes"],
        "addons": addons,
        "addon_prices": {a: ADDONS[a]["price"] for a in addons},
        "total": total,
        "details": details,
    }
    st.session_state.order_submitted = True
    st.session_state.submit_error = None
    return True


def generate_proposal_text(data):
    """Generate clean plain-text proposal for download."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"MERL ORDER — PROPOSAL SUMMARY")
    lines.append(f"Proposal ID: {data['proposal_id']}")
    lines.append(f"Generated: {data['submitted_at']}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("SELECTED BASE PACKAGE")
    lines.append("-" * 30)
    lines.append(f"{data['base_package']}  —  ${data['base_price']:,}")
    lines.append("")
    lines.append("Included:")
    for item in data["base_includes"]:
        lines.append(f"  • {item}")
    lines.append("")

    if data["addons"]:
        lines.append("SELECTED ADD-ON MODULES")
        lines.append("-" * 30)
        for addon in data["addons"]:
            price = data["addon_prices"].get(addon, 0)
            lines.append(f"{addon}  —  +${price:,}")
        lines.append("")
    else:
        lines.append("ADD-ON MODULES: None selected")
        lines.append("")

    lines.append("PROJECT DETAILS")
    lines.append("-" * 30)
    d = data["details"]
    lines.append(f"Project/Program: {d.get('project_name') or '—'}")
    if d.get("organization"):
        lines.append(f"Organization: {d['organization']}")
    lines.append(f"Sector: {d.get('sector') or '—'}")
    lines.append(f"Timeline: {d.get('timeline') or '—'}")
    lines.append(f"Est. Indicators: {d.get('num_indicators', 0)}")
    if d.get("notes"):
        lines.append(f"Notes: {d['notes']}")
    lines.append("")

    lines.append("TOTAL ESTIMATED INVESTMENT")
    lines.append("-" * 30)
    lines.append(f"USD ${data['total']:,}")
    lines.append("")
    lines.append("Note: This is an estimate. Final pricing and scope confirmed after scoping call.")
    lines.append("")

    lines.append("NEXT STEPS")
    lines.append("-" * 30)
    lines.append("1. MERL team reviews your requirements (1 business day).")
    lines.append("2. You receive a calendar link for a 30-minute scoping call.")
    lines.append("3. We deliver a detailed Statement of Work + refined quote.")
    lines.append("4. Kickoff meeting upon signed agreement.")
    lines.append("")
    lines.append("=" * 70)
    lines.append("Thank you for choosing MERL Order.")
    lines.append("Questions? Contact: orders@merl.example.com (demo)")
    lines.append("=" * 70)

    return "\n".join(lines)


# ============================================================================
# CUSTOM CSS (Professional, clean consulting aesthetic)
# ============================================================================

def inject_custom_css():
    """Inject professional styling via Streamlit's markdown."""
    css = f"""
    <style>
    /* App background and typography */
    .stApp {{
        background-color: {BG_LIGHT};
    }}
    h1, h2, h3, h4 {{
        color: {PRIMARY_BLUE};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .stMarkdown p, .stMarkdown li {{
        color: {TEXT_DARK};
    }}

    /* Top brand bar */
    .top-bar {{
        background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {ACCENT_TEAL} 100%);
        padding: 12px 24px;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .top-bar .brand {{
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.3px;
    }}
    .top-bar .tag {{
        font-size: 0.85rem;
        opacity: 0.9;
    }}

    /* Hero section - more premium */
    .hero {{
        text-align: center;
        padding: 1.6rem 1.2rem 1.8rem;
        background: white;
        border-radius: 18px;
        border: 1px solid {CARD_BORDER};
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }}
    .hero h1 {{
        font-size: 2.35rem;
        line-height: 1.15;
        margin-bottom: 0.4rem;
        color: {PRIMARY_BLUE};
    }}
    .hero p {{
        font-size: 1.05rem;
        color: {TEXT_MUTED};
        max-width: 640px;
        margin: 0 auto;
    }}

    /* Section headers */
    .step-header {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {PRIMARY_BLUE};
        margin: 1.25rem 0 0.5rem;
        padding-bottom: 4px;
        border-bottom: 2px solid {LIGHT_TEAL};
    }}

    /* Package cards - more premium */
    .package-card {{
        background: white;
        border: 1.5px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 20px 18px;
        height: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }}
    .package-card.selected {{
        border-color: {SOFT_GREEN};
        background: {LIGHT_TEAL};
        box-shadow: 0 6px 16px rgba(5, 150, 105, 0.15);
        transform: translateY(-1px);
    }}
    .package-card h4 {{
        margin: 0 0 6px 0;
        font-size: 1.05rem;
    }}
    .package-price {{
        font-size: 1.65rem;
        font-weight: 700;
        color: {ACCENT_TEAL};
        margin: 8px 0;
    }}
    .package-card ul {{
        font-size: 0.82rem;
        line-height: 1.35;
        padding-left: 18px;
        margin: 6px 0 4px;
        color: {TEXT_DARK};
    }}
    .package-card li {{
        margin-bottom: 2px;
    }}

    /* Add-on cards - premium feel */
    .addon-card {{
        background: white;
        border: 1px solid {CARD_BORDER};
        border-radius: 12px;
        padding: 14px 15px;
        height: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }}
    .addon-card:hover {{
        border-color: #94a3b8;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }}
    .addon-title {{
        font-weight: 600;
        font-size: 0.95rem;
        color: {PRIMARY_BLUE};
        margin-bottom: 2px;
    }}
    .addon-price {{
        color: {SOFT_GREEN};
        font-weight: 700;
        font-size: 0.95rem;
    }}

    /* Sidebar summary styling */
    .sidebar-total {{
        background: {PRIMARY_BLUE};
        color: white;
        padding: 14px 16px;
        border-radius: 10px;
        text-align: center;
        margin: 12px 0;
    }}
    .sidebar-total .label {{
        font-size: 0.8rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .sidebar-total .amount {{
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1.1;
    }}

    /* Proposal / success screen */
    .proposal-header {{
        background: linear-gradient(90deg, {ACCENT_TEAL} 0%, {SOFT_GREEN} 100%);
        color: white;
        padding: 18px 24px;
        border-radius: 14px;
        text-align: center;
    }}
    .proposal-header h2 {{
        color: white;
        margin: 4px 0 2px;
    }}
    .scope-box {{
        background: white;
        border: 1px solid {CARD_BORDER};
        border-radius: 10px;
        padding: 16px 18px;
        margin: 12px 0;
    }}
    .next-steps {{
        background: #F0F9FF;
        border-left: 5px solid {ACCENT_TEAL};
        padding: 14px 18px;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    .next-steps ol {{
        margin: 8px 0 0 18px;
        padding: 0;
    }}

    /* Misc polish */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
    }}
    .stButton > button[kind="primary"] {{
        background-color: {ACCENT_TEAL};
        border-color: {ACCENT_TEAL};
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: {SOFT_GREEN};
        border-color: {SOFT_GREEN};
    }}
    .small-muted {{
        font-size: 0.78rem;
        color: {TEXT_MUTED};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# UI RENDER FUNCTIONS
# ============================================================================

def render_top_bar():
    """Professional header with Altamont Group branding and logo."""
    col_logo, col_title = st.columns([0.9, 5.5], vertical_alignment="center")

    with col_logo:
        try:
            st.image(LOGO_PATH, width=52)
        except Exception:
            st.markdown("**ALTAMONT**")  # fallback

    with col_title:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:12px;">
                <div>
                    <span style="font-size:1.55rem; font-weight:700; color:{PRIMARY_BLUE}; letter-spacing:-0.4px;">MERL Order</span>
                    <span style="font-size:0.8rem; color:{TEXT_MUTED}; margin-left:8px;">by Altamont Group</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style="background: linear-gradient(90deg, {PRIMARY_BLUE} 0%, {ACCENT_TEAL} 100%); 
                    height: 3px; border-radius: 2px; margin: 8px 0 18px 0;"></div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    """Improved professional hero with stronger messaging and demo helper."""
    st.markdown(
        f"""
        <div class="hero">
            <h1 style="margin-bottom:0.35rem; font-size:2.25rem;">Professional MERL Services,<br>Configured in Minutes</h1>
            <p style="margin:0 auto 0.8rem; max-width:620px; font-size:1.05rem;">
                Get a clear, transparent proposal for monitoring, evaluation, research, and learning services 
                tailored to your program.
            </p>
            <div style="margin-top:0.4rem; font-size:0.9rem; color:#475569;">
                <strong>Altamont Group</strong> — Delivering high-quality MERL solutions across Africa and beyond
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load Example button - very useful for demos
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        if st.button(
            "🚀 Load Example Order",
            type="secondary",
            use_container_width=True,
            help="Prefills a realistic sample order so you can quickly explore the full experience",
        ):
            load_example_order()
            st.rerun()


def render_trust_signals():
    """Professional trust signals aligned with Altamont Group branding."""
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div style='text-align:center; padding:8px 6px; background:white; border-radius:10px; border:1px solid {CARD_BORDER};'>"
            "<div style='font-size:1.15rem; font-weight:700; color:#0F766E;'>12+</div>"
            "<div class='small-muted'>Countries across Africa</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div style='text-align:center; padding:8px 6px; background:white; border-radius:10px; border:1px solid {CARD_BORDER};'>"
            "<div style='font-size:1.15rem; font-weight:700; color:#0F766E;'>85+</div>"
            "<div class='small-muted'>MERL projects delivered</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"<div style='text-align:center; padding:8px 6px; background:white; border-radius:10px; border:1px solid {CARD_BORDER};'>"
            "<div style='font-size:1.15rem; font-weight:700; color:#0F766E;'>48hr</div>"
            "<div class='small-muted'>Average proposal turnaround</div></div>",
            unsafe_allow_html=True,
        )


def render_package_selection():
    """Step 1: Three package cards with selection buttons."""
    st.markdown('<div class="step-header">1. Choose Your Base Package</div>', unsafe_allow_html=True)
    st.caption("All packages include a kickoff call, clear deliverables, and one round of revisions.")

    pkg_names = list(PACKAGES.keys())
    cols = st.columns(3, gap="medium")

    for i, name in enumerate(pkg_names):
        info = PACKAGES[name]
        is_selected = st.session_state.base_package == name

        with cols[i]:
            # Card container
            card_class = "package-card selected" if is_selected else "package-card"
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

            st.markdown(f"<h4>{name}{'  ✓' if is_selected else ''}</h4>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#64748B; font-size:0.82rem; min-height:38px;'>{info['short_desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='package-price'>${info['price']:,}</div>", unsafe_allow_html=True)

            # Includes
            for item in info["includes"]:
                st.markdown(f"<div style='font-size:0.78rem; line-height:1.3;'>• {item}</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)  # close card

            # Selection button
            btn_label = "Selected ✓" if is_selected else "Select this package"
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
    """Step 2: Add-on modules in a responsive grid with live checkboxes."""
    st.markdown('<div class="step-header">2. Add Optional Modules (Layered Upsells)</div>', unsafe_allow_html=True)
    st.caption("Select any combination. Each add-on is priced as a one-time project enhancement.")

    addon_names = list(ADDONS.keys())
    cols_per_row = 3

    for row_start in range(0, len(addon_names), cols_per_row):
        row_cols = st.columns(cols_per_row, gap="medium")
        for j, col in enumerate(row_cols):
            idx = row_start + j
            if idx >= len(addon_names):
                break
            name = addon_names[idx]
            info = ADDONS[name]
            key = f"cb_{name.replace(' ', '_').replace('&', 'and')}"

            with col:
                with st.container(border=True):
                    st.markdown(f"<div class='addon-title'>{name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:0.78rem; color:#64748B; min-height:42px;'>{info['desc']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='addon-price'>+ ${info['price']:,}</span>", unsafe_allow_html=True)

                    # Compact includes line
                    inc_str = " • ".join(info["includes"])
                    st.markdown(f"<div style='font-size:0.72rem; color:#64748B; margin-top:4px;'>{inc_str}</div>", unsafe_allow_html=True)

                    # Checkbox (state persists automatically via key)
                    st.checkbox(
                        "Add to my order",
                        key=key,
                        value=st.session_state.get(key, False),
                    )


def render_project_details():
    """Step 3: Simple scoped questions."""
    st.markdown('<div class="step-header">3. Project Details</div>', unsafe_allow_html=True)
    st.caption("Help us understand scope so we can prepare an accurate proposal.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.text_input(
            "Project / Program Name *",
            key="proj_name",
            placeholder="e.g. USAID Health Resilience Activity 2025-2028",
            help="The official name of the program or project this MERL support is for.",
        )
        st.text_input(
            "Organization (optional)",
            key="org_name",
            placeholder="e.g. Save the Children / Ministry of Health",
        )
        st.text_input(
            "Work Email (for confirmation)",
            key="contact_email",
            placeholder="you@organization.org",
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
        st.slider(
            "Rough number of indicators",
            min_value=5,
            max_value=120,
            value=25,
            step=5,
            key="num_indicators",
            help="This helps us estimate effort. A precise number is not required at this stage.",
        )

    st.text_area(
        "Specific focus areas, constraints, or notes (optional)",
        key="notes",
        placeholder="e.g. Need strong gender and inclusion lens; data must integrate with DHIS2; remote data collection only.",
        height=90,
        help="Any specific requirements, data systems, geographic constraints, or donor requirements we should know about.",
    )


def render_sidebar_summary():
    """Live order summary + Submit button (always visible in sidebar)."""
    with st.sidebar:
        st.markdown("### 📋 Order Summary")
        st.caption("Updates live as you configure")

        base = st.session_state.base_package
        addons = get_selected_addons()
        total = calculate_total(base, addons)
        details = get_current_form_values()

        if base:
            st.success(f"**{base}**", icon="✅")
            st.markdown(f"<div style='font-size:0.9rem; color:#64748B;'>${PACKAGES[base]['price']:,}</div>", unsafe_allow_html=True)
        else:
            st.info("No base package selected yet")

        if addons:
            st.markdown("**Add-ons**")
            for a in addons:
                st.markdown(f"• {a} <span style='color:#059669;'>+${ADDONS[a]['price']:,}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='small-muted'>No add-ons selected</span>", unsafe_allow_html=True)

        # Project quick view
        if details.get("project_name"):
            st.markdown(f"**Project:** {details['project_name'][:42]}{'...' if len(details['project_name'])>42 else ''}")
        if details.get("sector"):
            st.markdown(f"**Sector:** {details['sector']}")

        st.divider()

        # Big total
        st.markdown(
            f"""
            <div class="sidebar-total">
                <div class="label">Estimated Total</div>
                <div class="amount">${total:,}</div>
                <div style="font-size:0.72rem; opacity:0.8; margin-top:2px;">USD • one-time project fee</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Prices are estimates. Final quote issued after scoping call.")

        # Submit button
        submitted = st.button(
            "Submit Order → Get Proposal",
            type="primary",
            use_container_width=True,
            help="This will generate a professional proposal summary based on your selections. No data is sent yet.",
        )

        if submitted:
            success = capture_proposal_snapshot()
            if success:
                st.rerun()
            # error will be shown below

        if st.session_state.submit_error:
            st.error(st.session_state.submit_error)
            # Auto-clear next interaction by user
            if st.button("Dismiss", key="dismiss_err"):
                st.session_state.submit_error = None
                st.rerun()

        st.divider()

        # Utility
        if st.button("Clear All Selections", use_container_width=True, type="secondary"):
            clear_all_selections()
            st.rerun()

        st.markdown(
            "<div class='small-muted' style='margin-top:12px; text-align:center;'>Altamont Group<br>Module 1 — Frontend Demo</div>",
            unsafe_allow_html=True,
        )


def render_config_interface():
    """Main configuration flow (shown when order not yet submitted)."""
    render_top_bar()
    render_hero()
    render_trust_signals()

    # Main content area
    render_package_selection()
    st.markdown("<br>", unsafe_allow_html=True)

    render_addon_selection()
    st.markdown("<br>", unsafe_allow_html=True)

    render_project_details()

    # Footer note
    st.markdown(
        "<div style='margin-top:1.25rem; font-size:0.78rem; color:#64748B; text-align:center;'>"
        "Your selections are saved in this browser session. Use the sidebar to review pricing and submit."
        "</div>",
        unsafe_allow_html=True,
    )


def render_proposal_screen():
    """Clean, professional post-submission proposal summary."""
    data = st.session_state.proposal_data
    if not data:
        st.error("No proposal data found. Please start a new order.")
        if st.button("Start New Order"):
            clear_all_selections()
            st.rerun()
        return

    # Header with logo
    col1, col2 = st.columns([1, 6])
    with col1:
        try:
            st.image(LOGO_PATH, width=48)
        except Exception:
            pass
    with col2:
        st.markdown(
            f"""
            <div class="proposal-header" style="margin-bottom:0; padding:18px 24px;">
                <div style="font-size:0.85rem; opacity:0.9;">ORDER RECEIVED</div>
                <h2 style="margin:4px 0 2px;">Proposal {data['proposal_id']}</h2>
                <div style="font-size:0.9rem;">Generated on {data['submitted_at']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.success("Thank you. Your configuration has been captured. A member of our MERL team will contact you shortly.", icon="📬")

    # Two-column layout: Package + Addons | Scope
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown("#### Selected Package")
        st.markdown(f"**{data['base_package']}** — ${data['base_price']:,}")
        with st.expander("What's included", expanded=True):
            for item in data["base_includes"]:
                st.markdown(f"• {item}")

        if data["addons"]:
            st.markdown("#### Selected Add-on Modules")
            for addon in data["addons"]:
                price = data["addon_prices"].get(addon, 0)
                st.markdown(f"**{addon}** — +${price:,}")
            st.caption("Detailed scope for add-ons will be refined during scoping.")
        else:
            st.markdown("#### Add-on Modules")
            st.caption("None selected")

        st.markdown("#### Total Estimated Investment")
        st.markdown(f"<span style='font-size:2rem; font-weight:700; color:#0F766E;'>${data['total']:,}</span> <span style='color:#64748B;'>USD</span>", unsafe_allow_html=True)
        st.caption("This is an estimate. Final pricing confirmed after scoping call.")

    with right:
        st.markdown("#### Project Scope Summary")
        d = data["details"]

        scope_text = f"""**{d.get('project_name', 'Your project')}** in the **{d.get('sector', 'selected sector')}** sector."""
        if d.get("timeline"):
            scope_text += f" Expected timeline: **{d['timeline']}**."
        if d.get("num_indicators"):
            scope_text += f" Approximately **{d['num_indicators']} indicators** under management."

        st.markdown(
            f"<div class='scope-box'>{scope_text}</div>",
            unsafe_allow_html=True,
        )

        if d.get("organization"):
            st.markdown(f"**Organization:** {d['organization']}")
        if d.get("email"):
            st.markdown(f"**Contact:** {d['email']}")

        if d.get("notes"):
            st.markdown("**Additional notes captured:**")
            st.info(d["notes"])

        st.markdown("#### What Happens Next")
        st.markdown(
            """
            <div class="next-steps">
            <ol>
                <li><strong>Review (1 business day)</strong> — Our team reviews your requirements and prepares clarifying questions.</li>
                <li><strong>Scoping Call (30 min)</strong> — We schedule a short call to refine scope, timeline, and deliverables.</li>
                <li><strong>Detailed SOW + Quote</strong> — You receive a formal Statement of Work and final pricing within 48 hours of the call.</li>
                <li><strong>Kickoff</strong> — Work begins once the agreement is signed.</li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Action buttons
    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        proposal_text = generate_proposal_text(data)
        st.download_button(
            label="📥 Download Proposal (.txt)",
            data=proposal_text,
            file_name=f"{data['proposal_id']}_MERL_Proposal.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with colB:
        if st.button("📧 Simulate Email Confirmation", use_container_width=True):
            st.info(f"Demo: Confirmation email would be sent to {d.get('email') or 'your provided address'} with proposal attached.")
    with colC:
        if st.button("🔄 Start New Order", type="primary", use_container_width=True):
            clear_all_selections()
            st.rerun()

    st.markdown(
        "<div class='small-muted' style='text-align:center; margin-top:1rem;'>Prepared by <strong>Altamont Group</strong> — Module 1 Frontend Prototype</div>",
        unsafe_allow_html=True,
    )


# ============================================================================
# MAIN APP ENTRYPOINT
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

    # Always render sidebar summary when in ordering mode
    if not st.session_state.order_submitted:
        render_sidebar_summary()

    # Main view switch
    if st.session_state.order_submitted and st.session_state.proposal_data:
        render_proposal_screen()
    else:
        render_config_interface()


if __name__ == "__main__":
    main()
