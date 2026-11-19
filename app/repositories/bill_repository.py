

from typing import Dict, Optional

from app.models.bill import Bill


class BillRepository:
    def __init__(self) -> None:
        self._bills: Dict[str, Bill] = {}

    def create(self) -> Bill:
        bill = Bill()
        self._bills[bill.id] = bill
        return bill

    def get(self, session_id: str) -> Optional[Bill]:
        return self._bills.get(session_id)

    def save(self, bill: Bill) -> None:
        # No-op for the in-memory store (the object is already the one
        # held in self._bills), kept so a future DB-backed repository
        # has a natural place to persist changes.
        self._bills[bill.id] = bill


# Single shared instance - one physical till, one store of bills.
bill_repository = BillRepository()
