from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    cents: int = 0
    symbol: str = "€"
    cpu = 100  # cents per monetary unit

    @classmethod
    def euro(cls, amount: int | Decimal | float) -> "Money":
        return cls(int(amount * 100), "€")

    @property
    def float(self) -> float:
        return self.cents / self.cpu

    def __str__(self):
        return f"{self.float:,.2f}{self.symbol}"

    @property
    def gr(self):
        stv = str(self)
        return stv.replace(",", "X").replace(".", ",").replace("X", ".")

    @property
    def gr_(self):
        if self.cents == 0:
            return ""
        return self.gr

    def __add__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            return Money(self.cents + other.cents, self.symbol)

    def __sub__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            return Money(self.cents - other.cents, self.symbol)

    def __mul__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            return Money(int(self.cents * other.cents / self.cpu), self.symbol)

    def __truediv__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            return Money(int(self.cents / other.cents * self.cpu), self.symbol)
