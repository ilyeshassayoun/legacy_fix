# log_util.py
# A homemade logger. The logging module felt like "too much magic" in 2013.

import time

LOG_LINES: list[str] = []   # module-level buffer; flushed to disk by flush_log()
DEBUG = False


def log(message: str) -> None:
    """Timestamp message, print it, and buffer it for the next flush."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a debug-level message (only active when DEBUG is True)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Append buffered log lines to path and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
