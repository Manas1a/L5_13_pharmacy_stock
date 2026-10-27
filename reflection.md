# Lab 5 — Static Code Analysis Reflection

**Project:** Pharmacy Prescription & Stock Tracker

**Python File:** `pharmacy_system.py`

## Proposed Reflection Question 1: What is static code analysis, and what did you learn from this lab?

Static code analysis is the process of examining source code without executing it to identify potential bugs, security vulnerabilities, and coding-standard violations.

In this lab, I learned how to use Pylint, Bandit, and Flake8 to analyze a Python pharmacy management program. The tools helped me identify problems such as unsafe SQL queries, mutable default arguments, improper exception handling, and formatting violations.

I also learned how to interpret analysis reports, identify line numbers, fix the reported issues, and rerun the tools to verify improvements.

## Proposed Reflection Question 2: How do Pylint, Bandit, and Flake8 differ?

Each tool focuses on a different aspect of code quality.

**Pylint** checks programming practices, potential bugs, naming conventions, documentation, and maintainability. It initially rated my program 6.90/10.

**Bandit** identifies potential security vulnerabilities in Python code. It detected a possible SQL injection vulnerability and silent exception handling in my original program.

**Flake8** checks coding-style violations such as unused imports, missing blank lines, and overly long lines. It initially reported 15 violations.

Using all three tools helped me identify a wider range of issues than using a single tool.

## Proposed Reflection Question 3: What were the most important issues you fixed, and how did the fixes improve the program?

One important issue was the SQL injection vulnerability. The original program constructed SQL queries using string formatting. I replaced this with parameterized queries to prevent user input from being interpreted as SQL commands.

Another issue was the mutable default argument in the stock management function. I replaced the default empty list with `None` and initialized a new list inside the function.

I also improved exception handling, used context managers for file operations, removed unused imports, added docstrings, and corrected naming and formatting issues.

Additionally, I improved stock validation to prevent invalid quantities and dispensing when insufficient stock is available.

These changes improved the security, readability, and reliability of the pharmacy management program.

## Proposed Reflection Question 4: How did you verify the improvements, and why is static code analysis important in software engineering?

After modifying the program, I reran Pylint, Bandit, and Flake8 and compared their results with the original reports.

The results were:

| Tool | Before | After |
|---|---|---|
| Pylint | 6.90/10 | 9.92/10 |
| Bandit | 2 findings | 0 findings |
| Flake8 | 15 violations | 0 violations |

The final Pylint score exceeded the target of 9.5/10. Bandit reported no remaining findings, and Flake8 reported no violations.

This lab demonstrated that static analysis is useful because it detects problems early, encourages secure coding practices, and improves software maintainability.

However, static analysis cannot detect every logical error. Programs must also be executed and tested to ensure that they behave correctly.

## Final Reflection

This lab helped me understand the importance of combining multiple static analysis tools to improve software quality.

By identifying issues, implementing fixes, and verifying the results, I gained practical experience with code review, secure programming, debugging, and maintaining Python applications.