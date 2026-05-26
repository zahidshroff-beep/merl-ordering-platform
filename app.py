import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ==================== CONFIG ====================
st.set_page_config(page_title="MERL Order | Altamont Group", page_icon="📋", layout="wide")

# ==================== DATA ====================
PACKAGES = {
    "Build Your Foundation": {
        "price": 7250,
        "tagline": "For new programs or major redesigns",
        "benefit": "Get a strong, donor-ready MERL foundation from day one.",
        "includes": [
            "Full indicator framework design",
            "Baseline + endline methodology",
            "Theory of Change + Results Framework",
            "Data collection tools (templates + protocols)",
            "1 virtual workshop with your team"
        ]
    },
    "Demonstrate Results": {
        "price": 7250,
        "tagline": "For evaluations, mid-term/final reviews",
        "benefit": "Clear, credible evidence for donors and stakeholders.",
        "includes": [
            "Evaluation design (process/outcome/impact)",
            "Data collection & analysis",
            "Findings + actionable recommendations",
            "Donor-ready report + executive summary",
            "Presentation to your team/stakeholders"
        ]
    },
    "Turn Data into Decisions": {
        "price": 7250,
        "tagline": "For teams that have data but need insights",
        "benefit": "Transform existing data into clear decisions and stories.",
        "includes": [
            "Data cleaning + quality check",
            "Analysis against your indicators",
            "Dashboard + visual insights",
            "Learning brief + recommendations",
            "1 workshop to interpret findings together"
        ]
    }
}

ADDONS = {
    "Gender, Equity & Inclusion Focus": {"price": 1850, "value": "Stronger equity lens across design, data, and reporting"},
    "Donor-Ready Reporting Pack": {"price": 1650, "value": "Professional reports tailored to your main donor(s)"},
    "Learning Briefs & Knowledge Products": {"price": 1450, "value": "Concise, shareable products for internal & external use"},
    "Remote Data Collection Support": {"price": 1250, "value": "Tools + protocols for phone/online data collection"},
    "Stakeholder Validation Workshop": {"price": 950, "value": "Half-day session to validate findings with your team"},
    " MEL System Health Check": {"price": 850, "value": "Quick diagnostic + prioritized improvement plan"}
}

SECTORS = ["Agriculture & Livelihoods", "Education", "Health", "WASH", "Climate & Resilience", "Governance & Accountability", "Economic Development", "Other"]
TIMELINE_OPTIONS = ["1-3 months", "3-6 months", "6-12 months", "12+ months"]

# ==================== SESSION STATE ====================
def init_session_state():
    if "base_package" not in st.session_state:
        st.session_state.base_package = None
    if "selected_addons" not in st.session_state:
        st.session_state.selected_addons = set()
    if "order_submitted" not in st.session_state:
        st.session_state.order_submitted = False
    if "proposal_data" not in st.session_state:
        st.session_state.proposal_data = None
    if "submit_error" not in st.session_state:
        st.session_state.submit_error = None

# ==================== HELPER FUNCTIONS ====================
def get_selected_addons():
    return list(st.session_state.selected_addons)

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
        return False, "Project or program name is required."
    if not details.get("sector"):
        return False, "Please select the primary sector."
    email = (details.get("email") or "").strip()
    if not email:
        return False, "Your work email is required."
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Please enter a valid work email address."
    return True, None

def save_order_to_sheet(data):
    # Placeholder - will be replaced with real Google Sheets later
    st.success("Order saved (demo mode)")
    return True

def capture_proposal_snapshot():
    try:
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
            "submitted_at": datetime.now().strftime("%d %b, %Y at %I:%M %p"),
            "base_package": base,
            "base_price": PACKAGES[base]["price"] if base else 0,
            "total": total,
            "project_name": details.get("project_name", ""),
            "organization": details.get("organization", ""),
            "email": details.get("email", ""),
        }
        return True
    except Exception as e:
        st.session_state.submit_error = f"Error: {str(e)}"
        return False

def clear_all_selections():
    st.session_state.base_package = None
    st.session_state.selected_addons = set()
    st.session_state.order_submitted = False
    st.session_state.proposal_data = None
    st.session_state.submit_error = None

# ==================== UI ====================
def render_top_bar():
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
        <span style="font-size:1.6rem; font-weight:700; color:#0f172a;">ALTAMONT GROUP</span>
        <span style="background:#0f766e; color:white; padding:2px 10px; border-radius:9999px; font-size:0.75rem;">MERL Ordering</span>
    </div>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("### High-quality MERL support, without the RFP headache.")
    st.caption("Configure your engagement • Transparent pricing • 48-hour proposal turnaround")

def render_package_selection():
    st.markdown("### 1. Choose your starting package")
    cols = st.columns(3)
    for i, (name, info) in enumerate(PACKAGES.items()):
        with cols[i]:
            if st.button(name, key=f"pkg_{i}", use_container_width=True):
                st.session_state.base_package = name

def render_addon_selection():
    st.markdown("### 2. Add enhancements (optional)")
    for name, info in ADDONS.items():
        checked = st.checkbox(f"{name} (+${info['price']})", key=f"addon_{name}")
        if checked:
            st.session_state.selected_addons.add(name)
        else:
            st.session_state.selected_addons.discard(name)

def render_project_details():
    st.markdown("### 3. Tell us about your project")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Project Name *", key="proj_name")
        st.text_input("Organization", key="org_name")
        st.text_input("Work Email *", key="contact_email")
    with col2:
        st.selectbox("Sector *", [""] + SECTORS, key="sector")
        st.selectbox("Timeline", TIMELINE_OPTIONS, key="timeline")
        st.number_input("Rough number of people who will benefit", min_value=0, key="num_beneficiaries")

def render_submit_cta():
    base = st.session_state.get("base_package")
    addons = get_selected_addons()
    total = calculate_total(base, addons) if base else 0

    st.markdown("---")
    if st.button("Submit My Request", type="primary", use_container_width=True):
        save_order_to_sheet({
            "project_name": st.session_state.get("proj_name", ""),
            "organization": st.session_state.get("org_name", ""),
            "email": st.session_state.get("contact_email", ""),
            "package": base,
            "addons": ", ".join(addons) if addons else "None",
            "total_price": total
        })
        success = capture_proposal_snapshot()
        if success:
            st.session_state.order_submitted = True
            st.rerun()

def main():
    init_session_state()
    render_top_bar()
    render_hero()

    if st.session_state.order_submitted:
        st.success("Request Received Successfully")
        st.markdown("Thank you. Your request has been submitted to Altamont Group.")
        if st.button("Submit Another Request"):
            clear_all_selections()
            st.rerun()
        return

    render_package_selection()
    render_addon_selection()
    render_project_details()
    render_submit_cta()

if __name__ == "__main__":
    main()