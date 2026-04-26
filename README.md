# User Session Analyzer

A Python tool for storing, managing, and analyzing user activity sessions using SQLite and pandas.

The project was built as a practice backend/data processing system to simulate basic analytics pipeline: data collection → storage → analysis.

## Features
- Create and store user activity sessions
- Persist data in SQLite database
- Analyze session data using pandas
- Filter sessions by category and time range
- Generate basic usage statistics

## Technologies
- Python
- SQLite
- pandas
- unittest

## Example usage
```python
from session_tracker import SessionTracker

tracker = SessionTracker()
tracker.add_session(user="user1", category="study", duration=45)

stats = tracker.get_statistics()
print(stats)
