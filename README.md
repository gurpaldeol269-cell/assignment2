# BACT7501 Assessment 2: Requisition System Prototype

This repository contains an object-oriented Python prototype for a staff purchase requisition system developed as part of **Assessment 2: Software Development Project**.

---

## Overview

The system allows staff members to submit purchase requisitions, automatically approves requisitions below $500, keeps requisitions of $500 or more pending for managerial approval, and tracks real-time statistics.

### Key Features
- **Object-Oriented Design**: Encapsulates all data and operations within the `Requisition` class.
- **Unique Identification**: Generates sequential IDs starting at `10001` using an external counter.
- **Automatic Approval**: Requisitions with a total below `$500` are automatically approved with an approval reference number (`<Staff_ID><last 3 digits of Requisition_ID>`).
- **Manager Response**: Pending requisitions can be reviewed and marked as `Approved` or `Not approved`.
- **Statistics Tracking**: Tracks the total submitted, approved, pending, and not approved requisitions dynamically.

---

## Design Principles Applied

1. **Encapsulation**: State (`date`, `staff_id`, `items`, `total`, `status`, `approval_reference`) and behaviors (`add_requisition`, `approve_requisition`, `respond_to_requisition`, etc.) are bundled inside the `Requisition` class.
2. **Single Responsibility Principle (SRP)**: Each method performs one dedicated function (e.g., `requisitions_details` computes and returns the total, while `approve_requisition` evaluates the business rule).
3. **Don't Repeat Yourself (DRY)**: Centralized formatting and display logic prevent code duplication.

---

## How to Run

Ensure you have Python 3.10+ installed. Run the script directly from your terminal:

```bash
python requisition_system.py
```

### Test Scenarios Included in `main()`
The program automatically executes 5 test cases covering boundary values:
1. `10001` - $450 (under $500 -> Auto-approved with reference `FN19001`)
2. `10002` - $1000 (>= $500 -> Pending -> Manager responds `Approved` with reference `FN20002`)
3. `10003` - $3500 (>= $500 -> Pending -> Manager responds `Not approved`)
4. `10004` - $490 (under $500 -> Auto-approved with reference `FN02004`)
5. `10005` - $500 (boundary value -> Stays `Pending`)
