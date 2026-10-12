# Test Author Packet

Read this when an essential contract needs a test and the implementation exists: the packet is what a test author who has not seen the implementation receives. The author writes tests from the contract, so the tests check what callers rely on rather than what the code happens to do. Which contracts are essential, and how mismatches are reconciled, is in [correctness and verification](correctness-and-verification.md#tests).

## Contents

- Include
- Exclude
- Instructions to the author
- Example packet
- After the author returns

## Include

- **The interface contract.** The public names the tests call and their signatures in the language's notation, with parameter and return types; invariants, ordering, units, and side effects visible at the interface; and the import path or entry point.
- **Input and output examples.** Cases from the requirement, the documented contract, an independent calculation, or a reproduced bug, each marked normative (must hold) or illustrative. Include boundary cases the contract names.
- **Error behavior.** Which inputs are rejected, the error type or category the caller sees, and whether anything is written or sent before the error.
- **The verification split.** Which properties these tests own, which are covered by real-run checks, and which belong to evaluation, so the author does not assert on learned or judged quality. For each essential contract, the reason it is essential.
- **Seams where fakes are allowed.** The external I/O and model seams, with the controlled adapters that already exist (recorded or fake) and their interfaces.
- **Project test conventions.** The test runner, the directory and file naming, the fixture style, and the command that runs the tests.

## Exclude

- Implementation file paths, code, diffs, and private module or helper names.
- The implementer's own tests, scratch scripts, and commit messages that describe how the code works.
- Expected values obtained by running the implementation.

The author may read public documentation and the interface declaration file when it holds no implementation. When the language puts declarations and bodies in one file, copy the signatures and contract documentation into the packet instead of pointing to the file.

## Instructions to the author

- Call the public interface; use real collaborators inside the module.
- Fake only at the listed external I/O and model seams, using the listed controlled adapters where they exist.
- Do not assert on call order, call counts, or arguments passed between internal collaborators.
- Name each test for the behavior it checks; one behavior per test.
- Derive every expected value from the packet. When the packet does not determine a result, do not guess: list the case as a contract question in the reply.
- Return the tests, the command that runs them, the result of running them, and the list of contract questions.

## Example packet

Synthetic. A billing module splits an invoice total across cost centers.

```text
Interface: split_total(total: Money, shares: list[Share]) -> list[Allocation]
  Import:  billing.allocation
  Money:   amount in minor units (integer cents) plus a currency code
  Share:   cost_center id and a positive integer weight
Invariants:
  - Allocations appear in the order of shares.
  - Allocated amounts sum exactly to total.amount.
  - Each allocation is floor(total * weight / sum_of_weights); the remaining cents go
    one each to the earliest shares in input order.
Examples (normative):
  - 1000 cents, weights [1, 1, 1] -> [334, 333, 333]
  - 1000 cents, weights [2, 1]    -> [667, 333]
  - 0 cents, weights [5]          -> [0]
Errors:
  - Empty shares or a non-positive weight -> AllocationError(kind="invalid_shares"); nothing returned.
  - Mixed currencies are impossible by type; not tested.
Verification split:
  - This contract is essential because ledger totals depend on exact sums and the order is persisted.
  - Rounding display in reports is covered by the report's real-run check, not here.
Seams: none; the function is pure.
Conventions: pytest, tests/billing/test_allocation.py, run with `uv run --group test pytest tests/billing`.
```

## After the author returns

Run the tests against the implementation. Classify every failure as an implementation bug, a contract gap, or a bad test before editing either side, and settle each contract question the author listed the same way. Remove any test that only restates the implementation. Report which contracts now have tests, the command and its result, and whether the author was blind.
