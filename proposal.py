"""
MERL Ordering App — Proposal Generation

Pure function that turns a captured proposal snapshot into a professional,
plain-text proposal ready for copy/paste into email or download as .txt.

No Streamlit dependencies. Safe to import from anywhere.
"""

from __future__ import annotations

from typing import Any


def generate_proposal_text(data: dict[str, Any]) -> str:
    """
    Generate a clean, professional plain-text summary for the client's records.

    This is provided as a downloadable file after submission.
    The order has already been saved. No manual copy/email action is required.
    """
    lines: list[str] = []

    lines.append("=" * 74)
    lines.append("ALTAMONT GROUP")
    lines.append("MERL SUPPORT REQUEST — RECEIPT & SUMMARY")
    lines.append(f"Proposal ID: {data['proposal_id']}")
    lines.append(f"Submitted: {data['submitted_at']}")
    lines.append("=" * 74)
    lines.append("")

    lines.append("Thank you for submitting your request for Monitoring, Evaluation,")
    lines.append("Research & Learning (MERL) support.")
    lines.append("")
    lines.append("Your submission has been received and saved.")
    lines.append("Altamont Group will review your requirements and contact you")
    lines.append("within one business day to schedule a short scoping conversation.")
    lines.append("")

    d = data["details"]
    if d.get("organization") or d.get("project_name"):
        lines.append("SUBMITTED FOR")
        lines.append("-" * 20)
        if d.get("organization"):
            lines.append(f"{d['organization']}")
        if d.get("project_name"):
            lines.append(f"Project: {d['project_name']}")
        if d.get("email"):
            lines.append(f"Contact: {d['email']}")
        lines.append("")

    lines.append("ENGAGEMENT REQUESTED")
    lines.append("-" * 20)
    lines.append(f"{data['base_package']}  —  ${data['base_price']:,} USD")
    lines.append("")

    if data["addons"]:
        lines.append("SELECTED ENHANCEMENTS")
        lines.append("-" * 20)
        for addon in data["addons"]:
            price = data["addon_prices"].get(addon, 0)
            lines.append(f"+ {addon}  —  ${price:,}")
        lines.append("")

    lines.append("PROJECT CONTEXT")
    lines.append("-" * 20)
    lines.append(f"Sector: {d.get('sector', '—')}")
    lines.append(f"Timeline: {d.get('timeline', '—')}")
    if d.get("num_beneficiaries"):
        lines.append(f"Estimated reach: {d['num_beneficiaries']:,} people")
    if d.get("notes"):
        lines.append(f"Notes: {d['notes']}")
    lines.append("")

    lines.append("TOTAL ESTIMATED INVESTMENT")
    lines.append("-" * 20)
    lines.append(f"USD ${data['total']:,}")
    lines.append("")

    lines.append("NEXT STEPS")
    lines.append("-" * 20)
    lines.append("Altamont Group will contact you within one business day")
    lines.append("to schedule a 30-minute scoping call.")
    lines.append("We will then prepare a formal Statement of Work and refined quote.")
    lines.append("")

    lines.append("=" * 74)
    lines.append("Altamont Group")
    lines.append("Strategic advisory for organizations that want measurable impact.")
    lines.append("www.altamontgroup.ca")
    lines.append("zs@altamontgroup.ca")
    lines.append("=" * 74)

    return "\n".join(lines)
