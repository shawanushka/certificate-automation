# upgrade_database.py
import sqlite3

DB_FILE = 'participants.db'

print("Connecting to database to add 'status' column...")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

try:
    # This command adds a new column called 'status'
    cursor.execute("ALTER TABLE participants ADD COLUMN status TEXT")
    print("Successfully added 'status' column.")
    
    # NOW, let's mark all your *existing* names as 'Done'
    # so the robot doesn't re-upload them.
    cursor.execute("UPDATE participants SET status = 'Done'")
    print(f"Marked {cursor.rowcount} existing participants as 'Done'.")

except sqlite3.OperationalError as e:
    # This will happen if you try to run it a second time
    print(f"Skipping: {e}")

conn.commit()
conn.close()

print("Database upgrade complete!")