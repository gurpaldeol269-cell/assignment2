"""Object-oriented prototype for the staff purchase requisition system."""

from __future__ import annotations

from typing import Iterable


_NEXT_REQUISITION_NUMBER = 1


class Requisition:
    """Stores one requisition and provides its main operations."""

    _requisitions: list["Requisition"] = []

    def __init__(self) -> None:
        """Initialize the shared data for one requisition."""
        global _NEXT_REQUISITION_NUMBER

        self.date = ""
        self.staff_id = ""
        self.staff_name = ""
        self.requisition_id = str(10000 + _NEXT_REQUISITION_NUMBER)
        self.items: list[tuple[str, float]] = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference: str | None = None
        _NEXT_REQUISITION_NUMBER += 1
        self._requisitions.append(self)

    def add_requisition(
        self,
        date: str | None = None,
        staff_id: str | None = None,
        staff_name: str | None = None,
        items: Iterable[tuple[str, float]] | None = None,
    ) -> float:
        """Capture requisition details and return the calculated total.

        When arguments are omitted, details are collected using ``input``.
        Supplying arguments makes the method easy to test and allows a caller
        to provide a prepared list of item names and prices.
        """
        self.date = date if date is not None else input("Date: ").strip()
        self.staff_id = (
            staff_id if staff_id is not None else input("Staff ID: ").strip()
        )
        self.staff_name = (
            staff_name if staff_name is not None else input("Staff Name: ").strip()
        )

        if items is None:
            self.items = self._read_items()
        else:
            self.items = self._validate_items(items)

        self.total = round(sum(price for _, price in self.items), 2)
        return self.total

    def requisitions_details(self) -> float:
        """Return the current requisition total for approval decisions."""
        return self.total

    def approve_requisition(self) -> tuple[str, str | None]:
        """Approve totals below $500 and keep larger totals pending."""
        self.approval_reference = None

        if self.requisitions_details() < 500:
            self.status = "Approved"
            self.approval_reference = (
                f"{self.staff_id}{self.requisition_id[-3:]}"
            )
        else:
            self.status = "Pending"

        return self.status, self.approval_reference

    def respond_to_requisition(self, response: str) -> str:
        """Allow a manager to approve or reject a pending requisition."""
        if self.status != "Pending":
            raise ValueError("Only pending requisitions can receive a response.")

        normalized_response = response.strip().lower()
        if normalized_response == "approved":
            self.status = "Approved"
            self.approval_reference = f"{self.staff_id}{self.requisition_id[-3:]}"
        elif normalized_response in {"not approved", "notapproved"}:
            self.status = "Not approved"
            self.approval_reference = None
        else:
            raise ValueError("Response must be Approved or Not approved.")

        return self.status

    def display_requisitions(self) -> None:
        """Display the requisition details and approval information."""
        print("\nPrinting requisition:")
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: ${self.total:.2f}")
        print(f"Status: {self.status}")
        print(
            "Approval Reference Number: "
            f"{self.approval_reference or 'Not available'}"
        )

    @classmethod
    def display_all_requisitions(cls) -> None:
        """Display every requisition created during this program run."""
        for requisition in cls._requisitions:
            requisition.display_requisitions()

    @classmethod
    def requisition_statistics(cls) -> dict[str, int]:
        """Return counts of submitted requisitions grouped by status."""
        statistics = {
            "total": len(cls._requisitions),
            "approved": 0,
            "pending": 0,
            "not approved": 0,
        }
        for requisition in cls._requisitions:
            statistics[requisition.status.lower()] += 1
        return statistics

    @classmethod
    def display_statistics(cls) -> None:
        """Display requisition statistics on the console."""
        statistics = cls.requisition_statistics()
        print("\nDisplaying the Requisition Statistics")
        print(
            "The total number of requisitions submitted: "
            f"{statistics['total']}"
        )
        print(
            "The total number of approved requisitions: "
            f"{statistics['approved']}"
        )
        print(
            "The total number of pending requisitions: "
            f"{statistics['pending']}"
        )
        print(
            "The total number of not approved requisitions: "
            f"{statistics['not approved']}"
        )

    @staticmethod
    def _read_items() -> list[tuple[str, float]]:
        """Read at least one item and its price from the console."""
        captured_items: list[tuple[str, float]] = []

        while True:
            item_name = input("Item Name: ").strip()
            if not item_name:
                print("Item name cannot be empty.")
                continue

            while True:
                try:
                    item_price = float(input("Item Price ($): "))
                    if item_price < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Enter a non-negative numeric price.")

            captured_items.append((item_name, item_price))
            another_item = input("Add another item (yes/no): ").strip().lower()
            if another_item != "yes":
                return captured_items

    @staticmethod
    def _validate_items(
        items: Iterable[tuple[str, float]],
    ) -> list[tuple[str, float]]:
        """Validate prepared item data before calculating the total."""
        validated_items: list[tuple[str, float]] = []

        for item_name, item_price in items:
            if not item_name.strip():
                raise ValueError("Item names cannot be empty.")
            if item_price < 0:
                raise ValueError("Item prices cannot be negative.")
            validated_items.append((item_name.strip(), float(item_price)))

        if not validated_items:
            raise ValueError("A requisition must contain at least one item.")

        return validated_items


def main() -> None:
    """Create and display example requisitions for testing."""
    requisitions = [
        ("03/04/2024", "FN19", "John Paul", [("Coffee", 200), ("Paper", 100)]),
        ("04/04/2024", "FN20", "Alex Smith", [("Laptop", 750)]),
        ("07/05/2024", "FN15", "Emma Wellington", [("Equipment", 3500)]),
        ("03/05/2024", "FN02", "Catlin White", [("Stationery", 490)]),
        ("08/05/2024", "FN21", "Jordan Lee", [("Desk", 500)]),
    ]

    submitted = []
    for date, staff_id, staff_name, items in requisitions:
        requisition = Requisition()
        requisition.add_requisition(date, staff_id, staff_name, items)
        requisition.approve_requisition()
        submitted.append(requisition)

    Requisition.display_statistics()

    submitted[1].respond_to_requisition("Approved")
    submitted[2].respond_to_requisition("Not approved")
    submitted[4].respond_to_requisition("Approved")

    Requisition.display_all_requisitions()
    Requisition.display_statistics()


if __name__ == "__main__":
    main()
