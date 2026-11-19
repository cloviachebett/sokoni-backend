# Sokoni Change-Maker — Backend

FastAPI backend for the market-stall till. One item price at a time,
running total, cash-paid checkout, fewest-notes-and-coins change
breakdown, and a `receipts/receipt.txt` written on each completed sale.

## Run it

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs at `http://localhost:8000/docs`.

## Endpoints

| Method | Path                              | Purpose                                   |
|--------|-----------------------------------|--------------------------------------------|
| POST   | `/till/sessions`                  | Start a new bill                          |
| POST   | `/till/sessions/{id}/items`       | Add one item price, returns running total |
| POST   | `/till/sessions/{id}/checkout`    | Submit cash paid, get change + receipt    |
| GET    | `/till/receipt`                   | Fetch the last written receipt.txt        |

## Structure

- `app/schemas/till.py` — Pydantic request/response models (the API's I/O shape)
- `app/models/bill.py` — the plain `Bill` domain object + denomination list; no framework or storage code
- `app/repositories/bill_repository.py` — storage layer (in-memory dict); the only place that knows *how* bills are stored
- `app/services/till_service.py` — business logic: adding items, the change algorithm, receipt writing; depends on the repository, knows nothing about HTTP
- `app/services/errors.py` — service-layer exceptions
- `app/routers/till.py` — HTTP routing; translates service exceptions into status codes, no business logic
- `app/main.py` — app wiring, CORS

## Notes

- Bills are kept in memory via `BillRepository` (one till, no need for
  a database yet). To persist across restarts, write a new repository
  class with the same `create` / `get` / `save` interface and swap it
  into `TillService` — nothing above the repository layer changes.
- Change breakdown uses a greedy algorithm over `[1000, 500, 200, 100,
  50, 20, 10, 5, 1]`. Greedy is optimal for this denomination set.
- Validation: item price ≤ 0 → `422`; cash paid < total → `402` with a
  "not paid enough" message instead of a negative change.
