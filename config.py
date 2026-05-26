"""
MERL Ordering App — Configuration

All client-facing content, pricing, brand constants, and pure business logic.
This module contains no Streamlit dependencies and can be imported anywhere.

Changes to packages, add-ons, pricing, or messaging should be made here.
"""

from __future__ import annotations

from typing import Any

# ============================================================================
# BRAND & PAGE CONFIG
# ============================================================================

PAGE_TITLE = "Order MERL Support | Altamont Group"
PAGE_ICON = "altamont_logo.png"
LOGO_PATH = "altamont_logo.png"

# Brand colors — premium consulting aesthetic (deep navy + confident teal)
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

# ============================================================================
# CLIENT-CENTRIC BASE PACKAGES
# Reframed around common client situations and outcomes.
# ============================================================================

PACKAGES: dict[str, dict[str, Any]] = {
    "Build Your Foundation": {
        "price": 4850,
        "tagline": "Best for new programs or major redesigns",
        "client_benefit": "Establish clear measures of success and a practical monitoring system so you start strong, measure what matters, and satisfy donor requirements from day one.",
        "includes": [
            "Up to 20 core performance measures with plain-language definitions",
            "Practical monitoring plan tailored to your implementation realities",
            "Results framework that connects activities to outcomes",
            "One focused virtual workshop with your team (90 minutes)",
            "Clean deliverables package + 30 days of email support",
        ],
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
            "Virtual presentation to your team and key stakeholders",
        ],
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
            "90 days of light support and refinements",
        ],
    },
}

# ============================================================================
# SIMPLE, TRANSPARENT ADD-ONS
# Clear value, minimal jargon, focused on common client pain points.
# ============================================================================

ADDONS: dict[str, dict[str, Any]] = {
    "Gender, Equity & Inclusion Focus": {
        "price": 1850,
        "desc": "Integrate strong GESI analysis and disaggregated indicators throughout your framework or evaluation so you can credibly report on equity outcomes.",
        "client_value": "Show donors and stakeholders that you are serious about inclusion and leaving no one behind.",
    },
    "Donor-Ready Reporting Pack": {
        "price": 1650,
        "desc": "Custom templates and automation for your primary donor's reporting requirements, plus narrative support that makes your results shine.",
        "client_value": "Cut reporting time dramatically and submit polished, consistent reports every quarter.",
    },
    "Stakeholder Data Collection Tools": {
        "price": 1950,
        "desc": "Professionally designed surveys, interview guides, and mobile data collection setup (Kobo/ODK) with enumerator guidance.",
        "client_value": "Collect high-quality data from the field without reinventing the wheel or hiring expensive consultants.",
    },
    "Executive Dashboard & Portal": {
        "price": 4250,
        "desc": "Premium interactive dashboard with role-based views, automated email summaries, and a clean executive portal for leadership and boards.",
        "client_value": "Give your leadership and donors an always-on, beautiful view of progress they can trust.",
    },
    "Learning Briefs & Knowledge Products": {
        "price": 1450,
        "desc": "Two to three high-quality learning briefs, case studies, or one-pagers with professional design — perfect for sharing with partners and funders.",
        "client_value": "Turn your results into compelling stories that build your reputation and support resource mobilization.",
    },
    "Team Capability Workshop": {
        "price": 2250,
        "desc": "Half-day virtual workshop that equips your team with practical skills to maintain and use your new MERL system long after we leave.",
        "client_value": "Build lasting internal capacity instead of remaining dependent on external support.",
    },
}

# ============================================================================
# SUPPORTING LISTS
# ============================================================================

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
    "Other / Multiple Sectors",
]

TIMELINE_OPTIONS = [
    "1–3 months (rapid or focused scope)",
    "3–6 months (standard engagement)",
    "6–12 months (multi-phase or complex)",
    "12+ months (long-term partnership)",
]

# ============================================================================
# PURE HELPER FUNCTIONS (no Streamlit dependencies)
# ============================================================================

def get_addon_checkbox_key(name: str) -> str:
    """
    Generate a stable session_state key for an add-on checkbox.
    Centralizes the fragile string sanitization in one place.
    """
    safe = name.replace(" ", "_").replace("&", "and").replace(",", "")
    return f"cb_{safe}"


def calculate_total(base_package: str | None, selected_addons: list[str]) -> int:
    """Return the total price for the selected package + add-ons."""
    if not base_package or base_package not in PACKAGES:
        return 0
    total = PACKAGES[base_package]["price"]
    for addon in selected_addons:
        if addon in ADDONS:
            total += ADDONS[addon]["price"]
    return total


def validate_order(
    base_package: str | None,
    details: dict[str, Any],
    selected_addons: list[str],
) -> tuple[bool, str | None]:
    """
    Validate that the order has the minimum required information.
    Returns (is_valid, error_message).
    """
    if not base_package:
        return False, "Please select one of the three starting packages above."

    if not details.get("project_name"):
        return False, "Project or program name is required so we can prepare your proposal accurately."

    if not details.get("sector"):
        return False, "Please select the primary sector or focus area."

    email = (details.get("email") or "").strip()
    if not email:
        return False, "Your work email is required so we can send your custom proposal and schedule a scoping call."

    # Basic email sanity check (kept simple and fast)
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Please enter a valid work email address (e.g. you@yourorganization.org)."

    return True, None
