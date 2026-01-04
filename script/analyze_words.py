#!/usr/bin/env python3
"""
Analyze word frequency from archived Discord messages.
Finds the top N most used words, with options to filter stop words.
"""

import glob
import re
import sqlite3
import sys
from collections import Counter
from typing import Optional

# Common English stop words to filter out
STOP_WORDS = {
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "i",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "they",
    "we",
    "say",
    "her",
    "she",
    "or",
    "an",
    "will",
    "my",
    "one",
    "all",
    "would",
    "there",
    "their",
    "what",
    "so",
    "up",
    "out",
    "if",
    "about",
    "who",
    "get",
    "which",
    "go",
    "me",
    "when",
    "make",
    "can",
    "like",
    "time",
    "no",
    "just",
    "him",
    "know",
    "take",
    "people",
    "into",
    "year",
    "your",
    "good",
    "some",
    "could",
    "them",
    "see",
    "other",
    "than",
    "then",
    "now",
    "look",
    "only",
    "come",
    "its",
    "over",
    "think",
    "also",
    "back",
    "after",
    "use",
    "two",
    "how",
    "our",
    "work",
    "first",
    "well",
    "way",
    "even",
    "new",
    "want",
    "because",
    "any",
    "these",
    "give",
    "day",
    "most",
    "us",
    "is",
    "was",
    "are",
    "been",
    "has",
    "had",
    "were",
    "said",
    "did",
    "am",
    "im",
    "ive",
    "dont",
    "doesnt",
    "didnt",
    "cant",
    "wont",
    "wouldnt",
    "couldnt",
    "shouldnt",
    "isnt",
    "arent",
    "wasnt",
    "werent",
    "hasnt",
    "havent",
    "hadnt",
}


def find_latest_db() -> Optional[str]:
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


def tokenize(text: str) -> list[str]:
    """
    Tokenize text into words.
    - Converts to lowercase
    - Removes URLs, mentions, emojis
    - Splits on word boundaries
    - Filters short words
    """
    if not text:
        return []

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"www\.\S+", "", text)

    # Remove Discord mentions and channels
    text = re.sub(r"<@!?\d+>", "", text)
    text = re.sub(r"<#\d+>", "", text)
    text = re.sub(r"<@&\d+>", "", text)

    # Remove Discord emojis
    text = re.sub(r"<a?:\w+:\d+>", "", text)

    # Convert to lowercase
    text = text.lower()

    # Extract words (alphanumeric + apostrophes for contractions)
    words = re.findall(r"\b[a-z]{2,}(?:'[a-z]+)?\b", text)

    return words


def analyze_words(
    db_path: str, top_n: int = 100, filter_stop_words: bool = True, min_length: int = 2
):
    """
    Analyze word frequency from the database.

    Args:
        db_path: Path to the SQLite database
        top_n: Number of top words to return
        filter_stop_words: Whether to filter common stop words
        min_length: Minimum word length to include
    """
    print(f"📁 Analyzing: {db_path}")
    print(f"⚙️  Settings: top {top_n}, min length: {min_length}", end="")
    if filter_stop_words:
        print(f", filtering {len(STOP_WORDS)} stop words")
    else:
        print(", including all words")
    print("=" * 70)

    try:
        # Connect to database with read-only mode
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=30.0)
        cursor = conn.cursor()

        # Get total message count
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = cursor.fetchone()[0]
        print(f"📊 Total messages: {total_messages:,}")

        # Fetch all message content
        print("🔄 Loading messages...")
        cursor.execute("SELECT content FROM messages WHERE content IS NOT NULL")

        word_counter = Counter()
        messages_processed = 0
        batch_size = 10000

        print("🔍 Processing messages...")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break

            for (content,) in rows:
                words = tokenize(content)

                # Filter by length
                words = [w for w in words if len(w) >= min_length]

                # Filter stop words if requested
                if filter_stop_words:
                    words = [w for w in words if w not in STOP_WORDS]

                word_counter.update(words)

            messages_processed += len(rows)
            if messages_processed % 50000 == 0:
                print(f"   Processed {messages_processed:,} messages...")

        conn.close()

        print(f"✅ Processed {messages_processed:,} messages")
        print(f"📚 Unique words found: {len(word_counter):,}")
        print()

        # Get top N words
        top_words = word_counter.most_common(top_n)

        print(f"🏆 Top {top_n} Most Used Words:")
        print("=" * 70)

        # Calculate total word count for percentages
        total_words = sum(word_counter.values())

        for i, (word, count) in enumerate(top_words, 1):
            percentage = (count / total_words) * 100
            bar_length = int(percentage * 2)  # Scale for display
            bar = "█" * bar_length

            print(f"{i:3d}. {word:20s} {count:8,} ({percentage:5.2f}%) {bar}")

        print("=" * 70)
        print(f"📈 Total words analyzed: {total_words:,}")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    # Parse command line arguments
    top_n = 100
    filter_stop_words = True
    min_length = 2

    if len(sys.argv) > 1:
        try:
            top_n = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid number: {sys.argv[1]}")
            sys.exit(1)

    if len(sys.argv) > 2 and sys.argv[2] in ["all", "no-filter", "nofilter"]:
        filter_stop_words = False

    if len(sys.argv) > 3:
        try:
            min_length = int(sys.argv[3])
        except ValueError:
            print(f"❌ Invalid minimum length: {sys.argv[3]}")
            sys.exit(1)

    # Find database
    db_path = find_latest_db()
    if not db_path:
        print("❌ No database files found.")
        print("\nSearched in current directory, src/, ../src/")
        print("\nRun !archive in Discord first to create a database.")
        sys.exit(1)

    # Run analysis
    analyze_words(db_path, top_n, filter_stop_words, min_length)

    print()
    print("💡 Usage tips:")
    print("   python script/analyze_words.py 50           # Top 50 words")
    print("   python script/analyze_words.py 100 all      # Include stop words")
    print("   python script/analyze_words.py 100 all 3    # Min 3 letters")


if __name__ == "__main__":
    main()
