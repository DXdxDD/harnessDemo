from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class OrderItem:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class PriceResult:
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal


def money(value: Decimal | int | str | float) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_order_total(
    items: list[OrderItem],
    coupon: str | None = None,
    tax_rate: Decimal = Decimal("0.08"),
) -> PriceResult:
    if not items:
        raise ValueError("order must contain at least one item")

    subtotal = sum((item.unit_price * item.quantity for item in items), Decimal("0"))
    subtotal = money(subtotal)

    discount = _calculate_discount(subtotal, coupon)
    taxable_amount = subtotal - discount
    tax = money(taxable_amount * tax_rate)
    total = money(taxable_amount + tax)

    return PriceResult(
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        total=total,
    )


def _calculate_discount(subtotal: Decimal, coupon: str | None) -> Decimal:
    if coupon is None:
        return Decimal("0.00")

    normalized = coupon.strip().upper()
    if normalized == "SAVE10":
        return money(subtotal * Decimal("0.10"))
    if normalized == "SAVE20" and subtotal >= Decimal("100.00"):
        return money(subtotal * Decimal("0.20"))
    if normalized == "MINUS5":
        return min(Decimal("5.00"), subtotal)

    return Decimal("0.00")
