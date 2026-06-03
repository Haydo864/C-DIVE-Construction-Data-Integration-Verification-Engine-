from pydantic import BaseModel, Field, field_validator
from typing import List

class InvoiceLineItem(BaseModel):
    description: str = Field(..., description="Description of the work or material")
    cost_code: str = Field(..., description="Multifamily cost code, e.g., '07-200' for Thermal/Moisture")
    amount: float = Field(..., description="Dollar amount for this specific line item")

class ConstructionInvoice(BaseModel):
    vendor_name: str
    invoice_date: str
    total_amount: float
    line_items: List[InvoiceLineItem]

    @field_validator('total_amount')
    def total_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Total amount must be greater than zero")
        return v