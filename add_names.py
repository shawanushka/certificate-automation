# add_names.py
import sqlite3

DB_FILE = 'participants.db'

# --- Add your new names here ---
new_people = [
    ('Anushka Shaw',),
    ('Aditya Kotkar',),
    ('Avinash Shaw',)
]
# -------------------------------

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# We now insert with the 'status' as 'Pending'
# (Or NULL, which our main script will also catch)
for (name,) in new_people:
    try:
        cursor.execute("INSERT INTO participants (full_name, status) VALUES (?, 'Pending')", (name,))
        print(f"Added new participant: {name}")
    except Exception as e:
        print(f"Could not add {name}: {e}")

conn.commit()
conn.close()

print(f"Successfully added {len(new_people)} new participants.")