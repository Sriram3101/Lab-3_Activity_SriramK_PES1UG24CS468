"""Greedy peer-to-peer settlement for group-trip balances.

Finding the true minimum number of transactions is NP-hard, so this greedy
approach is an approximation. It runs in O(n log n), meeting the target of
under 100 ms for 50 travelers and 500 expenses.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import random
from time import perf_counter


@dataclass(frozen=True)
class Payment:
	"""A positive payment from one traveler to another."""

	payer: str
	payee: str
	amount: int

	def __post_init__(self) -> None:
		if type(self.amount) is not int:
			raise TypeError("Payment amount must be an integer")
		if self.amount <= 0:
			raise ValueError("Payment amount must be positive")


def _validate_balances(balances: dict[str, int]) -> None:
	"""Raise TypeError if any balance is not an integer."""
	if any(type(amount) is not int for amount in balances.values()):
		raise TypeError("Balances must be integers")


def compute_settlement(balances: dict[str, int]) -> list[Payment]:
	"""Return deterministic payments that settle all zero-sum balances.

	Positive balances are creditors and negative balances are debtors.
	Example: ``compute_settlement({"A": 40, "B": -40})`` returns one payment.
	"""
	_validate_balances(balances)
	if sum(balances.values()) != 0:
		raise ValueError("Balances do not sum to zero")

	creditors = {name: amount for name, amount in balances.items() if amount > 0}
	debtors = {name: amount for name, amount in balances.items() if amount < 0}
	payments: list[Payment] = []

	# Pair exact opposites first; sorted IDs make duplicate matches deterministic.
	creditor_ids: dict[int, list[str]] = {}
	for name, amount in creditors.items():
		creditor_ids.setdefault(amount, []).append(name)
	for names in creditor_ids.values():
		names.sort()
	matched_indices: dict[int, int] = {}
	for debtor in sorted(debtors):
		amount = -debtors[debtor]
		names = creditor_ids.get(amount, [])
		index = matched_indices.get(amount, 0)
		if index < len(names):
			payee = names[index]
			matched_indices[amount] = index + 1
			creditors.pop(payee)
			payments.append(Payment(debtor, payee, amount))
	matched_debtors = {payment.payer for payment in payments}
	debtors = {name: amount for name, amount in debtors.items() if name not in matched_debtors}

	debtor_heap = [(-abs(amount), name) for name, amount in debtors.items()]
	creditor_heap = [(-amount, name) for name, amount in creditors.items()]
	heapq.heapify(debtor_heap)
	heapq.heapify(creditor_heap)

	while debtor_heap and creditor_heap:
		neg_debt, payer = heapq.heappop(debtor_heap)
		neg_credit, payee = heapq.heappop(creditor_heap)
		amount = min(-neg_debt, -neg_credit)
		payments.append(Payment(payer, payee, amount))

		debt_left = -neg_debt - amount
		credit_left = -neg_credit - amount
		if debt_left:
			heapq.heappush(debtor_heap, (-debt_left, payer))
		if credit_left:
			heapq.heappush(creditor_heap, (-credit_left, payee))

	return sorted(payments, key=lambda payment: (payment.payer, payment.payee, payment.amount))


def apply_payment(balances: dict[str, int], payment: Payment) -> dict[str, int]:
	"""Return a new balance mapping with ``payment`` applied.

	Example: applying ``Payment("A", "B", 10)`` adds 10 to A and subtracts
	10 from B.
	"""
	_validate_balances(balances)
	if type(payment.amount) is not int:
		raise TypeError("Payment amount must be an integer")
	if payment.amount <= 0:
		raise ValueError("Payment amount must be positive")
	result = dict(balances)
	result[payment.payer] = result.get(payment.payer, 0) + payment.amount
	result[payment.payee] = result.get(payment.payee, 0) - payment.amount
	return result


def verify_settlement(balances: dict[str, int], payments: list[Payment]) -> bool:
	"""Return True if applying all payments leaves every balance at zero.

	Example: ``verify_settlement({"A": 10, "B": -10}, [Payment("B", "A", 10)])``
	returns ``True``.
	"""
	current = dict(balances)
	for payment in payments:
		current = apply_payment(current, payment)
	return all(amount == 0 for amount in current.values())


def net_balances(paid: dict[str, int], owed: dict[str, int]) -> dict[str, int]:
	"""Return paid minus owed for every traveler in either mapping.

	Example: ``net_balances({"A": 20}, {"A": 5, "B": 3})`` returns
	``{"A": 15, "B": -3}``.
	"""
	_validate_balances(paid)
	_validate_balances(owed)
	travelers = paid.keys() | owed.keys()
	return {name: paid.get(name, 0) - owed.get(name, 0) for name in travelers}


if __name__ == "__main__":
	balances = {"A": 60, "B": 20, "C": -50, "D": -30}
	payments = compute_settlement(balances)
	assert len(payments) == 3
	assert verify_settlement(balances, payments)

	exact_balances = {"A": 40, "B": -40}
	exact_payments = compute_settlement(exact_balances)
	assert len(exact_payments) == 1
	assert verify_settlement(exact_balances, exact_payments)

	try:
		compute_settlement({"A": 10})
	except ValueError:
		pass
	else:
		raise AssertionError("Expected ValueError for non-zero total")

	try:
		compute_settlement({"A": 1.5, "B": -1.5})  # type: ignore[dict-item]
	except TypeError:
		pass
	else:
		raise AssertionError("Expected TypeError for float balances")

	rng = random.Random(0)
	for _ in range(1_000):
		count = rng.randint(2, 50)
		values = [rng.randint(-10_000, 10_000) for _ in range(count - 1)]
		values.append(-sum(values))
		case = {f"T{index:02d}": value for index, value in enumerate(values)}
		case_payments = compute_settlement(case)
		nonzero_count = sum(value != 0 for value in case.values())
		assert verify_settlement(case, case_payments)
		assert len(case_payments) <= nonzero_count - 1

	performance_balances = {f"T{index:02d}": index - 24 for index in range(50)}
	performance_balances["T49"] -= sum(performance_balances.values())
	start = perf_counter()
	compute_settlement(performance_balances)
	assert perf_counter() - start < 0.1

	print("All checks passed")
