

from pathlib import Path
from typing import Dict

from app.models.bill import DENOMINATIONS, Bill
from app.repositories.bill_repository import BillRepository, bill_repository
from app.schemas.till import ChangeBreakdown, ReceiptOut
from app.services.errors import (
    InsufficientPaymentError,
    SessionNotFoundError,
    ValidationError,
)


class TillService:
    def __init__(
        self, repository: BillRepository, receipts_dir: str = "receipts"
    ) -> None:
        self._repository = repository
        self._receipts_dir = Path(receipts_dir)
        self._receipts_dir.mkdir(parents=True, exist_ok=True)

    

    def start_bill(self) -> Bill:
        return self._repository.create()

    def get_bill(self, session_id: str) -> Bill:
        bill = self._repository.get(session_id)
        if bill is None:
            raise SessionNotFoundError(session_id)
        return bill

    def add_item(self, session_id: str, price: float) -> Bill:
        bill = self.get_bill(session_id)
        if price <= 0:
            raise ValidationError("Item price must be greater than zero.")
        bill.add_item(price)
        self._repository.save(bill)
        return bill

    # checkout 

    def checkout(self, session_id: str, cash_paid: float) -> ReceiptOut:
        bill = self.get_bill(session_id)
        if cash_paid < 0:
            raise ValidationError("Cash paid cannot be negative.")
        if cash_paid < bill.total:
            raise InsufficientPaymentError(
                f"Not enough cash: bill is {bill.total}, received {cash_paid}."
            )

        change_due = round(cash_paid - bill.total, 2)
        breakdown = self._breakdown_change(change_due)
        change = ChangeBreakdown(denominations=breakdown, change_due=change_due)

        receipt_text = self._format_receipt(bill, cash_paid, change)
        self._write_receipt(receipt_text)
        bill.closed = True
        self._repository.save(bill)

        return ReceiptOut(
            session_id=bill.id,
            items=bill.items,
            total_bill=bill.total,
            cash_paid=cash_paid,
            change=change,
            receipt_text=receipt_text,
        )

    

    @staticmethod
    def _breakdown_change(amount: float) -> Dict[int, int]:
       
        remaining = int(round(amount))
        breakdown: Dict[int, int] = {}
        for note in DENOMINATIONS:
            count, remaining = divmod(remaining, note)
            if count:
                breakdown[note] = count
        return breakdown

    @staticmethod
    def _format_receipt(bill: Bill, cash_paid: float, change: ChangeBreakdown) -> str:
        lines = ["SOKONI CHANGE-MAKER - RECEIPT", "-" * 32]
        for price in bill.items:
            lines.append(f"Item: {price:.2f}")
        lines.append("-" * 32)
        lines.append(f"Total bill: {bill.total:.2f}")
        lines.append(f"Amount paid: {cash_paid:.2f}")
        lines.append(f"Change due: {change.change_due:.2f}")
        lines.append("Change breakdown:")
        for note in DENOMINATIONS:
            count = change.denominations.get(note)
            if count:
                lines.append(f"  {note} x {count}")
        return "\n".join(lines) + "\n"

    def _write_receipt(self, text: str) -> None:
        (self._receipts_dir / "receipt.txt").write_text(text, encoding="utf-8")



till_service = TillService(bill_repository)
