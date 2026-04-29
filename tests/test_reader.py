"""Tests for the CSV reader module."""

from pathlib import Path

import pytest

from invoice_automation.models import Invoice, InvoiceItem
from invoice_automation.reader import CSVReadError, _parse_items, read_invoices_from_csv


class TestParseItems:
    """Tests for _parse_items helper."""

    def test_valid_items(self) -> None:
        """Test parsing valid items string."""
        items = _parse_items("Cuaderno|3|85.00;;Plumas|10|12.50")
        assert len(items) == 2
        assert items[0].description == "Cuaderno"
        assert items[0].quantity == 3
        assert items[0].unit_price == 85.00
        assert items[1].description == "Plumas"
        assert items[1].quantity == 10
        assert items[1].unit_price == 12.50

    def test_single_item(self) -> None:
        """Test parsing single item."""
        items = _parse_items("Lapiz|5|8.00")
        assert len(items) == 1
        assert items[0].description == "Lapiz"
        assert items[0].quantity == 5

    def test_empty_string_raises(self) -> None:
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError):
            _parse_items("")

    def test_invalid_format_raises(self) -> None:
        """Test that invalid format raises ValueError."""
        with pytest.raises(ValueError):
            _parse_items("Cuaderno|3")  # Missing price

    def test_whitespace_stripped(self) -> None:
        """Test that whitespace is stripped."""
        items = _parse_items("  Cuaderno  |  3  |  85.00  ")
        assert items[0].description == "Cuaderno"
        assert items[0].quantity == 3


class TestInvoiceModel:
    """Tests for Invoice Pydantic model."""

    def test_subtotal_calculation(self) -> None:
        """Test subtotal is calculated correctly."""
        items = [
            InvoiceItem(description="Item 1", quantity=2, unit_price=100.00),
            InvoiceItem(description="Item 2", quantity=3, unit_price=50.00),
        ]
        # 2*100 + 3*50 = 350
        assert items[0].subtotal == 200.00
        assert items[1].subtotal == 150.00

    def test_invoice_totals(self) -> None:
        """Test invoice total calculation with IVA."""
        invoice = Invoice(
            invoice_id="TEST-001",
            client_name="Test",
            client_rfc="XAXX010101000",
            issue_date=__import__("datetime").date(2026, 4, 1),
            items=[InvoiceItem(description="Item", quantity=1, unit_price=100.00)],
        )
        # Subtotal = 100, IVA = 16, Total = 116
        assert float(invoice.subtotal) == 100.00
        assert float(invoice.iva_amount) == 16.00
        assert float(invoice.total) == 116.00

    def test_rfc_uppercase(self) -> None:
        """Test that RFC is converted to uppercase."""
        invoice = Invoice(
            invoice_id="TEST-001",
            client_name="Test",
            client_rfc="xaxx010101000",
            issue_date=__import__("datetime").date(2026, 4, 1),
            items=[],
        )
        assert invoice.client_rfc == "XAXX010101000"


class TestReadInvoices:
    """Tests for read_invoices_from_csv function."""

    def test_read_valid_csv(self, sample_csv_path: Path) -> None:
        """Test reading a valid CSV file."""
        invoices = read_invoices_from_csv(sample_csv_path)
        assert len(invoices) == 2
        assert invoices[0].invoice_id == "TEST-FAC-001"
        assert invoices[1].invoice_id == "TEST-FAC-002"

    def test_file_not_found(self) -> None:
        """Test that non-existent file raises CSVReadError."""
        with pytest.raises(CSVReadError, match="File not found"):
            read_invoices_from_csv("/nonexistent/file.csv")

    def test_missing_columns(self, tmp_path: Path) -> None:
        """Test that missing required columns raises CSVReadError."""
        csv_path = tmp_path / "bad.csv"
        csv_path.write_text("invoice_id,client_name\nFAC-001,Cliente\n")
        with pytest.raises(CSVReadError, match="Missing required columns"):
            read_invoices_from_csv(csv_path)
