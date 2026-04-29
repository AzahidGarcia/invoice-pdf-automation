"""Pytest fixtures and configuration."""

from pathlib import Path

import pytest

from invoice_automation.models import Invoice, InvoiceItem


@pytest.fixture
def sample_invoice() -> Invoice:
    """A single sample invoice for testing."""
    return Invoice(
        invoice_id="TEST-001",
        client_name="Cliente de prueba",
        client_rfc="XAXX010101000",
        issue_date=__import__("datetime").date(2026, 4, 1),
        due_date=__import__("datetime").date(2026, 4, 15),
        items=[
            InvoiceItem(description="Cuaderno profesional", quantity=3, unit_price=85.00),
            InvoiceItem(description="Plumas azul", quantity=10, unit_price=12.50),
        ],
        category="Papeleria",
    )


@pytest.fixture
def fixtures_dir() -> Path:
    """Path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_csv_path(fixtures_dir: Path) -> Path:
    """Path to the sample invoices CSV fixture."""
    return fixtures_dir / "sample_invoices.csv"
