# SQL Practice Questions - Answer Key

Complete solutions for all 130 SQL practice questions from SQL_PRACTICE.md

---

## Level 1: Basic SELECT Queries (Answers 1-10)

### 1. Select Everything
```sql
SELECT * FROM messages LIMIT 10
```

### 2. Select Specific Columns
```sql
SELECT author_name, content FROM messages
```

### 3. Count Total Messages
```sql
SELECT COUNT(*) FROM messages
```

### 4. Count Unique Authors
```sql
SELECT COUNT(DISTINCT author_id) FROM messages
```

### 5. Find Your Messages
```sql
SELECT * FROM messages WHERE author_id = '536875405819379733'
```

### 6. Limit Results
```sql
SELECT * FROM messages LIMIT 20
```

### 7. Non-Empty Messages
```sql
SELECT * FROM messages WHERE content IS NOT NULL AND content != ''
```

### 8. Messages with Attachments
```sql
SELECT * FROM messages WHERE attachments IS NOT NULL AND attachments != ''
```

### 9. Specific Author by Name
```sql
SELECT * FROM messages WHERE author_name = 'specific_username'
```

### 10. Select Distinct Author Names
```sql
SELECT DISTINCT author_name FROM messages
```

---

## Level 2: WHERE Clauses & Filtering (Answers 11-25)

### 11. Messages Containing a Word
```sql
SELECT * FROM messages WHERE LOWER(content) LIKE '%discord%'
```

### 12. Messages NOT Containing a Word
```sql
SELECT * FROM messages WHERE content NOT LIKE '%http%'
```

### 13. Long Messages
```sql
SELECT * FROM messages WHERE LENGTH(content) > 200
```

### 14. Short Messages
```sql
SELECT * FROM messages WHERE LENGTH(content) <= 10
```

### 15. Multiple Conditions (AND)
```sql
SELECT * FROM messages 
WHERE author_id = '536875405819379733' 
AND LOWER(content) LIKE '%discord%'
```

### 16. Multiple Conditions (OR)
```sql
SELECT * FROM messages 
WHERE LOWER(content) LIKE '%hello%' 
OR LOWER(content) LIKE '%hi%'
```

### 17. Date Range Filter
```sql
SELECT * FROM messages 
WHERE created_at >= '2025-12-01' 
AND created_at < '2026-01-01'
```

### 18. Recent Messages
```sql
SELECT * FROM messages WHERE created_at > '2026-01-01'
```

### 19. Message ID Range
```sql
SELECT * FROM messages 
WHERE message_id BETWEEN '1000000000000000000' AND '2000000000000000000'
```

### 20. Exclude Multiple Authors
```sql
SELECT * FROM messages 
WHERE author_id NOT IN ('123456789', '987654321', '555555555')
```

### 21. Pattern Matching with LIKE
```sql
SELECT * FROM messages WHERE content LIKE 'I think%'
```

### 22. Pattern Matching - Ends With
```sql
SELECT * FROM messages WHERE content LIKE '%?'
```

### 23. Pattern Matching - Contains
```sql
SELECT * FROM messages 
WHERE LOWER(content) LIKE '%lol%' 
OR LOWER(content) LIKE '%lmao%'
```

### 24. NULL Values
```sql
SELECT * FROM messages WHERE attachments IS NULL OR attachments = ''
```

### 25. Complex Filter
```sql
SELECT * FROM messages 
WHERE is_tracked(author_id) = 1 
AND LENGTH(content) > 100 
AND content LIKE '%http%'
```

---

## Level 3: Sorting & Ordering (Answers 26-35)

### 26. Sort by Date (Ascending)
```sql
SELECT * FROM messages ORDER BY created_at ASC
```

### 27. Sort by Date (Descending)
```sql
SELECT * FROM messages ORDER BY created_at DESC
```

### 28. Sort by Author Name
```sql
SELECT * FROM messages ORDER BY author_name ASC
```

### 29. Sort by Message Length
```sql
SELECT *, LENGTH(content) as msg_length 
FROM messages 
ORDER BY msg_length DESC
```

### 30. Multiple Sort Criteria
```sql
SELECT * FROM messages ORDER BY author_name ASC, created_at ASC
```

### 31. Top 10 Longest Messages
```sql
SELECT *, LENGTH(content) as length 
FROM messages 
ORDER BY length DESC 
LIMIT 10
```

### 32. Most Recent Messages per Author
```sql
SELECT author_id, author_name, MAX(created_at) as last_message
FROM messages
GROUP BY author_id
ORDER BY last_message DESC
```

### 33. Sort by Word Count
```sql
SELECT *, word_count(content) as words 
FROM messages 
ORDER BY words DESC
```

### 34. Random Sample
```sql
SELECT * FROM messages ORDER BY RANDOM() LIMIT 10
```

### 35. Sort NULL Values
```sql
SELECT * FROM messages 
ORDER BY CASE WHEN attachments IS NULL OR attachments = '' THEN 1 ELSE 0 END, attachments
```

---

## Level 4: Aggregate Functions (Answers 36-50)

### 36. COUNT All Messages
```sql
SELECT COUNT(*) as total_messages FROM messages
```

### 37. COUNT Distinct Authors
```sql
SELECT COUNT(DISTINCT author_id) as unique_authors FROM messages
```

### 38. AVG Message Length
```sql
SELECT AVG(LENGTH(content)) as avg_length FROM messages
```

### 39. MAX Message Length
```sql
SELECT MAX(LENGTH(content)) as max_length FROM messages
```

### 40. MIN and MAX Dates
```sql
SELECT MIN(created_at) as first_message, MAX(created_at) as last_message 
FROM messages
```

### 41. SUM of Word Counts
```sql
SELECT SUM(word_count(content)) as total_words FROM messages
```

### 42. COUNT with WHERE
```sql
SELECT COUNT(*) as thank_messages 
FROM messages 
WHERE LOWER(content) LIKE '%thanks%'
```

### 43. AVG Sentiment Score
```sql
SELECT AVG(sentiment_polarity(content)) as avg_sentiment FROM messages
```

### 44. COUNT Messages per Author
```sql
SELECT author_name, COUNT(*) as message_count 
FROM messages 
GROUP BY author_id
```

### 45. MAX Sentiment per Author
```sql
SELECT author_name, MAX(sentiment_polarity(content)) as max_sentiment
FROM messages
GROUP BY author_id
```

### 46. Average Word Count per Author
```sql
SELECT author_name, AVG(word_count(content)) as avg_words
FROM messages
GROUP BY author_id
```

### 47. Messages by Date
```sql
SELECT DATE(created_at) as day, COUNT(*) as message_count
FROM messages
GROUP BY day
ORDER BY day
```

### 48. COUNT with Multiple Conditions
```sql
SELECT COUNT(*) as positive_long_messages
FROM messages
WHERE LENGTH(content) > 100 
AND sentiment_polarity(content) > 0.2
```

### 49. Standard Statistics
```sql
SELECT 
    COUNT(*) as count,
    AVG(LENGTH(content)) as avg_length,
    MIN(LENGTH(content)) as min_length,
    MAX(LENGTH(content)) as max_length
FROM messages
```

### 50. Percentage Calculation
```sql
SELECT 
    COUNT(*) as total_messages,
    SUM(CASE WHEN attachments != '' AND attachments IS NOT NULL THEN 1 ELSE 0 END) as with_attachments,
    ROUND(100.0 * SUM(CASE WHEN attachments != '' AND attachments IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as percentage
FROM messages
```

---

## Level 5: GROUP BY & HAVING (Answers 51-65)

### 51. Messages per Author
```sql
SELECT author_name, COUNT(*) as message_count
FROM messages
GROUP BY author_id
```

### 52. Sort Grouped Results
```sql
SELECT author_name, COUNT(*) as message_count
FROM messages
GROUP BY author_id
ORDER BY message_count DESC
```

### 53. HAVING Clause - Filter Groups
```sql
SELECT author_name, COUNT(*) as message_count
FROM messages
GROUP BY author_id
HAVING COUNT(*) > 100
```

### 54. Multiple Aggregates in GROUP BY
```sql
SELECT 
    author_name,
    COUNT(*) as message_count,
    AVG(LENGTH(content)) as avg_length,
    SUM(word_count(content)) as total_words
FROM messages
GROUP BY author_id
```

### 55. GROUP BY Date
```sql
SELECT DATE(created_at) as day, COUNT(*) as message_count
FROM messages
GROUP BY day
ORDER BY day
```

### 56. GROUP BY with WHERE
```sql
SELECT real_name(author_id) as person, COUNT(*) as message_count
FROM messages
WHERE is_tracked(author_id) = 1
GROUP BY real_name(author_id)
```

### 57. HAVING with Multiple Conditions
```sql
SELECT 
    author_name,
    COUNT(*) as message_count,
    AVG(sentiment_polarity(content)) as avg_sentiment
FROM messages
GROUP BY author_id
HAVING COUNT(*) > 500 AND AVG(sentiment_polarity(content)) > 0.1
```

### 58. Top 10 Most Active Authors
```sql
SELECT author_name, COUNT(*) as message_count
FROM messages
GROUP BY author_id
ORDER BY message_count DESC
LIMIT 10
```

### 59. GROUP BY Sentiment Label
```sql
SELECT sentiment_label(content) as sentiment, COUNT(*) as count
FROM messages
GROUP BY sentiment
```

### 60. Average Sentiment per Tracked User
```sql
SELECT 
    real_name(author_id) as person,
    AVG(sentiment_polarity(content)) as avg_sentiment
FROM messages
WHERE is_tracked(author_id) = 1
GROUP BY real_name(author_id)
ORDER BY avg_sentiment DESC
```

### 61. Messages per Month
```sql
SELECT STRFTIME('%Y-%m', created_at) as month, COUNT(*) as message_count
FROM messages
GROUP BY month
ORDER BY month
```

### 62. GROUP BY Hour of Day
```sql
SELECT STRFTIME('%H', created_at) as hour, COUNT(*) as message_count
FROM messages
GROUP BY hour
ORDER BY hour
```

### 63. Authors with Attachments
```sql
SELECT author_name, COUNT(*) as messages_with_attachments
FROM messages
WHERE attachments IS NOT NULL AND attachments != ''
GROUP BY author_id
ORDER BY messages_with_attachments DESC
```

### 64. GROUP BY Message Length Buckets
```sql
SELECT 
    CASE 
        WHEN LENGTH(content) < 50 THEN 'short'
        WHEN LENGTH(content) < 200 THEN 'medium'
        ELSE 'long'
    END as category,
    COUNT(*) as count
FROM messages
GROUP BY category
```

### 65. Most Subjective Authors
```sql
SELECT 
    author_name,
    AVG(sentiment_subjectivity(content)) as avg_subjectivity,
    COUNT(*) as message_count
FROM messages
GROUP BY author_id
HAVING COUNT(*) >= 100
ORDER BY avg_subjectivity DESC
LIMIT 10
```

---

## Level 6: JOINs & Subqueries (Answers 66-80)

### 66. Self-Join - Find Message Pairs
```sql
SELECT 
    m1.author_name,
    m1.created_at as first_message,
    m2.created_at as second_message
FROM messages m1
JOIN messages m2 ON m1.author_id = m2.author_id
WHERE m1.message_id < m2.message_id
AND JULIANDAY(m2.created_at) - JULIANDAY(m1.created_at) < (1.0/1440.0)
LIMIT 100
```

### 67. Subquery in WHERE
```sql
SELECT * FROM messages
WHERE author_id IN (
    SELECT author_id 
    FROM messages 
    GROUP BY author_id 
    HAVING COUNT(*) > 1000
)
```

### 68. Subquery in SELECT
```sql
SELECT 
    author_name,
    content,
    (SELECT COUNT(*) FROM messages m2 WHERE m2.author_id = messages.author_id) as author_total
FROM messages
LIMIT 100
```

### 69. Correlated Subquery
```sql
SELECT author_name, content, LENGTH(content) as length
FROM messages m1
WHERE LENGTH(content) > (
    SELECT AVG(LENGTH(content)) 
    FROM messages m2 
    WHERE m2.author_id = m1.author_id
)
LIMIT 100
```

### 70. IN Subquery
```sql
SELECT * FROM messages
WHERE author_id IN (
    SELECT author_id 
    FROM messages 
    GROUP BY author_id 
    ORDER BY COUNT(*) DESC 
    LIMIT 5
)
```

### 71. NOT IN Subquery
```sql
SELECT DISTINCT author_id, author_name
FROM messages
WHERE author_id NOT IN (
    SELECT DISTINCT author_id
    FROM messages
    WHERE sentiment_polarity(content) < -0.1
)
```

### 72. Subquery with MAX
```sql
SELECT * FROM messages
WHERE sentiment_polarity(content) = (
    SELECT MAX(sentiment_polarity(content)) FROM messages
)
```

### 73. Subquery in FROM (Derived Table)
```sql
SELECT * FROM (
    SELECT 
        author_name,
        COUNT(*) as msg_count,
        AVG(sentiment_polarity(content)) as avg_sentiment
    FROM messages
    GROUP BY author_id
) AS author_stats
WHERE msg_count > 500
ORDER BY avg_sentiment DESC
```

### 74. EXISTS Subquery
```sql
SELECT DISTINCT m1.author_id, m1.author_name
FROM messages m1
WHERE EXISTS (
    SELECT 1 FROM messages m2 
    WHERE m2.author_id = m1.author_id 
    AND m2.attachments IS NOT NULL 
    AND m2.attachments != ''
)
```

### 75. Multiple Subqueries
```sql
SELECT * FROM messages
WHERE author_id IN (
    SELECT author_id FROM messages GROUP BY author_id HAVING COUNT(*) > 1000
)
AND author_id IN (
    SELECT author_id FROM messages GROUP BY author_id HAVING AVG(sentiment_polarity(content)) > 0.15
)
```

### 76. WITH Clause (CTE) - Basic
```sql
WITH author_stats AS (
    SELECT 
        author_id,
        author_name,
        COUNT(*) as message_count,
        AVG(sentiment_polarity(content)) as avg_sentiment
    FROM messages
    GROUP BY author_id
)
SELECT * FROM author_stats
WHERE message_count > 500
ORDER BY avg_sentiment DESC
```

### 77. Multiple CTEs
```sql
WITH active_authors AS (
    SELECT author_id FROM messages GROUP BY author_id HAVING COUNT(*) > 1000
),
positive_authors AS (
    SELECT author_id FROM messages GROUP BY author_id HAVING AVG(sentiment_polarity(content)) > 0.15
)
SELECT DISTINCT m.author_name, COUNT(*) as message_count
FROM messages m
JOIN active_authors a ON m.author_id = a.author_id
JOIN positive_authors p ON m.author_id = p.author_id
GROUP BY m.author_id
```

### 78. Recursive CTE
```sql
WITH RECURSIVE numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 100
)
SELECT n FROM numbers
```

### 79. Subquery for Ranking
```sql
SELECT * FROM (
    SELECT 
        author_name,
        content,
        sentiment_polarity(content) as sentiment,
        ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY sentiment_polarity(content) DESC) as rank
    FROM messages
)
WHERE rank <= 3
```

### 80. Complex Nested Subquery
```sql
SELECT author_name, content, LENGTH(content) as length
FROM messages m1
WHERE LENGTH(content) >= (
    SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY LENGTH(content))
    FROM messages m2
    WHERE m2.author_id = m1.author_id
)
LIMIT 100
```
*Note: SQLite doesn't have PERCENTILE_CONT, use this alternative:*
```sql
SELECT author_name, content, LENGTH(content) as length
FROM messages m1
WHERE LENGTH(content) >= (
    SELECT LENGTH(content)
    FROM messages m2
    WHERE m2.author_id = m1.author_id
    ORDER BY LENGTH(content) DESC
    LIMIT 1 OFFSET (
        SELECT CAST(COUNT(*) * 0.1 AS INTEGER)
        FROM messages m3
        WHERE m3.author_id = m1.author_id
    )
)
LIMIT 100
```

---

## Level 7: Advanced String Functions (Answers 81-90)

### 81. SUBSTR - Extract Username
```sql
SELECT author_name, SUBSTR(author_name, 1, 10) as short_name
FROM messages
```

### 82. REPLACE - Clean Content
```sql
SELECT content, REPLACE(content, 'lol', 'haha') as cleaned_content
FROM messages
WHERE content LIKE '%lol%'
```

### 83. TRIM - Clean Whitespace
```sql
SELECT content, LENGTH(content) as original, LENGTH(TRIM(content)) as trimmed
FROM messages
WHERE LENGTH(content) != LENGTH(TRIM(content))
```

### 84. UPPER and LOWER
```sql
SELECT author_name, UPPER(author_name) as uppercase_name
FROM messages
```

### 85. LENGTH vs Custom word_count
```sql
SELECT 
    content,
    LENGTH(content) as char_count,
    word_count(content) as words,
    ROUND(LENGTH(content) * 1.0 / word_count(content), 2) as avg_word_length
FROM messages
WHERE word_count(content) > 0
LIMIT 100
```

### 86. INSTR - Find Position
```sql
SELECT content, INSTR(content, 'http') as link_position
FROM messages
WHERE content LIKE '%http%'
```

### 87. LIKE with Multiple Patterns
```sql
SELECT content
FROM messages
WHERE content LIKE '%😀%' 
   OR content LIKE '%😂%' 
   OR content LIKE '%❤%'
   OR content LIKE '%🔥%'
LIMIT 50
```

### 88. String Concatenation
```sql
SELECT 
    author_name || ' (' || DATE(created_at) || '): ' || SUBSTR(content, 1, 50) || '...' as formatted
FROM messages
LIMIT 100
```

### 89. CASE Statement - Categorize
```sql
SELECT 
    content,
    CASE 
        WHEN LENGTH(content) < 50 THEN 'short'
        WHEN LENGTH(content) < 200 THEN 'medium'
        ELSE 'long'
    END as category
FROM messages
```

### 90. CASE with Sentiment
```sql
SELECT 
    content,
    sentiment_polarity(content) as score,
    CASE 
        WHEN sentiment_polarity(content) > 0.5 THEN 'very positive'
        WHEN sentiment_polarity(content) > 0.1 THEN 'positive'
        WHEN sentiment_polarity(content) > -0.1 THEN 'neutral'
        WHEN sentiment_polarity(content) > -0.5 THEN 'negative'
        ELSE 'very negative'
    END as label
FROM messages
LIMIT 100
```

---

## Level 8: Date & Time Functions (Answers 91-100)

### 91. STRFTIME - Extract Year
```sql
SELECT STRFTIME('%Y', created_at) as year, COUNT(*) as message_count
FROM messages
GROUP BY year
```

### 92. STRFTIME - Extract Month
```sql
SELECT 
    CASE STRFTIME('%m', created_at)
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END as month,
    COUNT(*) as message_count
FROM messages
GROUP BY STRFTIME('%m', created_at)
ORDER BY STRFTIME('%m', created_at)
```

### 93. Day of Week Analysis
```sql
SELECT 
    CASE CAST(STRFTIME('%w', created_at) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_of_week,
    COUNT(*) as message_count
FROM messages
GROUP BY STRFTIME('%w', created_at)
ORDER BY message_count DESC
```

### 94. Hour of Day Analysis
```sql
SELECT STRFTIME('%H', created_at) as hour, COUNT(*) as message_count
FROM messages
GROUP BY hour
ORDER BY message_count DESC
```

### 95. Date Arithmetic
```sql
SELECT * FROM messages
WHERE JULIANDAY('now') - JULIANDAY(created_at) <= 30
```

### 96. Time Between Messages
```sql
WITH ordered_messages AS (
    SELECT 
        author_id,
        author_name,
        created_at,
        LAG(created_at) OVER (PARTITION BY author_id ORDER BY created_at) as prev_time
    FROM messages
)
SELECT 
    author_name,
    ROUND((JULIANDAY(created_at) - JULIANDAY(prev_time)) * 24 * 60, 2) as minutes_between
FROM ordered_messages
WHERE prev_time IS NOT NULL
LIMIT 100
```

### 97. Monthly Growth
```sql
WITH monthly_counts AS (
    SELECT 
        STRFTIME('%Y-%m', created_at) as month,
        COUNT(*) as count
    FROM messages
    GROUP BY month
)
SELECT 
    month,
    count,
    LAG(count) OVER (ORDER BY month) as prev_month,
    count - LAG(count) OVER (ORDER BY month) as growth
FROM monthly_counts
```

### 98. Weekend vs Weekday
```sql
SELECT 
    CASE 
        WHEN CAST(STRFTIME('%w', created_at) AS INTEGER) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as message_count,
    AVG(sentiment_polarity(content)) as avg_sentiment
FROM messages
GROUP BY day_type
```

### 99. Time of Day Sentiment
```sql
SELECT 
    CASE 
        WHEN CAST(STRFTIME('%H', created_at) AS INTEGER) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN CAST(STRFTIME('%H', created_at) AS INTEGER) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN CAST(STRFTIME('%H', created_at) AS INTEGER) BETWEEN 18 AND 22 THEN 'Evening'
        ELSE 'Night'
    END as time_of_day,
    COUNT(*) as message_count,
    AVG(sentiment_polarity(content)) as avg_sentiment
FROM messages
GROUP BY time_of_day
ORDER BY avg_sentiment DESC
```

### 100. Timezone Conversion
```sql
SELECT 
    created_at as utc_time,
    DATETIME(created_at, '+5 hours', '+45 minutes') as nepal_time
FROM messages
LIMIT 10
```

---

## Level 9: Window Functions (Answers 101-110)

### 101. ROW_NUMBER - Rank Messages
```sql
SELECT 
    ROW_NUMBER() OVER (ORDER BY created_at) as row_num,
    author_name,
    content,
    created_at
FROM messages
LIMIT 100
```

### 102. RANK - Rank Authors
```sql
SELECT 
    author_name,
    COUNT(*) as message_count,
    RANK() OVER (ORDER BY COUNT(*) DESC) as rank
FROM messages
GROUP BY author_id
```

### 103. DENSE_RANK
```sql
SELECT 
    author_name,
    COUNT(*) as message_count,
    DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) as dense_rank
FROM messages
GROUP BY author_id
```

### 104. NTILE - Quartiles
```sql
SELECT 
    author_name,
    COUNT(*) as message_count,
    NTILE(4) OVER (ORDER BY COUNT(*)) as quartile
FROM messages
GROUP BY author_id
```

### 105. LAG - Previous Value
```sql
SELECT 
    author_name,
    content,
    created_at,
    LAG(content) OVER (PARTITION BY author_id ORDER BY created_at) as previous_message
FROM messages
LIMIT 100
```

### 106. LEAD - Next Value
```sql
SELECT 
    author_name,
    content,
    created_at,
    LEAD(created_at) OVER (ORDER BY created_at) as next_timestamp
FROM messages
LIMIT 100
```

### 107. Running Total
```sql
SELECT 
    DATE(created_at) as day,
    COUNT(*) as daily_count,
    SUM(COUNT(*)) OVER (ORDER BY DATE(created_at)) as running_total
FROM messages
GROUP BY day
```

### 108. Moving Average
```sql
WITH daily_counts AS (
    SELECT 
        DATE(created_at) as day,
        COUNT(*) as count
    FROM messages
    GROUP BY day
)
SELECT 
    day,
    count,
    AVG(count) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7day
FROM daily_counts
```

### 109. Percent Rank
```sql
SELECT 
    author_name,
    COUNT(*) as message_count,
    PERCENT_RANK() OVER (ORDER BY COUNT(*)) as percentile
FROM messages
GROUP BY author_id
```

### 110. Window Frame
```sql
SELECT 
    message_id,
    content,
    sentiment_polarity(content) as sentiment,
    AVG(sentiment_polarity(content)) OVER (
        ORDER BY created_at 
        ROWS BETWEEN 5 PRECEDING AND 5 FOLLOWING
    ) as smoothed_sentiment
FROM messages
LIMIT 100
```

---

## Level 10: Expert Challenges (Answers 111-125)

### 111. Most Active Conversation
```sql
WITH hourly_buckets AS (
    SELECT 
        DATETIME(STRFTIME('%Y-%m-%d %H:00:00', created_at)) as hour_start,
        COUNT(*) as message_count
    FROM messages
    GROUP BY hour_start
)
SELECT hour_start, message_count
FROM hourly_buckets
ORDER BY message_count DESC
LIMIT 1
```

### 112. Sentiment Trends Over Time
```sql
SELECT 
    STRFTIME('%Y-%m', created_at) as month,
    AVG(sentiment_polarity(content)) as avg_sentiment,
    COUNT(*) as message_count
FROM messages
GROUP BY month
ORDER BY month
```

### 113. Author Similarity
```sql
WITH author_sentiments AS (
    SELECT 
        author_id,
        author_name,
        AVG(sentiment_polarity(content)) as avg_sentiment,
        AVG(sentiment_subjectivity(content)) as avg_subjectivity,
        AVG(word_count(content)) as avg_words
    FROM messages
    GROUP BY author_id
    HAVING COUNT(*) >= 100
)
SELECT 
    a1.author_name as author1,
    a2.author_name as author2,
    ABS(a1.avg_sentiment - a2.avg_sentiment) as sentiment_diff,
    ABS(a1.avg_subjectivity - a2.avg_subjectivity) as subjectivity_diff
FROM author_sentiments a1
JOIN author_sentiments a2 ON a1.author_id < a2.author_id
ORDER BY (sentiment_diff + subjectivity_diff)
LIMIT 10
```

### 114. Conversation Threads
```sql
WITH message_gaps AS (
    SELECT 
        message_id,
        author_name,
        created_at,
        LAG(created_at) OVER (ORDER BY created_at) as prev_time,
        (JULIANDAY(created_at) - JULIANDAY(LAG(created_at) OVER (ORDER BY created_at))) * 24 * 60 as gap_minutes
    FROM messages
)
SELECT 
    COUNT(*) as thread_size,
    MIN(created_at) as thread_start,
    MAX(created_at) as thread_end
FROM (
    SELECT 
        *,
        SUM(CASE WHEN gap_minutes > 5 OR gap_minutes IS NULL THEN 1 ELSE 0 END) 
            OVER (ORDER BY created_at) as thread_id
    FROM message_gaps
)
GROUP BY thread_id
ORDER BY thread_size DESC
LIMIT 20
```

### 115. Word Frequency Analysis
```sql
-- This requires splitting words, which is complex in SQLite
-- Here's a simplified version for the top words in short messages
WITH words AS (
    SELECT LOWER(TRIM(content)) as word
    FROM messages
    WHERE word_count(content) = 1
    AND LENGTH(content) > 2
    AND LENGTH(content) < 20
)
SELECT word, COUNT(*) as frequency
FROM words
GROUP BY word
ORDER BY frequency DESC
LIMIT 50
```

### 116. Activity Patterns
```sql
SELECT 
    real_name(author_id) as person,
    SUM(CASE WHEN CAST(STRFTIME('%w', created_at) AS INTEGER) IN (0, 6) THEN 1 ELSE 0 END) as weekend_msgs,
    SUM(CASE WHEN CAST(STRFTIME('%w', created_at) AS INTEGER) NOT IN (0, 6) THEN 1 ELSE 0 END) as weekday_msgs,
    ROUND(1.0 * SUM(CASE WHEN CAST(STRFTIME('%w', created_at) AS INTEGER) IN (0, 6) THEN 1 ELSE 0 END) / 
          SUM(CASE WHEN CAST(STRFTIME('%w', created_at) AS INTEGER) NOT IN (0, 6) THEN 1 ELSE 0 END), 2) as weekend_ratio
FROM messages
WHERE is_tracked(author_id) = 1
GROUP BY real_name(author_id)
ORDER BY weekend_ratio DESC
```

### 117. Response Time Analysis
```sql
WITH conversations AS (
    SELECT 
        author_id,
        created_at,
        LAG(created_at) OVER (ORDER BY created_at) as prev_time,
        LAG(author_id) OVER (ORDER BY created_at) as prev_author
    FROM messages
)
SELECT 
    AVG((JULIANDAY(created_at) - JULIANDAY(prev_time)) * 24 * 60) as avg_response_minutes
FROM conversations
WHERE prev_author != author_id
AND (JULIANDAY(created_at) - JULIANDAY(prev_time)) * 24 * 60 < 10
```

### 118. Sentiment Shift Detection
```sql
WITH monthly_sentiment AS (
    SELECT 
        real_name(author_id) as person,
        STRFTIME('%Y-%m', created_at) as month,
        AVG(sentiment_polarity(content)) as avg_sentiment
    FROM messages
    WHERE is_tracked(author_id) = 1
    GROUP BY person, month
),
sentiment_changes AS (
    SELECT 
        person,
        month,
        avg_sentiment,
        LAG(avg_sentiment) OVER (PARTITION BY person ORDER BY month) as prev_sentiment,
        avg_sentiment - LAG(avg_sentiment) OVER (PARTITION BY person ORDER BY month) as change
    FROM monthly_sentiment
)
SELECT person, month, avg_sentiment, prev_sentiment, change
FROM sentiment_changes
WHERE ABS(change) > 0.2
ORDER BY ABS(change) DESC
```

### 119. Top Words by Author
```sql
-- Simplified version for single-word messages
WITH author_words AS (
    SELECT 
        real_name(author_id) as person,
        LOWER(TRIM(content)) as word
    FROM messages
    WHERE is_tracked(author_id) = 1
    AND word_count(content) = 1
    AND LENGTH(content) > 2
    AND LENGTH(content) < 20
)
SELECT person, word, COUNT(*) as frequency
FROM author_words
GROUP BY person, word
ORDER BY person, frequency DESC
```

### 120. Cohort Analysis
```sql
WITH first_message AS (
    SELECT author_id, MIN(DATE(created_at)) as join_date
    FROM messages
    GROUP BY author_id
),
cohorts AS (
    SELECT 
        STRFTIME('%Y-%m', join_date) as cohort,
        author_id
    FROM first_message
)
SELECT 
    c.cohort,
    COUNT(DISTINCT c.author_id) as cohort_size,
    AVG(
        (SELECT COUNT(*) FROM messages m WHERE m.author_id = c.author_id)
    ) as avg_messages_per_user
FROM cohorts c
GROUP BY c.cohort
ORDER BY c.cohort
```

### 121. Emoji Usage
```sql
-- Simplified: Count messages with common emojis
SELECT 
    SUM(CASE WHEN content LIKE '%😀%' OR content LIKE '%😃%' OR content LIKE '%😄%' THEN 1 ELSE 0 END) as happy_face,
    SUM(CASE WHEN content LIKE '%😂%' OR content LIKE '%🤣%' THEN 1 ELSE 0 END) as laughing,
    SUM(CASE WHEN content LIKE '%❤%' OR content LIKE '%💕%' THEN 1 ELSE 0 END) as heart,
    SUM(CASE WHEN content LIKE '%🔥%' THEN 1 ELSE 0 END) as fire,
    SUM(CASE WHEN content LIKE '%👍%' THEN 1 ELSE 0 END) as thumbs_up
FROM messages
```

### 122. Message Burst Detection
```sql
WITH message_times AS (
    SELECT 
        author_id,
        author_name,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY created_at) as msg_num
    FROM messages
),
bursts AS (
    SELECT 
        m1.author_name,
        m1.created_at as burst_start,
        m5.created_at as burst_end,
        (JULIANDAY(m5.created_at) - JULIANDAY(m1.created_at)) * 24 * 60 as duration_minutes
    FROM message_times m1
    JOIN message_times m5 ON m1.author_id = m5.author_id AND m5.msg_num = m1.msg_num + 4
    WHERE (JULIANDAY(m5.created_at) - JULIANDAY(m1.created_at)) * 24 * 60 <= 1
)
SELECT * FROM bursts
ORDER BY burst_start
```

### 123. Content Similarity
```sql
-- Simple similarity: same length and similar sentiment
WITH message_pairs AS (
    SELECT 
        m1.message_id as msg1_id,
        m1.content as msg1_content,
        m2.message_id as msg2_id,
        m2.content as msg2_content,
        ABS(LENGTH(m1.content) - LENGTH(m2.content)) as length_diff,
        ABS(sentiment_polarity(m1.content) - sentiment_polarity(m2.content)) as sentiment_diff
    FROM messages m1
    JOIN messages m2 ON m1.message_id < m2.message_id
    WHERE LENGTH(m1.content) > 50
    AND LENGTH(m2.content) > 50
    LIMIT 10000
)
SELECT msg1_content, msg2_content, length_diff, sentiment_diff
FROM message_pairs
WHERE length_diff < 10 AND sentiment_diff < 0.1
LIMIT 20
```

### 124. Sentiment Volatility
```sql
WITH author_sentiments AS (
    SELECT 
        author_id,
        author_name,
        sentiment_polarity(content) as sentiment
    FROM messages
),
stats AS (
    SELECT 
        author_name,
        AVG(sentiment) as avg_sentiment,
        COUNT(*) as msg_count,
        -- Standard deviation calculation
        SQRT(AVG(sentiment * sentiment) - AVG(sentiment) * AVG(sentiment)) as std_dev
    FROM author_sentiments
    GROUP BY author_id
    HAVING COUNT(*) >= 100
)
SELECT author_name, avg_sentiment, std_dev, msg_count
FROM stats
ORDER BY std_dev DESC
```

### 125. Comprehensive Analytics Dashboard
```sql
WITH stats AS (
    SELECT 
        COUNT(*) as total_messages,
        COUNT(DISTINCT author_id) as unique_authors,
        MIN(created_at) as first_message,
        MAX(created_at) as last_message,
        AVG(sentiment_polarity(content)) as avg_sentiment,
        AVG(LENGTH(content)) as avg_length
    FROM messages
),
top_authors AS (
    SELECT author_name, COUNT(*) as count
    FROM messages
    GROUP BY author_id
    ORDER BY count DESC
    LIMIT 5
),
sentiment_dist AS (
    SELECT 
        sentiment_label(content) as label,
        COUNT(*) as count
    FROM messages
    GROUP BY label
),
day_of_week AS (
    SELECT 
        CASE CAST(STRFTIME('%w', created_at) AS INTEGER)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END as day,
        COUNT(*) as count
    FROM messages
    GROUP BY STRFTIME('%w', created_at)
)
SELECT 
    'Total Messages: ' || total_messages ||
    ' | Unique Authors: ' || unique_authors ||
    ' | Date Range: ' || DATE(first_message) || ' to ' || DATE(last_message) ||
    ' | Avg Sentiment: ' || ROUND(avg_sentiment, 3) ||
    ' | Avg Length: ' || ROUND(avg_length, 1) as dashboard
FROM stats
```

---

## Bonus: Performance & Optimization (Answers 126-130)

### 126. Query Plan Analysis
```sql
EXPLAIN QUERY PLAN
SELECT author_name, COUNT(*) as msg_count
FROM messages
WHERE is_tracked(author_id) = 1
GROUP BY author_id
ORDER BY msg_count DESC
```

### 127. Index Creation
```sql
-- Create indexes for common query patterns
CREATE INDEX idx_author_id ON messages(author_id);
CREATE INDEX idx_created_at ON messages(created_at);
CREATE INDEX idx_author_created ON messages(author_id, created_at);

-- Check if index helps
EXPLAIN QUERY PLAN
SELECT * FROM messages WHERE author_id = '536875405819379733' ORDER BY created_at;
```

### 128. Query Optimization
```sql
-- SLOW: Subquery in SELECT
SELECT 
    author_name,
    (SELECT COUNT(*) FROM messages m2 WHERE m2.author_id = messages.author_id) as total
FROM messages;

-- FAST: Use GROUP BY instead
SELECT author_name, COUNT(*) as total
FROM messages
GROUP BY author_id;
```

### 129. Bulk Operations
```sql
-- Efficient bulk update example
UPDATE messages 
SET author_name = REPLACE(author_name, 'old_name', 'new_name')
WHERE author_name LIKE '%old_name%';

-- Efficient bulk delete
DELETE FROM messages
WHERE LENGTH(content) < 2 
AND attachments IS NULL;
```

### 130. Complex View
```sql
CREATE VIEW author_analytics AS
SELECT 
    real_name(author_id) as person,
    COUNT(*) as total_messages,
    AVG(sentiment_polarity(content)) as avg_sentiment,
    AVG(sentiment_subjectivity(content)) as avg_subjectivity,
    AVG(word_count(content)) as avg_words,
    SUM(CASE WHEN attachments != '' THEN 1 ELSE 0 END) as messages_with_attachments,
    MIN(created_at) as first_message,
    MAX(created_at) as last_message,
    COUNT(DISTINCT DATE(created_at)) as active_days
FROM messages
WHERE is_tracked(author_id) = 1
GROUP BY real_name(author_id);

-- Now you can query it easily:
SELECT * FROM author_analytics ORDER BY avg_sentiment DESC;
```

---

## Pro Tips for Using These Answers

1. **Don't just copy-paste**: Understand what each query does
2. **Modify and experiment**: Change the LIMIT, add WHERE clauses, try different columns
3. **Compare approaches**: Some questions have multiple valid solutions
4. **Test on your data**: Your results will be unique to your Discord archive
5. **Combine techniques**: Advanced queries often use multiple concepts together
6. **Check performance**: Use EXPLAIN QUERY PLAN for slow queries
7. **Build incrementally**: Start with simple queries and add complexity

## Common Patterns to Remember

### Pattern 1: Top N per Group
```sql
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY sentiment DESC) as rn
    FROM messages
) WHERE rn <= 3
```

### Pattern 2: Running Calculations
```sql
SELECT 
    date,
    value,
    SUM(value) OVER (ORDER BY date) as running_total,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg
FROM data
```

### Pattern 3: Conditional Aggregation
```sql
SELECT 
    author_id,
    SUM(CASE WHEN condition THEN 1 ELSE 0 END) as count_matching,
    AVG(CASE WHEN condition THEN value END) as avg_matching
FROM messages
GROUP BY author_id
```

### Pattern 4: Self-Join for Comparisons
```sql
SELECT a.*, b.*
FROM table a
JOIN table b ON a.key = b.key AND a.id < b.id
WHERE condition
```

---

**Congratulations!** If you've worked through all 130 questions, you're now a SQL master! 🎉

Keep practicing and exploring your data - SQL is a skill that improves with use!