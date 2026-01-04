#!/usr/bin/env python3
"""
Script to monitor database file size and estimate progress.
Works even when the database is locked.
Run with: python script/watch_progress.py
"""

import glob
import os
import sys
import time
from datetime import datetime


def format_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def find_latest_db():
    """Find the most recent database file."""
    search_paths = [
        "*_messages.db",
        "src/*_messages.db",
        "../*_messages.db",
        "../src/*_messages.db",
    ]

    db_files = []
    for pattern in search_paths:
        db_files.extend(glob.glob(pattern))

    if not db_files:
        return None

    return sorted(db_files)[-1]


def estimate_messages(size_bytes):
    """Estimate message count from file size."""
    # Average message size including all fields and overhead
    # Conservative estimate: 600-800 bytes per message
    min_est = size_bytes // 200
    max_est = size_bytes // 150
    avg_est = (min_est + max_est) // 2
    return min_est, max_est, avg_est


def monitor_progress(continuous=False, interval=5):
    """Monitor database file growth."""
    db_path = find_latest_db()

    if not db_path:
        print("❌ No database files found.")
        print("\nSearched in current directory, src/, ../src/")
        return

    print(f"📁 Monitoring: {os.path.basename(db_path)}")
    print(f"📍 Location: {os.path.dirname(os.path.abspath(db_path)) or '.'}")
    print("=" * 70)

    last_size = 0
    start_time = time.time()

    try:
        while True:
            # Get current file info
            size = os.path.getsize(db_path)
            mtime = os.path.getmtime(db_path)
            time_since_modified = time.time() - mtime

            # Calculate estimates
            min_est, max_est, avg_est = estimate_messages(size)

            # Calculate growth rate
            size_diff = size - last_size
            growth_rate = ""
            if last_size > 0 and continuous:
                messages_added = size_diff // 175  # rough average
                growth_rate = f" (+{messages_added:,} msgs in {interval}s)"

            # Clear screen for continuous mode
            if continuous:
                print("\033[2J\033[H", end="")  # Clear screen and move cursor to top
                print(f"📁 Monitoring: {os.path.basename(db_path)}")
                print(
                    f"📍 Location: {os.path.dirname(os.path.abspath(db_path)) or '.'}"
                )
                print("=" * 70)

            # Display current stats
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
            print(f"📦 File Size: {format_size(size)}{growth_rate}")
            print(f"📊 Estimated Messages: ~{avg_est:,} ({min_est:,} - {max_est:,})")

            # Status indicator
            if time_since_modified < 5:
                print(f"✅ Status: ACTIVE (modified {time_since_modified:.1f}s ago)")
            elif time_since_modified < 30:
                print(f"⚠️  Status: Slow (modified {time_since_modified:.1f}s ago)")
            else:
                print(f"❌ Status: STALLED? (modified {int(time_since_modified)}s ago)")

            # Progress milestones
            print(f"\n🎯 Milestones:")
            milestones = [
                (100, "✓" if avg_est >= 100 else "○"),
                (1000, "✓" if avg_est >= 1000 else "○"),
                (10000, "✓" if avg_est >= 10000 else "○"),
                (100000, "✓" if avg_est >= 100000 else "○"),
                (200000, "✓" if avg_est >= 200000 else "○"),
                (500000, "✓" if avg_est >= 500000 else "○"),
                (800000, "✓" if avg_est >= 800000 else "○"),
            ]

            for milestone, status in milestones:
                if avg_est >= milestone * 0.9:  # Show milestone when close
                    print(f"   {status} {milestone:,} messages", end="")
                    if avg_est < milestone:
                        remaining = milestone - avg_est
                        print(f" (est. {remaining:,} to go)")
                    else:
                        print(" ✓")

            # ETA calculation (rough)
            if continuous and last_size > 0 and size_diff > 0:
                elapsed = interval
                messages_per_sec = (size_diff / 175) / elapsed
                if messages_per_sec > 0:
                    # Estimate to 800k
                    remaining_messages = 800000 - avg_est
                    if remaining_messages > 0:
                        eta_seconds = remaining_messages / messages_per_sec
                        eta_minutes = int(eta_seconds / 60)
                        print(
                            f"\n⏱️  ETA to 800k: ~{eta_minutes} minutes ({messages_per_sec:.1f} msg/s)"
                        )

            if not continuous:
                break

            print(f"\n{'─' * 70}")
            print(f"Refreshing in {interval} seconds... (Ctrl+C to stop)")

            last_size = size
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Check if user wants continuous monitoring
    if len(sys.argv) > 1 and sys.argv[1] in ["-w", "--watch", "watch"]:
        print("🔄 Starting continuous monitoring (Ctrl+C to stop)...\n")
        monitor_progress(continuous=True, interval=5)
    else:
        monitor_progress(continuous=False)
        print("\n💡 Tip: Run with 'watch' argument for live updates:")
        print("   python script/watch_progress.py watch")
