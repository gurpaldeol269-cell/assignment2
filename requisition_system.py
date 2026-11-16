"""
Requisition System Prototype
Assessment 2: Software Development Project
"""

# Global counter to generate unique Requisition IDs starting at 10001
next_requisition_id = 10001


class Requisition:
    """Class to manage purchase requisitions."""

    # Class list to track all created requisition objects
    all_requisitions = []

    def __init__(self):
        """Initialize the shared data for a requisition."""
        global next_requisition_id

        self.date = ""
        self.staff_id = ""
        self.staff_name = ""
        self.requisition_id = str(next_requisition_id)
        next_requisition_id += 1

        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference = "Not available"

        # Track this requisition in the shared list
        Requisition.all_requisitions.append(self)

    def add_requisition(self, date=None, staff_id=None, staff_name=None, items=None):
        """Submit basic information and a list of items with costs, then return the total."""
        self.date = date if date is not None else input("Enter Date: ")
        self.staff_id = staff_id if staff_id is not None else input("Enter Staff ID: ")
        self.staff_name = staff_name if staff_name is not None else input("Enter Staff Name: ")

        if items is not None:
            self.items = items
        else:
            self.items = []
            while True:
                name = input("Item Name (or press Enter to finish): ").strip()
                if not name:
                    break
                price = float(input(f"Cost of {name}: "))
                self.items.append((name, price))

        # Calculate the total cost of all items
        self.total = sum(cost for _, cost in self.items)
        return self.total

    def requisitions_details(self):
        """Return the total cost of the requisition for approval decisions."""
        return self.total

    def approve_requisition(self):
        """Automatically approve requisitions below $500, or keep them pending."""
        # Only evaluate if the status has not already been finalized by a manager
        if self.status in ["Approved", "Not approved"]:
            return self.status, self.approval_reference

        total = self.requisitions_details()

        if total < 500:
            self.status = "Approved"
            # Reference number: Staff ID + last 3 digits of Requisition ID
            self.approval_reference = f"{self.staff_id}{self.requisition_id[-3:]}"
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

        return self.status, self.approval_reference

    def respond_to_requisition(self, response):
        """Allow a manager to respond to a pending requisition with Approved or Not approved."""
        if self.status != "Pending":
            print(f"Requisition {self.requisition_id} is not pending.")
            return self.status

        clean_response = response.strip().lower()

        if clean_response == "approved":
            self.status = "Approved"
            self.approval_reference = f"{self.staff_id}{self.requisition_id[-3:]}"
        elif clean_response in ["not approved", "notapproved"]:
            self.status = "Not approved"
            self.approval_reference = "Not available"
        else:
            print("Invalid response. Must be 'Approved' or 'Not approved'.")

        return self.status

    def display_requisition(self):
        """Display details for this individual requisition."""
        total_str = f"${int(self.total)}" if self.total.is_integer() else f"${self.total:.2f}"

        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: {total_str}")
        print(f"Status: {self.status}")
        print(f"Approval Reference Number: {self.approval_reference}\n")

    @classmethod
    def display_requisitions(cls):
        """Print information for all requisition objects."""
        for req in cls.all_requisitions:
            req.display_requisition()

    @classmethod
    def requisition_statistics(cls):
        """Calculate and return statistical information about all requisitions."""
        total_submitted = len(cls.all_requisitions)
        approved_count = 0
        pending_count = 0
        not_approved_count = 0

        for req in cls.all_requisitions:
            if req.status == "Approved":
                approved_count += 1
            elif req.status == "Pending":
                pending_count += 1
            elif req.status == "Not approved":
                not_approved_count += 1

        stats = {
            "total": total_submitted,
            "approved": approved_count,
            "pending": pending_count,
            "not_approved": not_approved_count,
        }
        return stats

    @classmethod
    def display_statistics(cls):
        """Display the requisition statistics on the console."""
        stats = cls.requisition_statistics()
        print("Displaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {stats['total']}")
        print(f"The total number of approved requisitions: {stats['approved']}")
        print(f"The total number of pending requisitions: {stats['pending']}")
        print(f"The total number of not approved requisitions: {stats['not_approved']}\n")


def main():
    """Test the requisition system with at least 5 different scenarios."""
    test_data = [
        ("03/04/2024", "FN19", "John Paul", [("Office Supplies", 450.0)]),
        ("05/04/2024", "FN20", "Tracy Brown", [("Laptop", 1000.0)]),
        ("07/05/2024", "FN15", "Emma Wellington", [("Projector", 3500.0)]),
        ("03/05/2024", "FN02", "Catlin White", [("Stationery", 490.0)]),
        ("08/05/2024", "FN21", "Jordan Lee", [("Desk & Chair", 500.0)]),
    ]

    submitted_requisitions = []

    # 1. Submit at least 5 requisitions (< $500 and >= $500)
    for date, staff_id, staff_name, items in test_data:
        req = Requisition()
        req.add_requisition(date, staff_id, staff_name, items)
        req.approve_requisition()
        submitted_requisitions.append(req)

    # 2. Display initial requisition statistics
    Requisition.display_statistics()

    # 3. Manager responds to requisitions that are >= $500 (greater than $499)
    # Requisition 10002 ($1000) -> Approved by manager
    submitted_requisitions[1].respond_to_requisition("Approved")

    # Requisition 10003 ($3500) -> Not approved by manager
    submitted_requisitions[2].respond_to_requisition("Not approved")

    # Requisition 10005 ($500) -> Left as Pending (proves $500 boundary stays pending)

    # 4. Display all requisitions and updated statistics
    Requisition.display_requisitions()
    Requisition.display_statistics()


if __name__ == "__main__":
    main()
