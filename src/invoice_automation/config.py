"""Branding, colors, and defaults for invoice generation."""

from typing import Final

# Business info
BUSINESS_NAME: Final[str] = "Papelería La Esquina"
BUSINESS_ADDRESS: Final[str] = "Av. Principal #123, Col. Centro, Ciudad de México, CDMX"
BUSINESS_EMAIL: Final[str] = "contacto@lasesquina.com"
BUSINESS_PHONE: Final[str] = "(55) 1234-5678"
BUSINESS_RFC: Final[str] = "XAXX010101000"

# VAT
IVA_RATE: Final[float] = 0.16

# Currency
DEFAULT_CURRENCY: Final[str] = "MXN"

# Colors (hex with # prefix for ReportLab HexColor())
COLOR_PRIMARY: Final[str] = "#1E3A5F"  # Dark blue
COLOR_SECONDARY: Final[str] = "#4A6FA5"  # Medium blue
COLOR_ACCENT: Final[str] = "#2E7D32"  # Green (for totals)
COLOR_TEXT: Final[str] = "#212121"  # Near black
COLOR_TEXT_LIGHT: Final[str] = "#757575"  # Gray
COLOR_BG_HEADER: Final[str] = "#1E3A5F"
COLOR_BG_ALT: Final[str] = "#F5F5F5"  # Light gray for alternating rows
COLOR_BORDER: Final[str] = "#BDBDBD"
COLOR_WHITE: Final[str] = "#FFFFFF"

# PDF layout
PAGE_SIZE: Final[tuple[int, int]] = (612, 792)  # Letter size in points
MARGIN: Final[int] = 50
LOGO_SIZE: Final[int] = 60
