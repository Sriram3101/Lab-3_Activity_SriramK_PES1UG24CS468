"""Compute deterministic peer-to-peer payments that settle traveler balances.

Finding the true minimum number of transactions is NP-hard, so this module uses
a greedy approximation. The implementation runs in O(n log n), meeting the
target of under 100 ms for 50 travelers and 500 expenses.

Example:
    >>> payments = compute_settlement({"A": 60, "B": 20, "C": -50, "D": -30})
    >>> verify_settlement({"A": 60, "B": 20, "C": -50, "D": -30}, payments)
    True
"""

from dataclasses import dataclass
import heapq
import random
from time import perf_counter


@dataclass(frozen=True)
class Payment:
    """A positive amount transferred from a payer to a payee.

    Example:
        >>> Payment("Alice", "Bob", 250)
        Payment(payer='Alice', payee='Bob', amount=250)
    """

    payer: str
    payee: str
    amount: int

    def __post_init__(self) -> None:
        if type(self.amount) is not int:
            raise TypeError("Payment amount must be an integer")


def _validate_balances(balances: dict[str, int]) -> None:
    """Raise TypeError unless every balance is an integer (not a bool)."""
    if any(type(balance) is not int for balance in balances.values()):
        raise TypeError("Balances must be integers")


def compute_settlement(balances: dict[str, int]) -> list[Payment]:
    """Return deterministic payments that bring all balances to zero.

    Positive balances are creditors; negative balances are debtors. Exact
    opposites are paired first, then the largest remaining debtor and creditor
    are settled greedily.

    Example:
        >>> payments = compute_settlement({"Alice": 40, "Bob": -40})
        >>> payments
        [Payment(payer='Bob', payee='Alice', amount=40)]
    """
    _validate_balances(balances)
    if sum(balances.values()) != 0:
        raise ValueError("Balances do not sum to zero")

    creditors_by_amount: dict[int, list[str]] = {}
    debtors_by_amount: dict[int, list[str]] = {}
    for traveler, balance in balances.items():
        if balance > 0:
            creditors_by_amount.setdefault(balance, []).append(traveler)
        elif balance < 0:
            debtors_by_amount.setdefault(-balance, []).append(traveler)

    payments: list[Payment] = []
    remaining_creditors: list[tuple[int, str]] = []
    remaining_debtors: list[tuple[int, str]] = []

    for amount in sorted(set(creditors_by_amount) | set(debtors_by_amount)):
        creditors = sorted(creditors_by_amount.get(amount, []))
        debtors = sorted(debtors_by_amount.get(amount, []))
        matched = min(len(creditors), len(debtors))
        for index in range(matched):
            payments.append(Payment(debtors[index], creditors[index], amount))
        for traveler in creditors[matched:]:
            heapq.heappush(remaining_creditors, (-amount, traveler))
        for traveler in debtors[matched:]:
            heapq.heappush(remaining_debtors, (-amount, traveler))

    while remaining_debtors and remaining_creditors:
        negative_debt, debtor = heapq.heappop(remaining_debtors)
        negative_credit, creditor = heapq.heappop(remaining_creditors)
        debt = -negative_debt
        credit = -negative_credit
        amount = min(debt, credit)
        payments.append(Payment(debtor, creditor, amount))

        if debt > amount:
            heapq.heappush(remaining_debtors, (-(debt - amount), debtor))
        if credit > amount:
            heapq.heappush(remaining_creditors, (-(credit - amount), creditor))

    return sorted(payments, key=lambda payment: (
        payment.payer,
        payment.payee,
        payment.amount,
    ))


def apply_payment(balances: dict[str, int], payment: Payment) -> dict[str, int]:
    """Apply a payment to a copy of balances and return the new mapping.

    A payer's balance increases and a payee's balance decreases.

    Example:
        >>> apply_payment({"Alice": -25, "Bob": 25}, Payment("Alice", "Bob", 25))
        {'Alice': 0, 'Bob': 0}
    """
    _validate_balances(balances)
    if type(payment.amount) is not int:
        raise TypeError("Payment amount must be an integer")
    if payment.amount <= 0:
        raise ValueError("Payment amount must be positive")

    updated = balances.copy()
    updated[payment.payer] = updated.get(payment.payer, 0) + payment.amount
    updated[payment.payee] = updated.get(payment.payee, 0) - payment.amount
    return updated


def verify_settlement(balances: dict[str, int], payments: list[Payment]) -> bool:
    """Return whether applying all payments leaves every balance at zero.

    Example:
        >>> verify_settlement(
        ...     {"Alice": 40, "Bob": -40},
        ...     [Payment("Bob", "Alice", 40)],
        ... )
        True
    """
    _validate_balances(balances)
    current = balances.copy()
    for payment in payments:
        current = apply_payment(current, payment)
    return all(balance == 0 for balance in current.values())


def net_balances(paid: dict[str, int], owed: dict[str, int]) -> dict[str, int]:
    """Return paid minus owed for each traveler appearing in either mapping.

    Example:
        >>> net_balances({"Alice": 100, "Bob": 20}, {"Alice": 30, "Carol": 5})
        {'Alice': 70, 'Bob': 20, 'Carol': -5}
    """
    _validate_balances(paid)
    _validate_balances(owed)
    travelers = paid.keys() | owed.keys()
    return {
        traveler: paid.get(traveler, 0) - owed.get(traveler, 0)
        for traveler in sorted(travelers)
    }


if __name__ == "__main__":
    example_balances = {"A": 60, "B": 20, "C": -50, "D": -30}
    example_payments = compute_settlement(example_balances)
    assert len(example_payments) == 3
    assert verify_settlement(example_balances, example_payments)

    opposite_payments = compute_settlement({"A": 40, "B": -40})
    assert len(opposite_payments) == 1

    try:
        compute_settlement({"A": 10, "B": -5})
    except ValueError as error:
        assert str(error) == "Balances do not sum to zero"
    else:
        raise AssertionError("Expected ValueError for non-zero total")

    try:
        compute_settlement({"A": 1.5, "B": -1.5})  # type: ignore[dict-item]
    except TypeError:
        pass
    else:
        raise AssertionError("Expected TypeError for float balances")

    random.seed(0)
    for _ in range(1_000):
        traveler_count = random.randint(2, 50)
        generated = {
            f"traveler-{index:02d}": random.choice((-1, 1)) * random.randint(1, 1_000)
            for index in range(traveler_count - 1)
        }
        generated[f"traveler-{traveler_count - 1:02d}"] = -sum(generated.values())
        generated_payments = compute_settlement(generated)
        assert verify_settlement(generated, generated_payments)
        nonzero_count = sum(balance != 0 for balance in generated.values())
        assert len(generated_payments) <= nonzero_count - 1

    benchmark_balances = {
        f"traveler-{index:02d}": (index + 1) if index < 25 else -(index - 24)
        for index in range(50)
    }
    benchmark_balances["traveler-49"] -= sum(benchmark_balances.values())
    started = perf_counter()
    compute_settlement(benchmark_balances)
    assert perf_counter() - started < 0.1

    print("All checks passed")