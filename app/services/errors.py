"""Exceptions raised by the service layer. Routers translate these into
HTTP status codes; nothing here knows about FastAPI.
"""


class ValidationError(Exception):
    """Raised when an item price or cash amount fails validation."""


class InsufficientPaymentError(Exception):
    """Raised when the cash paid is less than the total bill."""


class SessionNotFoundError(Exception):
    """Raised when a session id does not exist."""
