# Safety & Resource Protection

The Tsurugi bot implements multiple layers of protection to prevent resource exhaustion and malicious code execution on the server.

## Overview

Running a Discord bot with code execution capabilities (like `!matplotlib` and `!runsql`) poses security risks. We've implemented the following safety measures:

## Protection Mechanisms

### 1. **Execution Timeouts**

Prevents infinite loops and long-running operations from consuming resources.

- **Matplotlib code**: 5 second timeout
- **SQL queries**: 10 second timeout
- Uses Unix signals (`SIGALRM`) to interrupt execution

**Example protected operation:**
```python
@timeout(5)  # Kills execution after 5 seconds
def execute_code():
    exec(code, safe_globals, local_scope)
```

### 2. **Rate Limiting**

Prevents spam and resource exhaustion from repeated command usage.

- **Matplotlib**: 5 plots per minute per user
- **SQL queries**: 10 queries per minute per user
- Tracked per user, per command
- Returns friendly error message when exceeded

**Implementation:**
```python
@rate_limit(calls=5, period=60)  # 5 calls per 60 seconds
async def matplotlib(ctx, *, code: str = ""):
    # Command logic
```

### 3. **Restricted Execution Environment**

Limits what code can access and execute in `!matplotlib` commands.

**Allowed:**
- `matplotlib.pyplot` (plt)
- `numpy` (np)
- Basic built-ins: `abs`, `min`, `max`, `sum`, `len`, `range`, `zip`, `enumerate`
- Basic data types: `list`, `dict`, `tuple`, `set`

**Blocked:**
- `__import__`, `eval`, `exec`, `compile`
- `open` (file operations)
- `input` (user input)
- OS operations
- Network operations
- Subprocess execution

### 4. **SQL Query Validation**

Prevents dangerous database operations and SQL injection.

**Restrictions:**
- Only `SELECT` statements allowed
- No `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `CREATE`, `TRUNCATE`
- No `EXEC`, `EXECUTE`, `PRAGMA`
- No multiple statements (prevents SQL injection)
- Maximum 5000 characters per query
- Results limited to 1000 rows

**Example:**
```sql
-- ✅ Allowed
SELECT * FROM messages WHERE author_id = '123'

-- ❌ Blocked
DROP TABLE messages;
DELETE FROM messages;
INSERT INTO messages VALUES (...);
```

### 5. **Code Safety Checks**

Scans code for obviously dangerous patterns before execution.

**Detected patterns:**
- `import os`, `import sys`, `import subprocess`
- `import socket` (network operations)
- `__import__`, `eval()`, `exec()`, `compile()`
- `open()` (file operations)
- `while True` (warns about infinite loops)

### 6. **Size Limits**

Prevents memory exhaustion from large inputs/outputs.

- **Matplotlib code**: Max 2000 characters
- **SQL queries**: Max 5000 characters
- **Query results**: Max 1000 rows (truncated with warning)
- File attachments: Handled by Discord's limits

## Error Handling

All safety violations return clear error messages:

```
❌ Code execution timed out (5 second limit)
❌ Unsafe code detected: OS operations are restricted
❌ Query validation failed: Only SELECT queries are allowed
⏱️ Rate limit exceeded. Try again in 45 seconds.
❌ Code is too long (max 2000 characters)
⚠️ Results truncated to 1000 rows
```

## Implementation Details

### Timeout Mechanism

Uses Unix signals to interrupt long-running code:

```python
def timeout_handler(signum, frame):
    raise TimeoutError(f"Execution exceeded {seconds} second(s)")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(seconds)  # Set alarm
# ... execute code ...
signal.alarm(0)  # Cancel alarm
```

**Note:** This only works on Unix-like systems (Linux, macOS). Windows servers would need a different approach (e.g., `multiprocessing` with `Process.terminate()`).

### Rate Limiting Storage

Stores timestamps per user per command:

```python
{
  "user_id_123": {
    "matplotlib": [timestamp1, timestamp2, timestamp3],
    "runsql": [timestamp1, timestamp2]
  }
}
```

Old timestamps are cleaned up automatically when checking limits.

### Safe Globals

Restricted global namespace for `exec()`:

```python
safe_globals = {
    "plt": plt,
    "np": np,
    "__builtins__": {  # Minimal builtins
        "abs": abs,
        "min": min,
        # ... only safe functions
    },
    "__import__": None,  # Explicitly blocked
    "exec": None,
    "eval": None,
    "open": None,
}
```

## What's Still Vulnerable?

Despite these protections, some risks remain:

### 1. **CPU-Intensive Operations**
```python
# Can still max out CPU for 5 seconds
plt.plot(range(10000000), range(10000000))
```
**Mitigation:** Short timeout (5s), rate limiting, monitoring

### 2. **Memory Allocation**
```python
# Can allocate large amounts of memory
huge_array = np.zeros((10000, 10000, 10000))
```
**Mitigation:** Timeout will eventually kill it, OS memory limits

### 3. **Complex SQL Queries**
```sql
-- Can be slow but valid
SELECT * FROM messages m1 
CROSS JOIN messages m2 
CROSS JOIN messages m3;
```
**Mitigation:** 10s timeout, result row limit

## Recommendations for Production

For running on a production server, consider these additional measures:

### 1. **Operating System Limits**
Set ulimits for the bot process:
```bash
# In systemd service file
LimitCPU=300          # Max 5 minutes CPU
LimitAS=1G            # Max 1GB memory
LimitNOFILE=1024      # Max 1024 open files
```

### 2. **Docker Container**
Run the bot in a container with resource limits:
```yaml
# docker-compose.yml
services:
  tsurugi:
    image: tsurugi-bot
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

### 3. **Process Monitoring**
Use process managers like `systemd` or `supervisor` with:
- Auto-restart on crashes
- Resource monitoring
- Log rotation

### 4. **Separate User**
Run the bot as a non-privileged user with minimal permissions:
```bash
sudo useradd -r -s /bin/false tsurugi
sudo -u tsurugi python -m tsurugi
```

### 5. **Firewall Rules**
Ensure the bot can't make outbound connections except to Discord:
```bash
# Allow only Discord API
iptables -A OUTPUT -d discord.com -j ACCEPT
iptables -A OUTPUT -j DROP
```

### 6. **Regular Monitoring**
Monitor resource usage:
```bash
# CPU and memory usage
top -p $(pgrep -f tsurugi)

# Check for hanging processes
ps aux | grep tsurugi
```

## Testing Safety Features

You can test the safety features safely:

```python
# Test timeout (will be killed after 5s)
!matplotlib
import time
time.sleep(10)
plt.plot([1,2,3])

# Test rate limit (6th call will fail)
!matplotlib plt.plot([1,2,3])
# ... repeat 6 times quickly ...

# Test SQL validation
!runsql DROP TABLE messages;  # Will be blocked
```

## Files

- `src/tsurugi/helpers/safety.py` - Safety implementation
- `src/tsurugi/bot.py` - Command implementations with safety decorators

## Future Improvements

Potential enhancements for even better security:

1. **Sandbox environment** (e.g., using `firejail` or containers)
2. **AST parsing** to analyze code structure before execution
3. **Resource usage tracking** per user
4. **Whitelist mode** for matplotlib imports
5. **Query cost estimation** before execution
6. **Async timeouts** using `asyncio.wait_for()`
