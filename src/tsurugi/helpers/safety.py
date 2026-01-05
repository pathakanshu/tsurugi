"""
Safety helpers for preventing resource exhaustion from user code execution.
Includes timeouts, memory limits, and execution restrictions.
"""

import functools
import signal
import time
from collections import defaultdict
from typing import Any, Callable


class TimeoutError(Exception):
    """Raised when code execution exceeds time limit."""

    pass


class RateLimitError(Exception):
    """Raised when user exceeds rate limit."""

    pass


# Rate limiting storage: {user_id: {command: [timestamps]}}
_rate_limits = defaultdict(lambda: defaultdict(list))


def timeout(seconds: int):
    """
    Decorator to add execution timeout to a function.
    Only works on Unix-like systems (Linux, macOS).

    Args:
        seconds: Maximum execution time in seconds

    Raises:
        TimeoutError: If execution exceeds time limit
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Execution exceeded {seconds} second(s)")

            # Set the signal handler and alarm
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                # Restore the old signal handler and cancel alarm
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

            return result

        return wrapper

    return decorator


def rate_limit(calls: int, period: int):
    """
    Decorator to rate limit command usage per user.

    Args:
        calls: Number of allowed calls
        period: Time period in seconds

    Example:
        @rate_limit(calls=3, period=60)  # 3 calls per minute
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            user_id = str(ctx.author.id)
            command_name = ctx.command.name if ctx.command else "unknown"
            now = time.time()

            # Clean up old timestamps
            _rate_limits[user_id][command_name] = [
                ts for ts in _rate_limits[user_id][command_name] if now - ts < period
            ]

            # Check rate limit
            if len(_rate_limits[user_id][command_name]) >= calls:
                time_left = period - (now - _rate_limits[user_id][command_name][0])
                raise RateLimitError(
                    f"Rate limit exceeded. Try again in {time_left:.0f} seconds."
                )

            # Record this call
            _rate_limits[user_id][command_name].append(now)

            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator


def get_safe_exec_globals() -> dict[str, Any]:
    """
    Return a restricted set of globals for exec() to prevent dangerous operations.
    Only includes safe matplotlib functionality.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Only allow safe functions
    safe_globals = {
        "plt": plt,
        "np": np,
        # Math functions
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
        "zip": zip,
        "enumerate": enumerate,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
        # Explicitly blocked
        "__import__": None,
        "exec": None,
        "eval": None,
        "compile": None,
        "open": None,
        "input": None,
        "__builtins__": {
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "len": len,
            "range": range,
        },
    }

    return safe_globals


def validate_sql_query(query: str) -> tuple[bool, str]:
    """
    Validate SQL query to prevent dangerous operations.

    Args:
        query: The SQL query to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    query_upper = query.upper().strip()

    # Only allow SELECT statements
    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed"

    # Block dangerous keywords
    dangerous_keywords = [
        "DROP",
        "DELETE",
        "INSERT",
        "UPDATE",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "EXEC",
        "EXECUTE",
        "PRAGMA",
    ]

    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False, f"Dangerous keyword '{keyword}' is not allowed"

    # Check for multiple statements (SQL injection attempt)
    if ";" in query.rstrip(";"):
        return False, "Multiple statements are not allowed"

    return True, ""


def limit_query_results(results: list, max_rows: int = 1000) -> tuple[list, bool]:
    """
    Limit the number of rows returned from a query.

    Args:
        results: Query results
        max_rows: Maximum number of rows to return

    Returns:
        Tuple of (limited_results, was_truncated)
    """
    if len(results) > max_rows:
        return results[:max_rows], True
    return results, False


def format_size(bytes: int) -> str:
    """Format byte size to human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"


def check_code_safety(code: str) -> tuple[bool, str]:
    """
    Check if code contains obviously dangerous patterns.

    Args:
        code: Python code to check

    Returns:
        Tuple of (is_safe, warning_message)
    """
    dangerous_patterns = [
        ("import os", "OS operations are restricted"),
        ("import sys", "System operations are restricted"),
        ("import subprocess", "Subprocess operations are not allowed"),
        ("import socket", "Network operations are not allowed"),
        ("__import__", "Dynamic imports are not allowed"),
        ("eval(", "eval() is not allowed"),
        ("exec(", "exec() is not allowed"),
        ("compile(", "compile() is not allowed"),
        ("open(", "File operations are restricted"),
        ("while True", "Infinite loops may cause timeout"),
    ]

    for pattern, message in dangerous_patterns:
        if pattern in code:
            return False, message

    return True, ""
