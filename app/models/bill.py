
import uuid
from typing import List

DENOMINATIONS: List[int] = [1000, 500, 200, 100, 50, 20, 10, 5, 1]


class Bill:
    """A single customer's running bill."""

    def __init__(self) -> None:
        self.id: str = str(uuid.uuid4())
        self.items: List[float] = []
        self.closed: bool = False

    @property
    def total(self) -> float:
        return round(sum(self.items), 2)

    def add_item(self, price: float) -> None:
        self.items.append(round(price, 2))
