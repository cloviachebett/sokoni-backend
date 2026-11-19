

from typing import Dict, List

from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    """A single item price submitted by the cashier."""
    price: float = Field(..., description="Price of the item in shillings")


class SessionOut(BaseModel):
    """State returned to the client after each action on a bill."""
    session_id: str
    items: List[float]
    running_total: float


class CheckoutIn(BaseModel):
    """Cash handed over by the customer at checkout."""
    cash_paid: float


class ChangeBreakdown(BaseModel):
    """Fewest-notes-and-coins breakdown of the change owed."""
    denominations: Dict[int, int]  # denomination -> count
    change_due: float


class ReceiptOut(BaseModel):
    """Full result of a completed sale."""
    session_id: str
    items: List[float]
    total_bill: float
    cash_paid: float
    change: ChangeBreakdown
    receipt_text: str
