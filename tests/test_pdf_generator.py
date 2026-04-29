"""Tests for the PDF generator module."""

from pathlib import Path

import pytest

from invoice_automation.models import Invoice
from invoice_automation.pdf_generator import PDFGeneratorError, generate_invoice_pdf


class TestPDFGenerator:
    """Tests for generate_invoice_pdf function."""

    def test_generate_pdf(self, sample_invoice: Invoice, tmp_path: Path) -> None:
        """Test that PDF is generated and has reasonable size."""
        output_path = tmp_path / "test_invoice.pdf"
        result = generate_invoice_pdf(sample_invoice, output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.stat().st_size > 1000  # Should be > 1KB

    def test_generate_pdf_creates_file(self, sample_invoice: Invoice, tmp_path: Path) -> None:
        """Test that the PDF file is actually created."""
        output_path = tmp_path / "FAC-001.pdf"
        generate_invoice_pdf(sample_invoice, output_path)

        assert output_path.exists()
        # Read first bytes to verify it's a PDF
        with open(output_path, "rb") as f:
            header = f.read(4)
            assert header == b"%PDF"

    def test_invalid_path_should_fail(self, sample_invoice: Invoice) -> None:
        """Test that generation with invalid path may fail appropriately."""
        # Writing to /dev/null or similar might work, but /nonexistent/ will fail
        output_path = Path("/nonexistent/directory/FAC-001.pdf")
        with pytest.raises(PDFGeneratorError):
            generate_invoice_pdf(sample_invoice, output_path)
