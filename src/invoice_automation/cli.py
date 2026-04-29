"""CLI entry point using click."""

import logging
import sys
from pathlib import Path

import click

from invoice_automation import __version__
from invoice_automation.excel_summary import ExcelSummaryError, generate_excel_summary
from invoice_automation.pdf_generator import PDFGeneratorError, generate_invoice_pdf
from invoice_automation.reader import CSVReadError, read_invoices_from_csv


def _setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """invoice-automation: Genera facturas PDF y resúmenes Excel desde CSV."""
    pass


@main.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="CSV file with invoice data",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(),
    help="Output directory for PDFs and summary",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def generate(input: str, output: str, verbose: bool) -> None:
    """
    Generate all invoice PDFs and an Excel summary.

    Reads the input CSV, generates one PDF per invoice, and creates
    an Excel summary with totals by client, month, and category.
    """
    _setup_logging(verbose)
    logger = logging.getLogger(__name__)

    input_path = Path(input)
    output_path = Path(output)

    logger.info("Reading invoices from %s", input_path)
    try:
        invoices = read_invoices_from_csv(input_path)
    except CSVReadError as e:
        logger.error("Failed to read CSV: %s", e)
        sys.exit(1)

    logger.info("Found %d invoices", len(invoices))

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    pdf_dir = output_path / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    # Generate PDFs
    logger.info("Generating PDFs in %s", pdf_dir)
    for invoice in invoices:
        pdf_path = pdf_dir / f"{invoice.invoice_id}.pdf"
        try:
            generate_invoice_pdf(invoice, pdf_path)
            logger.debug("Generated: %s", pdf_path)
        except PDFGeneratorError as e:
            logger.error("Failed to generate PDF for %s: %s", invoice.invoice_id, e)
            sys.exit(1)

    logger.info("Generated %d PDFs", len(invoices))

    # Generate Excel summary
    summary_path = output_path / "resumen.xlsx"
    logger.info("Generating Excel summary at %s", summary_path)
    try:
        generate_excel_summary(invoices, summary_path)
    except ExcelSummaryError as e:
        logger.error("Failed to generate Excel summary: %s", e)
        sys.exit(1)

    logger.info("Done! Summary: %s", summary_path)
    click.echo(f"Generated {len(invoices)} PDFs and summary Excel")


@main.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="CSV file with invoice data",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(),
    help="Output path for Excel summary",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def summary(input: str, output: str, verbose: bool) -> None:
    """
    Generate only the Excel summary from invoice CSV data.
    """
    _setup_logging(verbose)
    logger = logging.getLogger(__name__)

    input_path = Path(input)
    output_path = Path(output)

    logger.info("Reading invoices from %s", input_path)
    try:
        invoices = read_invoices_from_csv(input_path)
    except CSVReadError as e:
        logger.error("Failed to read CSV: %s", e)
        sys.exit(1)

    logger.info("Found %d invoices", len(invoices))

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Generating Excel summary at %s", output_path)
    try:
        generate_excel_summary(invoices, output_path)
    except ExcelSummaryError as e:
        logger.error("Failed to generate Excel summary: %s", e)
        sys.exit(1)

    logger.info("Done! Summary: %s", output_path)
    click.echo(f"Generated Excel summary: {output_path}")


if __name__ == "__main__":
    main()
