"""
MERL Ordering App — Google Sheets Integration (Strict Mode)

Provides a lazy-initialized, robust client for appending orders.
Per the project requirements:
- Initialization is LAZY (only happens on actual submit, never at import time).
- Behavior is STRICT: credentials.json is required for saving orders.
- Error messages are excellent and actionable so a non-technical user or
  new team member knows exactly what to do.

The rest of the app (configurator + proposal preview) works perfectly
even when credentials.json is absent. Only the final submit step requires it.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

# Scope required for both Sheets and Drive (Drive is needed to open the spreadsheet by name)
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# The exact sheet name the client expects (must match the real Google Sheet)
SHEET_NAME = "MERL Orders - Module 2"

# Cache for the lazy client (module-level, survives reruns within the same process)
_sheet_client: gspread.Worksheet | None = None


class SheetsConfigurationError(Exception):
    """Raised when credentials.json is missing, invalid, or the target sheet cannot be reached."""
    pass


def _find_credentials_path() -> Path:
    """
    Resolve the location of credentials.json relative to this file.
    Works whether the app is run from the project root or elsewhere.
    """
    here = Path(__file__).resolve().parent
    candidate = here / "credentials.json"
    if candidate.exists():
        return candidate

    # Fallback: current working directory (common when running `streamlit run app.py`)
    cwd_candidate = Path.cwd() / "credentials.json"
    if cwd_candidate.exists():
        return cwd_candidate

    return candidate  # Return the most likely path for a good error message


def _load_credentials() -> Credentials:
    """Load and validate the service account credentials file."""
    creds_path = _find_credentials_path()

    if not creds_path.exists():
        raise SheetsConfigurationError(
            f"Google Sheets credentials file not found.\n\n"
            f"Expected location: {creds_path}\n\n"
            "To enable order saving:\n"
            "1. Place your service-account credentials.json in the same folder as app.py\n"
            "2. Make sure the file is named exactly 'credentials.json'\n"
            "3. The sheet 'MERL Orders - Module 2' must exist and the service account must have edit access.\n\n"
            "Contact zs@altamontgroup.ca if you need a credentials file or help setting this up."
        )

    try:
        with open(creds_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if "private_key" not in raw or "client_email" not in raw:
            raise ValueError("credentials.json is missing required service-account fields")
    except Exception as exc:
        raise SheetsConfigurationError(
            f"credentials.json exists but could not be read or is not a valid Google service-account key.\n\n"
            f"Path: {creds_path}\n"
            f"Error: {exc}\n\n"
            "Common fixes:\n"
            "• Re-download the JSON from Google Cloud Console (IAM & Admin → Service Accounts)\n"
            "• Make sure it is a Service Account key (not OAuth client ID)\n"
            "• Do not edit the file manually"
        ) from exc

    try:
        return Credentials.from_service_account_file(str(creds_path), scopes=SCOPE)
    except Exception as exc:
        raise SheetsConfigurationError(
            f"Failed to create Google credentials from the service-account file.\n\n"
            f"Path: {creds_path}\n"
            f"Error: {exc}"
        ) from exc


def _open_sheet() -> gspread.Worksheet:
    """Authorize and open the target worksheet. Only called on first real use."""
    global _sheet_client

    if _sheet_client is not None:
        return _sheet_client

    creds = _load_credentials()
    try:
        client = gspread.authorize(creds)
        spreadsheet = client.open(SHEET_NAME)
        _sheet_client = spreadsheet.sheet1
        return _sheet_client
    except gspread.exceptions.SpreadsheetNotFound as exc:
        raise SheetsConfigurationError(
            f"Google Sheet '{SHEET_NAME}' was not found.\n\n"
            "The service account can authenticate, but the spreadsheet does not exist or is not shared with it.\n\n"
            "Fix:\n"
            "1. Create (or rename) a Google Sheet exactly named 'MERL Orders - Module 2'\n"
            "2. Share it with the service account email (edit access)\n"
            "3. The first tab should be the one that will receive rows."
        ) from exc
    except Exception as exc:
        raise SheetsConfigurationError(
            f"Could not connect to the Google Sheet.\n\n"
            f"Sheet name: {SHEET_NAME}\n"
            f"Error: {exc}\n\n"
            "Common causes: network issues, insufficient permissions, or the sheet was deleted/renamed."
        ) from exc


def save_order_to_sheet(data: dict[str, Any]) -> tuple[bool, str]:
    """
    Append a single order row to the Google Sheet.

    Returns:
        (success: bool, message: str)

    This function is intentionally lazy — the Google client is only created
    the first time a real order is submitted.

    In strict mode we raise (via SheetsConfigurationError) on any configuration
    problem so the caller can present a clear, blocking error to the user.
    """
    try:
        sheet = _open_sheet()

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
            data.get("total_price", ""),
        ]
        sheet.append_row(row)
        return True, "Order saved to Google Sheets successfully."
    except SheetsConfigurationError:
        # Re-raise so the UI can show a prominent, actionable error
        raise
    except Exception as exc:
        # Unexpected runtime error (quota, network drop during write, etc.)
        return False, f"Unexpected error while saving to Google Sheets: {exc}"
