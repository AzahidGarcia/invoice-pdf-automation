"""Professional PDF generation with ReportLab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from invoice_automation import config
from invoice_automation.models import Invoice


class PDFGeneratorError(Exception):
    """Raised when PDF generation fails."""


def generate_invoice_pdf(invoice: Invoice, output_path: str | Path) -> Path:
    """
    Generate a professional PDF invoice.

    Args:
        invoice: The invoice data
        output_path: Where to save the PDF

    Returns:
        Path to the generated PDF
    """
    path = Path(output_path)
    try:
        doc = SimpleDocTemplate(
            str(path),
            pagesize=letter,
            leftMargin=config.MARGIN,
            rightMargin=config.MARGIN,
            topMargin=config.MARGIN,
            bottomMargin=config.MARGIN,
        )
    except Exception as e:
        raise PDFGeneratorError(f"Failed to create PDF document: {e}") from e

    story: list[Flowable] = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor(config.COLOR_PRIMARY),
        spaceAfter=6,
    )
    header_style = ParagraphStyle(
        "InvoiceHeader",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor(config.COLOR_TEXT_LIGHT),
        spaceAfter=2,
    )
    body_style = ParagraphStyle(
        "InvoiceBody",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor(config.COLOR_TEXT),
        spaceAfter=6,
    )

    # Header with logo placeholder and business info
    _add_header(story, title_style, header_style)

    # Invoice title
    story.append(Paragraph("FACTURA", title_style))
    story.append(Spacer(1, 0.1 * inch))

    # Invoice meta info table
    _add_invoice_meta(story, invoice, body_style)

    story.append(Spacer(1, 0.3 * inch))

    # Items table
    _add_items_table(story, invoice)

    story.append(Spacer(1, 0.2 * inch))

    # Totals
    _add_totals(story, invoice)

    story.append(Spacer(1, 0.4 * inch))

    # Footer
    _add_footer(story, body_style)

    try:
        doc.build(story)
    except Exception as e:
        raise PDFGeneratorError(f"Failed to build PDF: {e}") from e

    return path


def _add_header(story: list[Flowable], title_style: ParagraphStyle, meta_style: ParagraphStyle) -> None:
    """Add the header with logo placeholder and business info."""
    header_data = [
        [
            Paragraph(
                f"<font color='{config.COLOR_PRIMARY}'><b>{config.BUSINESS_NAME}</b></font>",
                title_style,
            ),
            Paragraph(
                f"<font color='{config.COLOR_TEXT_LIGHT}'>{config.BUSINESS_ADDRESS}</font><br/>"
                f"{config.BUSINESS_EMAIL}<br/>{config.BUSINESS_PHONE}",
                meta_style,
            ),
        ]
    ]
    header_table = Table(header_data, colWidths=[3 * inch, 3.5 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )
    story.append(header_table)

    # Logo placeholder rectangle
    logo_data = [[Paragraph(f"<font color='{config.COLOR_WHITE}'>LOGO</font>", ParagraphStyle(
        "LogoPlaceholder",
        fontSize=14,
        textColor=colors.HexColor(config.COLOR_WHITE),
        alignment=1,
    ))]]
    logo_table = Table(
        logo_data,
        colWidths=[1 * inch],
        rowHeights=[0.8 * inch],
    )
    logo_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(config.COLOR_SECONDARY)),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(logo_table)
    story.append(Spacer(1, 0.2 * inch))


def _add_invoice_meta(story: list[Flowable], invoice: Invoice, style: ParagraphStyle) -> None:
    """Add invoice metadata table (ID, client, dates)."""
    meta_info = [
        ["Factura No.:", invoice.invoice_id],
        ["Cliente:", invoice.client_name],
        ["RFC:", invoice.client_rfc],
        ["Fecha de emisión:", invoice.issue_date.strftime("%d/%m/%Y")],
    ]
    if invoice.due_date:
        meta_info.append(["Fecha de vencimiento:", invoice.due_date.strftime("%d/%m/%Y")])

    meta_table = Table(meta_info, colWidths=[1.5 * inch, 4 * inch])
    meta_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor(config.COLOR_TEXT_LIGHT)),
                ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor(config.COLOR_TEXT)),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(meta_table)


def _add_items_table(story: list[Flowable], invoice: Invoice) -> None:
    """Add the items table."""
    header = ["Descripción", "Cantidad", "Precio Unitario", "Subtotal"]
    table_data = [header]

    for item in invoice.items:
        table_data.append(
            [
                item.description,
                str(item.quantity),
                f"${item.unit_price:,.2f}",
                f"${item.subtotal:,.2f}",
            ]
        )

    col_widths = [3 * inch, 0.8 * inch, 1.4 * inch, 1.3 * inch]
    items_table = Table(table_data, colWidths=col_widths)
    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(config.COLOR_PRIMARY)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(config.COLOR_WHITE)),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor(config.COLOR_BG_ALT)),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(config.COLOR_BORDER)),
                ("LINEBELOW", (0, 0), (-1, 0), 1.5, colors.HexColor(config.COLOR_PRIMARY)),
            ]
        )
    )
    story.append(items_table)


def _add_totals(story: list[Flowable], invoice: Invoice) -> None:
    """Add subtotal, IVA, and total rows."""
    totals_data = [
        ["Subtotal:", f"${float(invoice.subtotal):,.2f}"],
        [f"IVA {config.IVA_RATE * 100:.0f}%:", f"${float(invoice.iva_amount):,.2f}"],
        ["TOTAL:", f"${float(invoice.total):,.2f}"],
    ]

    totals_table = Table(totals_data, colWidths=[5.2 * inch, 1.3 * inch])
    totals_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -2), "Helvetica"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("TEXTCOLOR", (0, -1), (-1, -1), colors.HexColor(config.COLOR_ACCENT)),
                ("FONTSIZE", (0, -1), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor(config.COLOR_TEXT)),
            ]
        )
    )
    story.append(totals_table)


def _add_footer(story: list[Flowable], style: ParagraphStyle) -> None:
    """Add footer with business info."""
    footer_text = (
        f"{config.BUSINESS_NAME}<br/>"
        f"RFC: {config.BUSINESS_RFC}<br/>"
        f"{config.BUSINESS_ADDRESS}<br/>"
        f"{config.BUSINESS_EMAIL}"
    )
    story.append(Paragraph(footer_text, style))
