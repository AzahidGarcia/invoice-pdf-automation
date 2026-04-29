"""CSV reading and validation with pandas."""

from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import ValidationError

from invoice_automation.models import Invoice, InvoiceItem


class CSVReadError(Exception):
    """Raised when CSV reading or validation fails."""


def read_invoices_from_csv(csv_path: str | Path) -> list[Invoice]:
    """
    Read invoices from a CSV file and validate them.

    Expected CSV columns:
    - invoice_id, client_name, client_rfc, issue_date, due_date, category
    - items: semicolon-separated "description|quantity|unit_price" groups
      (multiple items separated by ;;)

    Example:
    invoice_id,client_name,client_rfc,issue_date,due_date,items,category
    FAC-001,Cliente 001,XAXX010101000,2026-04-01,2026-04-15,"Cuaderno profesional|2|85.00;;Plumas azul|10|12.50",Papelería
    """
    path = Path(csv_path)
    if not path.exists():
        raise CSVReadError(f"File not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise CSVReadError(f"Failed to parse CSV: {e}") from e

    required_cols = {"invoice_id", "client_name", "client_rfc", "issue_date", "items"}
    missing = required_cols - set(df.columns)
    if missing:
        raise CSVReadError(f"Missing required columns: {missing}")

    invoices: list[Invoice] = []
    errors: list[str] = []

    for row_num, (_, row) in enumerate(df.iterrows(), start=2):
        try:
            invoice = _parse_row(row)
            invoices.append(invoice)
        except ValidationError as e:
            errors.append(f"Row {row_num}: {e}")

    if errors:
        raise CSVReadError("Validation errors:\n" + "\n".join(errors))

    return invoices


def _parse_row(row: Any) -> Invoice:
    """Parse a single CSV row into an Invoice."""
    items_str = str(row.get("items", ""))
    items = _parse_items(items_str)

    due_date: Any = row.get("due_date")
    if pd.isna(due_date) or due_date == "":
        due_date = None
    else:
        due_date = pd.to_datetime(due_date).date()

    return Invoice(
        invoice_id=str(row["invoice_id"]),
        client_name=str(row["client_name"]),
        client_rfc=str(row["client_rfc"]),
        issue_date=pd.to_datetime(row["issue_date"]).date(),
        due_date=due_date,
        items=items,
        category=str(row.get("category", "General")),
    )


def _parse_items(items_str: str) -> list[InvoiceItem]:
    """
    Parse items string into InvoiceItem list.

    Format: "description|quantity|unit_price;;description|quantity|unit_price"
    """
    if not items_str or items_str == "nan":
        raise ValueError("No items provided")

    items: list[InvoiceItem] = []
    item_strs = items_str.split(";;")

    for item_str in item_strs:
        item_str = item_str.strip()
        if not item_str:
            continue
        parts = item_str.split("|")
        if len(parts) != 3:
            raise ValueError(
                f"Item must have 3 parts (desc|qty|price), got: {item_str}"
            )
        description, qty_str, price_str = parts
        items.append(
            InvoiceItem(
                description=description.strip(),
                quantity=int(qty_str.strip()),
                unit_price=float(price_str.strip()),
            )
        )
    return items
