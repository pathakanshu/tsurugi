import datetime
import json
import os
import sqlite3

from textblob import TextBlob

# Load user mappings
USER_MAPPINGS = {}
USER_MAPPINGS_PATH = os.path.join(
    os.path.dirname(__file__), "data", "user_mappings.json"
)

try:
    with open(USER_MAPPINGS_PATH, "r") as f:
        data = json.load(f)
        # Create a reverse mapping: user_id -> real_name
        for real_name, user_data in data["users"].items():
            for account in user_data["accounts"]:
                USER_MAPPINGS[account["user_id"]] = user_data["name"]
except FileNotFoundError:
    print(f"Warning: User mappings file not found at {USER_MAPPINGS_PATH}")
except Exception as e:
    print(f"Warning: Could not load user mappings: {e}")


async def initialize_database(db_path: str):
    conn = sqlite3.connect(db_path)

    c = conn.cursor()
    # store message id, author id, author name, content, created at, attachments (as a comma separated list of urls)
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages
                 (message_id TEXT PRIMARY KEY,
                 author_id TEXT, author_name TEXT,
                 content TEXT,
                 created_at TEXT,
                 attachments TEXT)"""
    )
    return conn, c


async def store_messages(ctx):
    """
    Stores all messages from the current channel into a SQLite database.
    The database file is named with the current datetime, guild id, and channel id.
    Args:
        ctx: The context of the command.
    Returns:
        The number of messages stored."""

    now = datetime.datetime.now()
    datetime_str = now.strftime("%Y%m%d_%H%M%S")
    db_filename = f"{datetime_str}_{ctx.guild.id}_{ctx.channel.id}_messages.db"
    db_path = os.path.join(os.path.dirname(__file__), "data", db_filename)

    conn, c = await initialize_database(db_path)

    count = 0
    milestones = {100, 1000, 10000, 100000}
    last_100k_milestone = 0

    async for message in ctx.channel.history(limit=None, oldest_first=True):
        attachments = ",".join([attachment.url for attachment in message.attachments])
        c.execute(
            "INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(message.id),
                str(message.author.id),
                message.author.name,
                message.content,
                message.created_at.isoformat(),
                attachments,
            ),
        )
        count += 1

        # Send progress updates at specified milestones
        if count in milestones:
            await ctx.send(f"Progress: {count:,} messages stored...")
        elif count > 100000 and count % 100000 == 0 and count != last_100k_milestone:
            await ctx.send(f"Progress: {count:,} messages stored...")
            last_100k_milestone = count

    conn.commit()
    conn.close()
    return count


def sentiment_polarity(text: str) -> float:
    """
    Custom SQL function: Returns sentiment polarity score.
    Range: -1.0 (negative) to +1.0 (positive)
    """
    if not text:
        return 0.0
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity  # type: ignore
    except Exception:
        return 0.0


def sentiment_subjectivity(text: str) -> float:
    """
    Custom SQL function: Returns sentiment subjectivity score.
    Range: 0.0 (objective) to 1.0 (subjective)
    """
    if not text:
        return 0.0
    try:
        blob = TextBlob(text)
        return blob.sentiment.subjectivity  # type: ignore
    except Exception:
        return 0.0


def sentiment_label(text: str) -> str:
    """
    Custom SQL function: Returns sentiment label (positive/neutral/negative).
    """
    polarity = sentiment_polarity(text)
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


def word_count(text: str) -> int:
    """Custom SQL function: Returns word count."""
    if not text:
        return 0
    return len(text.split())


def real_name(author_id: str) -> str:
    """
    Custom SQL function: Maps Discord author ID to real person name.
    If not found in mappings, returns the original author_id.
    """
    if not author_id:
        return "Unknown"
    return USER_MAPPINGS.get(str(author_id), author_id)


def is_tracked(author_id: str) -> int:
    """
    Custom SQL function: Returns 1 if author is in the mappings, 0 otherwise.
    Use in WHERE clause to filter only tracked users.
    Example: WHERE is_tracked(author_id) = 1
    """
    if not author_id:
        return 0
    return 1 if str(author_id) in USER_MAPPINGS else 0


async def run_sql_query(db_path: str, query: str):
    """
    Runs a SQL query on the specified database and returns the results.
    Args:
        db_path: The path to the SQLite database file.
        query: The SQL query to run.
    Returns:
        The results of the query as a string to send in Discord.
    """
    if not os.path.exists(db_path):
        return "Database file not found."

    conn = sqlite3.connect(db_path)

    # Register custom SQL functions
    conn.create_function("sentiment_polarity", 1, sentiment_polarity)
    conn.create_function("sentiment_subjectivity", 1, sentiment_subjectivity)
    conn.create_function("sentiment_label", 1, sentiment_label)
    conn.create_function("word_count", 1, word_count)
    conn.create_function("real_name", 1, real_name)
    conn.create_function("is_tracked", 1, is_tracked)

    c = conn.cursor()
    try:
        c.execute(query)
        results = c.fetchall()
        conn.close()
        if not results:
            return "Query executed successfully, but no results to display."
        # Format results as a string
        result_str = "\n".join([str(row) for row in results])
        return f"Query Results:\n{result_str}"
    except sqlite3.Error as e:
        conn.close()
        return f"An error occurred: {e}"
