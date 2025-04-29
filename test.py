import os
import django
import sqlite3
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "raofoodapi.settings")
django.setup()

from aiapi.models import Questions


sqlite_db_path = "backup.db"
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS userapi_questions (
    id INTEGER PRIMARY KEY,
    topic TEXT UNIQUE,
    questions TEXT
)
""")

rows = Questions.objects.all()
for row in rows:
    cursor.execute(
        "INSERT OR REPLACE INTO userapi_questions (id, topic, questions) VALUES (?, ?, ?)",
        (row.id, row.topic, json.dumps(row.questions))
    )

conn.commit()
conn.close()
print(f"✅ {len(rows)} rows copied from PostgreSQL to {sqlite_db_path}")
