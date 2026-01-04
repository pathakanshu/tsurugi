# SQL Practice Questions - Discord Message Archive

A comprehensive guide to mastering SQL through 100+ practice questions using your Discord message archive database.

## Database Schema

Your `messages` table has the following structure:
```sql
messages (
    message_id TEXT PRIMARY KEY,
    author_id TEXT,
    author_name TEXT,
    content TEXT,
    created_at TEXT,  -- ISO 8601 format: "2026-01-01T12:34:56.789000+00:00"
    attachments TEXT  -- Comma-separated URLs
)
```

## Custom SQL Functions Available

- `sentiment_polarity(text)` - Returns -1.0 (negative) to +1.0 (positive)
- `sentiment_subjectivity(text)` - Returns 0.0 (objective) to 1.0 (subjective)
- `sentiment_label(text)` - Returns "positive", "neutral", or "negative"
- `word_count(text)` - Returns number of words in text
- `real_name(author_id)` - Maps Discord ID to real person name
- `is_tracked(author_id)` - Returns 1 if user is in mappings, 0 otherwise

---

## Level 1: Basic SELECT Queries (Questions 1-10)

### 1. Select Everything
Get all columns from all messages (limit to 10 for testing).

### 2. Select Specific Columns
Get only the author name and message content from all messages.

### 3. Count Total Messages
How many messages are in the database?

### 4. Count Unique Authors
How many unique authors have posted messages?

### 5. Find Your Messages
Select all messages where the author_id is your ID.

### 6. Limit Results
Get the first 20 messages in the database.

### 7. Non-Empty Messages
Select all messages where content is not empty or NULL.

### 8. Messages with Attachments
Find all messages that have attachments (attachments field is not empty).

### 9. Specific Author by Name
Find all messages from a specific author by their author_name.

### 10. Select Distinct Author Names
Get a list of all unique author names (no duplicates).

---

## Level 2: WHERE Clauses & Filtering (Questions 11-25)

### 11. Messages Containing a Word
Find all messages that contain the word "discord" (case-insensitive).

### 12. Messages NOT Containing a Word
Find all messages that do NOT contain "http" (filter out messages with links).

### 13. Long Messages
Find messages where content length is greater than 200 characters.

### 14. Short Messages
Find messages with 10 or fewer characters.

### 15. Multiple Conditions (AND)
Find messages from a specific author that also contain a specific word.

### 16. Multiple Conditions (OR)
Find messages that contain either "hello" OR "hi".

### 17. Date Range Filter
Find all messages created in December 2025.

### 18. Recent Messages
Find all messages created after January 1, 2026.

### 19. Message ID Range
Find messages where message_id is between two specific IDs.

### 20. Exclude Multiple Authors
Find messages from authors who are NOT in a list of specific IDs.

### 21. Pattern Matching with LIKE
Find all messages that start with "I think".

### 22. Pattern Matching - Ends With
Find all messages that end with a question mark "?".

### 23. Pattern Matching - Contains
Find messages that contain "lol" or "lmao" anywhere in the text.

### 24. NULL Values
Find all messages where attachments is NULL or empty.

### 25. Complex Filter
Find messages from tracked users that are longer than 100 characters and contain "http".

---

## Level 3: Sorting & Ordering (Questions 26-35)

### 26. Sort by Date (Ascending)
Get all messages ordered from oldest to newest.

### 27. Sort by Date (Descending)
Get all messages ordered from newest to oldest.

### 28. Sort by Author Name
Get all messages sorted alphabetically by author name.

### 29. Sort by Message Length
Get messages sorted by content length (longest first).

### 30. Multiple Sort Criteria
Sort messages first by author_name, then by created_at within each author.

### 31. Top 10 Longest Messages
Find the 10 longest messages in the database.

### 32. Most Recent Messages per Author
For each author, show their most recent message.

### 33. Sort by Word Count
Get messages sorted by word count (use custom function).

### 34. Random Sample
Get 10 random messages from the database.

### 35. Sort NULL Values
Get all messages sorted by attachments, with NULL/empty values at the end.

---

## Level 4: Aggregate Functions (Questions 36-50)

### 36. COUNT All Messages
Count the total number of messages.

### 37. COUNT Distinct Authors
Count how many unique authors posted.

### 38. AVG Message Length
Calculate the average length of all messages.

### 39. MAX Message Length
Find the length of the longest message.

### 40. MIN and MAX Dates
Find the date of the first and last message in the database.

### 41. SUM of Word Counts
Calculate the total number of words across all messages.

### 42. COUNT with WHERE
Count how many messages contain the word "thanks".

### 43. AVG Sentiment Score
Calculate the average sentiment polarity of all messages.

### 44. COUNT Messages per Author
For each author, count how many messages they posted.

### 45. MAX Sentiment per Author
For each author, find their most positive message score.

### 46. Average Word Count per Author
Calculate the average word count for each author's messages.

### 47. Messages by Date
Count how many messages were posted each day.

### 48. COUNT with Multiple Conditions
Count messages that are both long (>100 chars) and positive (sentiment > 0.2).

### 49. Standard Statistics
Get COUNT, AVG, MIN, MAX for message lengths in one query.

### 50. Percentage Calculation
Calculate what percentage of messages have attachments.

---

## Level 5: GROUP BY & HAVING (Questions 51-65)

### 51. Messages per Author
Group messages by author and count them.

### 52. Sort Grouped Results
Group by author, count messages, sort by count descending.

### 53. HAVING Clause - Filter Groups
Show authors who have posted more than 100 messages.

### 54. Multiple Aggregates in GROUP BY
For each author: count messages, average length, total word count.

### 55. GROUP BY Date
Group messages by day and count messages per day.

### 56. GROUP BY with WHERE
For tracked users only, count messages per person.

### 57. HAVING with Multiple Conditions
Find authors with more than 500 messages AND average sentiment > 0.1.

### 58. Top 10 Most Active Authors
Show the 10 authors with the most messages.

### 59. GROUP BY Sentiment Label
Count how many positive, neutral, and negative messages exist.

### 60. Average Sentiment per Tracked User
For each tracked user, calculate their average sentiment score.

### 61. Messages per Month
Group messages by year-month and count them.

### 62. GROUP BY Hour of Day
Extract hour from created_at and count messages per hour.

### 63. Authors with Attachments
Count how many messages with attachments each author has posted.

### 64. GROUP BY Message Length Buckets
Create length categories (short/medium/long) and count messages in each.

### 65. Most Subjective Authors
Find authors with the highest average subjectivity scores (min 100 messages).

---

## Level 6: JOINs & Subqueries (Questions 66-80)

### 66. Self-Join - Find Message Pairs
Find pairs of messages from the same author posted within 1 minute of each other.

### 67. Subquery in WHERE
Find messages from authors who have posted more than 1000 messages.

### 68. Subquery in SELECT
For each message, show how many total messages that author has.

### 69. Correlated Subquery
For each author, find messages that are longer than their average.

### 70. IN Subquery
Find messages from the top 5 most active authors.

### 71. NOT IN Subquery
Find messages from authors who have never posted a negative message.

### 72. Subquery with MAX
Find the message with the highest sentiment score.

### 73. Subquery in FROM (Derived Table)
Create a subquery of author stats, then query from that.

### 74. EXISTS Subquery
Find authors who have posted at least one message with attachments.

### 75. Multiple Subqueries
Find messages from authors who are both very active (>1000 msgs) and very positive (avg sentiment > 0.15).

### 76. WITH Clause (CTE) - Basic
Use a Common Table Expression to calculate author statistics, then query from it.

### 77. Multiple CTEs
Create two CTEs: one for active authors, one for positive authors, then join them.

### 78. Recursive CTE
(Advanced) Create a recursive query to generate a sequence or hierarchy.

### 79. Subquery for Ranking
Find each author's top 3 most positive messages.

### 80. Complex Nested Subquery
Find messages that are in the top 10% by length for their specific author.

---

## Level 7: Advanced String Functions (Questions 81-90)

### 81. SUBSTR - Extract Username
Extract the first 10 characters of each author's name.

### 82. REPLACE - Clean Content
Replace all "lol" with "haha" in message content.

### 83. TRIM - Clean Whitespace
Find messages with leading or trailing whitespace.

### 84. UPPER and LOWER
Convert all author names to uppercase.

### 85. LENGTH vs Custom word_count
Compare LENGTH(content) with word_count(content) for all messages.

### 86. INSTR - Find Position
Find the position of "http" in messages that contain links.

### 87. LIKE with Multiple Patterns
Find messages containing emoji patterns or special characters.

### 88. String Concatenation
Create a formatted string combining author name, date, and content preview.

### 89. CASE Statement - Categorize
Categorize messages as "short", "medium", or "long" based on length.

### 90. CASE with Sentiment
Create custom sentiment labels: "very negative", "negative", "neutral", "positive", "very positive".

---

## Level 8: Date & Time Functions (Questions 91-100)

### 91. STRFTIME - Extract Year
Extract the year from created_at for all messages.

### 92. STRFTIME - Extract Month
Group messages by month name (January, February, etc.).

### 93. Day of Week Analysis
Find which day of the week has the most messages.

### 94. Hour of Day Analysis
Find the most active hour of the day for messages.

### 95. Date Arithmetic
Find all messages posted in the last 30 days.

### 96. Time Between Messages
Calculate the time difference between consecutive messages from the same author.

### 97. Monthly Growth
Show message count growth month over month.

### 98. Weekend vs Weekday
Compare message counts and sentiment between weekends and weekdays.

### 99. Time of Day Sentiment
Analyze if sentiment differs by time of day (morning/afternoon/evening/night).

### 100. Timezone Conversion
Convert created_at timestamps to a different timezone.

---

## Level 9: Window Functions (Questions 101-110)

### 101. ROW_NUMBER - Rank Messages
Assign a row number to each message ordered by created_at.

### 102. RANK - Rank Authors
Rank authors by message count (handle ties).

### 103. DENSE_RANK
Like RANK but with no gaps in ranking numbers.

### 104. NTILE - Quartiles
Divide authors into 4 groups (quartiles) based on message count.

### 105. LAG - Previous Value
For each message, show the previous message's content from the same author.

### 106. LEAD - Next Value
For each message, show the next message's timestamp.

### 107. Running Total
Calculate a running total of messages over time.

### 108. Moving Average
Calculate a 7-day moving average of messages per day.

### 109. Percent Rank
Calculate what percentile each author falls into by message count.

### 110. Window Frame
Calculate average sentiment for each message using a window of 10 surrounding messages.

---

## Level 10: Expert Challenges (Questions 111-125)

### 111. Most Active Conversation
Find the period of 1 hour with the most messages.

### 112. Sentiment Trends Over Time
Show how average sentiment has changed month by month.

### 113. Author Similarity
Find pairs of authors with similar sentiment patterns.

### 114. Conversation Threads
Identify potential conversation threads (messages within 5 minutes of each other).

### 115. Word Frequency Analysis
Find the most common words across all messages (requires creative SQL).

### 116. Activity Patterns
Identify authors who are more active on weekends vs weekdays.

### 117. Response Time Analysis
Calculate average time between messages in a conversation.

### 118. Sentiment Shift Detection
Find authors whose sentiment has significantly changed over time.

### 119. Top Words by Author
For each author, find their most frequently used words.

### 120. Cohort Analysis
Group authors by when they sent their first message and analyze patterns.

### 121. Emoji Usage
Count and rank emoji usage across all messages.

### 122. Message Burst Detection
Find instances where an author sent 5+ messages within 1 minute.

### 123. Content Similarity
Find messages that are very similar to each other (using string comparison).

### 124. Sentiment Volatility
Calculate the standard deviation of sentiment for each author.

### 125. Comprehensive Analytics Dashboard
Create a single query that shows: total messages, unique authors, date range, avg sentiment, top 5 authors, sentiment distribution, messages per day of week, and avg message length.

---

## Bonus: Performance & Optimization (Questions 126-130)

### 126. Query Plan Analysis
Use EXPLAIN QUERY PLAN to understand how SQLite executes your queries.

### 127. Index Creation
Design and create indexes to speed up common queries.

### 128. Query Optimization
Take a slow query and rewrite it to be faster.

### 129. Bulk Operations
Write efficient UPDATE or DELETE queries for large datasets.

### 130. Complex View
Create a VIEW that combines multiple complex calculations for easy reuse.

---

## Tips for Practice

1. **Start Simple**: Begin with Level 1 and work your way up
2. **Test Your Queries**: Use `!runsql` in Discord to run each query
3. **Check Results**: Verify your results make sense with the data
4. **Experiment**: Try variations of each question
5. **Combine Concepts**: Later questions often require combining multiple concepts
6. **Read Documentation**: SQLite documentation is excellent for learning
7. **Optimize**: Try to write queries multiple ways and compare performance
8. **Real Data**: These questions use your actual Discord data, making learning more engaging

## Common SQLite Functions Reference

### String Functions
- `LENGTH(text)` - Length of string
- `SUBSTR(text, start, length)` - Extract substring
- `TRIM(text)` - Remove whitespace
- `UPPER(text)` / `LOWER(text)` - Change case
- `REPLACE(text, old, new)` - Replace text
- `INSTR(text, substring)` - Find position

### Aggregate Functions
- `COUNT(*)` - Count rows
- `SUM(column)` - Sum values
- `AVG(column)` - Average
- `MIN(column)` / `MAX(column)` - Min/Max values
- `GROUP_CONCAT(column)` - Concatenate group values

### Date/Time Functions
- `DATE(timestamp)` - Extract date
- `TIME(timestamp)` - Extract time
- `STRFTIME(format, timestamp)` - Format date/time
- `DATETIME('now')` - Current datetime
- `JULIANDAY(timestamp)` - Convert to Julian day for arithmetic

### Conditional
- `CASE WHEN condition THEN value ELSE other END`
- `COALESCE(value1, value2, ...)` - Return first non-NULL
- `NULLIF(value1, value2)` - Return NULL if equal
- `IFNULL(value, default)` - Replace NULL

## Example Solutions (First 5 Questions)

### Question 1 Solution:
```sql
SELECT * FROM messages LIMIT 10
```

### Question 2 Solution:
```sql
SELECT author_name, content FROM messages
```

### Question 3 Solution:
```sql
SELECT COUNT(*) FROM messages
```

### Question 4 Solution:
```sql
SELECT COUNT(DISTINCT author_id) FROM messages
```

### Question 5 Solution:
```sql
SELECT * FROM messages WHERE author_id = 'YOUR_ID_HERE'
```

---

## Progressive Learning Path

- **Beginner (Q1-35)**: Basic SELECT, WHERE, ORDER BY
- **Intermediate (Q36-80)**: Aggregates, GROUP BY, Subqueries
- **Advanced (Q81-110)**: String/Date functions, Window functions
- **Expert (Q111-130)**: Complex analytics, Optimization

By completing all 130 questions, you'll have mastered:
- Data retrieval and filtering
- Aggregation and grouping
- Joins and subqueries
- String and date manipulation
- Window functions
- Query optimization
- Real-world data analysis

Good luck on your SQL journey! 🚀

---

*Remember: The best way to learn SQL is by doing. Don't just read the questions—write and run the queries!*