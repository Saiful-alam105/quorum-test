# Quorum PR Analysis — Test Notes

This document contains documentation only. It is used to demonstrate how the
Quorum system behaves when a pull request contains no Python source code.

## Purpose

Quorum is an AI-powered pull request analysis system. Given a pull request,
it can:

- detect security vulnerabilities in Python code
- recognize safe implementations
- generate unit tests for Python modules
- report coverage estimates
- summarize documentation-only changes
- handle non-Python files

This repository is used to demonstrate each of those capabilities with a
sequence of isolated pull requests.

## Security Testing

Several pull requests introduce code that intentionally contains security
vulnerabilities. The goal is to verify that Quorum:

1. identifies the vulnerable pattern (for example `shell=True`, `eval`,
   SQL string concatenation, `pickle.loads`, weak hashing, unsafe template
   rendering, and unsafe YAML loading)
2. points to the exact function and line where the issue exists
3. explains why the pattern is unsafe and how it could be exploited
4. suggests a safer alternative

Each security pull request is designed so that the vulnerable code is
obvious and easy for a scanner to find. The affected functions are named
clearly and the module docstring states that the code is intentionally
vulnerable.

## Safe Code Recognition

Other pull requests contain security-related code that is written safely:

- `subprocess.run` with argument lists and `shell=False`
- parameterized SQL queries using `?` placeholders
- `secrets`-based random tokens and salted password hashing

Quorum should recognize these implementations and report no findings, or
only informational comments. This distinguishes a security scanner from a
system that simply flags any use of security-adjacent APIs.

## Test Generation

A set of pull requests adds pure-Python utility modules without any tests.
Quorum is expected to:

- detect that these are pure, testable functions
- generate unit tests covering normal paths
- cover edge cases such as empty input and invalid values
- cover branches such as conditional logic and error handling
- produce tests that can run without external dependencies

## Pull Request Analysis Workflow

For each pull request in this repository, the expected flow is:

1. Push a branch with one isolated change.
2. Open a pull request against `main`.
3. Quorum analyzes the diff.
4. The teacher reviews the Quorum output.
5. The pull request is merged into `main`.

Because each pull request touches only its own files, branches can be merged
in any order without merge conflicts.

## Demonstration Scenarios

### 1. Security Vulnerability Detection

A pull request adds a module that uses `subprocess.call(..., shell=True)`
with user-supplied strings. Quorum should flag shell injection.

### 2. Safe-Code Recognition

A pull request adds a command runner that uses `subprocess.run` with
argument lists and no shell. Quorum should report no vulnerabilities.

### 3. Test Generation

A pull request adds a pure math utility module. Quorum should generate
unit tests for its functions.

### 4. Coverage Analysis

The generated tests should show coverage across function branches, edge
cases, and error handling.

### 5. Non-Python Files

A pull request adds a JavaScript file. Quorum should handle the language
appropriately rather than attempting to analyze it as Python.

### 6. Documentation Only

This very document is an example. A documentation-only pull request should
produce no Python security findings and no test generation.

### 7. Moved / Renamed Modules

A pull request adds a standalone calculator module that represents a
component that was relocated. Quorum should handle the new file as an
isolated change.

## Expected Behavior Summary

| Change type | Expected Quorum output |
| ----------- | ---------------------- |
| vulnerable Python | security findings |
| safe Python | no findings |
| pure Python module | generated tests |
| documentation only | summary, no code analysis |
| JavaScript file | non-Python handling |
| isolated new module | normal analysis |

## Notes

- Every branch is created from the latest `main`.
- No branch modifies files introduced by another branch.
- All code is written for demonstration purposes only.
- The vulnerable examples must not be deployed or executed against real
  systems.

This repository is a teaching demonstration. It is intentionally small,
focused, and conflict-free so that the Quorum analysis results are easy to
compare across pull requests.