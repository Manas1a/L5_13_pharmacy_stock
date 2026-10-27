# Lab 5 — Static Code Analysis Issues

## Project
Pharmacy Prescription & Stock Tracker

**Python File:** `pharmacy_system.py`

## Tools Used
- Pylint
- Bandit
- Flake8

## Identified Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL Injection (B608) | Security — Medium | 21–22 | SQL query was constructed using string formatting with patient input, creating a possible SQL injection vulnerability. | Replaced string formatting with parameterized SQL queries using `?` placeholders. |
| Silent Exception Handling (B110) | Security — Low | 58–59 | A bare exception handler used `pass`, silently ignoring errors during stock loading. | Replaced it with specific exception handling and meaningful error messages. |
| Mutable Default Argument (W0102) | Bug | 24 | A function used a mutable list as a default argument, potentially sharing data across calls. | Replaced the default list with `None` and initialized a new list inside the function. |
| Improper File Handling (R1732, W1514) | Code Quality | 50, 57 | Files were opened without context managers or explicit encoding. | Used `with open()` and specified UTF-8 encoding. |
| Unused Import (F401, W0611) | Code Quality | 3 | The `os` module was imported but never used. | Removed the unused import. |
| Incorrect Function Naming (C0103) | Style | 61 | The function `printStock` did not follow Python's snake_case convention. | Renamed it to `print_stock` and updated its references. |
| Missing Docstrings (C0114, C0116) | Code Quality | 1, 11, 19, 24, 29, 41, 49, 54, 61, 66 | The module and multiple functions lacked documentation. | Added module-level and function-level docstrings. |
| Bare Exception Handling (W0702, E722) | Code Quality | 38, 58 | Bare exception handlers could hide unexpected errors. | Used specific exception types such as `ValueError`, `OSError`, and `json.JSONDecodeError` where appropriate. |
| Formatting Violations (E302, E305, E501) | Style | 11, 19, 24, 25, 29, 36, 41, 49, 54, 61, 66, 83 | Missing blank lines and overly long lines violated PEP 8 style guidelines. | Added appropriate blank lines and reformatted long statements. |
| Global Variable Usage (W0603) | Code Quality | 55 | Unnecessary global reassignment reduced maintainability. | Updated stock data without using unnecessary global reassignment. |

*Line numbers refer to the original Python file and before-analysis reports.*

## Verification

| Tool | Before Fixes | After Fixes |
|---|---|---|
| Pylint | 6.90/10 | 9.92/10 |
| Bandit | 2 findings | 0 findings |
| Flake8 | 15 violations | 0 violations |

### Final Results

- **Issues addressed:** 10 documented issue categories
- **Initial Pylint score:** 6.90/10
- **Final Pylint score:** 9.92/10
- **Bandit findings remaining:** 0
- **Flake8 findings remaining:** 0

One Pylint warning remains: `R0911` (too many return statements), reported at line 56 in the updated file. The final score nevertheless exceeds the required target.

## Conclusion

Static code analysis helped identify and correct security, code-quality, and formatting problems in the Pharmacy Prescription & Stock Tracker.

The most important improvements were replacing unsafe SQL string construction with parameterized queries, correcting mutable default arguments, improving exception handling, and adopting safer file operations.

After the changes, the Pylint score improved from 6.90/10 to 9.92/10. Bandit identified no remaining security findings, and Flake8 reported no violations.

The analysis demonstrates how static analysis tools can improve code security, readability, and maintainability while supporting more reliable software development.