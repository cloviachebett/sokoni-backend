
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.models.bill import Bill
from app.schemas.till import CheckoutIn, ItemIn, ReceiptOut, SessionOut
from app.services.errors import (
    InsufficientPaymentError,
    SessionNotFoundError,
    ValidationError,
)
from app.services.till_service import till_service

router = APIRouter(prefix="/till", tags=["till"])


def _session_out(bill: Bill) -> SessionOut:
    return SessionOut(session_id=bill.id, items=bill.items, running_total=bill.total)


@router.post("/sessions", response_model=SessionOut)
def start_session():
    bill = till_service.start_bill()
    return _session_out(bill)


@router.post("/sessions/{session_id}/items", response_model=SessionOut)
def add_item(session_id: str, item: ItemIn):
    try:
        bill = till_service.add_item(session_id, item.price)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found.")
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return _session_out(bill)


@router.post("/sessions/{session_id}/checkout", response_model=ReceiptOut)
def checkout(session_id: str, payload: CheckoutIn):
    try:
        return till_service.checkout(session_id, payload.cash_paid)
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found.")
    except InsufficientPaymentError as exc:
        raise HTTPException(status_code=402, detail=str(exc))
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("/receipt", response_class=PlainTextResponse)
def get_receipt():
    path = till_service._receipts_dir / "receipt.txt"
    if not path.exists():
        raise HTTPException(status_code=404, detail="No receipt yet.")
    return path.read_text(encoding="utf-8")
