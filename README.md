# Requisition System Prototype

This prototype implements the Assignment 2 requirements using a
`Requisition` class.

## Run the test examples

```text
python requisition_system.py
```

The program creates two requisitions:

- a total below `$500`, which becomes `Approved` and receives an approval
  reference;
- a total of `$500` or more, which remains `Pending`.

The `add_requisition` method can also be called without arguments to collect
details interactively from the user.
