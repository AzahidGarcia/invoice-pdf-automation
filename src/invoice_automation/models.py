"""Pydantic models for invoice data validation."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class InvoiceItem(BaseModel):
    """A single line item in an invoice."""

    description: Annotated[str, Field(min_length=1, max_length=200)]
    quantity: Annotated[int, Field(gt=0)]
    unit_price: Annotated[float, Field(gt=0)]

    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this item."""
        return round(self.quantity * self.unit_price, 2)

    model_config = {"frozen": True}


class Invoice(BaseModel):
    """Full invoice data."""

    invoice_id: Annotated[str, Field(min_length=1, max_length=50)]
    client_name: Annotated[str, Field(min_length=1, max_length=100)]
    client_rfc: Annotated[str, Field(min_length=10, max_length=20)]
    issue_date: date
    due_date: date | None = None
    items: list[InvoiceItem]
    category: Annotated[str, Field(max_length=50)] = "General"

    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal before VAT."""
        total = sum(item.subtotal for item in self.items)
        return Decimal(str(round(total, 2)))

    @property
    def iva_amount(self) -> Decimal:
        """Calculate VAT amount."""
        return Decimal(str(round(float(self.subtotal) * 0.16, 2)))

    @property
    def total(self) -> Decimal:
        """Calculate total including VAT."""
        return self.subtotal + self.iva_amount

    @field_validator("client_rfc")
    @classmethod
    def validate_rfc(cls, v: str) -> str:
        """Ensure RFC is uppercase."""
        return v.upper()

    model_config = {"frozen": True}
