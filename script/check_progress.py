#!/usr/bin/env python3
"""
Script to check the progress of an ongoing archive operation.
Reads the SQLite database file and shows the current message count.
"""

import glob
import sqlite3
import sys


def check_progress():
    # Search for database files in common locations
    search_paths = [
        "*_messages.db",  # Current directory
        "src/*_messages.db",  # src directory
        "../*_messages.db",  # Parent directory
        "../src/*_messages.db",  # Parent's src directory
    ]

    db_files: list[str] = []
    for pattern in search_paths:
        db_files.extend(glob.glob(pattern))

    if not db_files:
        print("No database files found.")
        print("Searched in:")
        for pattern in search_paths:
            print(f"  - {pattern}")
        return

    # Get the most recent database file
    db_files = sorted(db_files)
    latest_db = db_files[-1]

    print(f"Found {len(db_files)} database file(s)")
    print(f"Checking progress in: {latest_db}")
    print("-" * 60)

    try:
        # Open in read-only mode with URI and set timeout
        conn = sqlite3.connect(f"file:{latest_db}?mode=ro", uri=True, timeout=30.0)
        cursor = conn.cursor()

        # Get total message count
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_count = cursor.fetchone()[0]

        # Get unique author count
        cursor.execute("SELECT COUNT(DISTINCT author_id) FROM messages")
        author_count = cursor.fetchone()[0]

        # Get date range
        cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM messages")
        min_date, max_date = cursor.fetchone()

        # Get top 5 authors
        cursor.execute("""
            SELECT author_name, COUNT(*) as count
            FROM messages
            GROUP BY author_id
            ORDER BY count DESC
            LIMIT 5
        """)
        top_authors = cursor.fetchall()

        conn.close()

        # Display results
        print(f"📊 Messages archived: {total_count:,}")
        print(f"👥 Unique authors: {author_count:,}")
        print(
            f"📅 Date range: {min_date[:10] if min_date else 'N/A'} to {max_date[:10] if max_date else 'N/A'}"
        )
        print()
        print("🏆 Top 5 Authors:")
        for i, (name, count) in enumerate(top_authors, 1):
            print(f"  {i}. {name}: {count:,} messages")

    except sqlite3.Error as e:
        print(f"Error reading database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    check_progress()
