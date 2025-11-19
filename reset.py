import sqlite3

# Connect to the database
conn = sqlite3.connect('participants.db')
cursor = conn.cursor()

# The command to reset everyone
cursor.execute("UPDATE participants SET status = 'Pending'")
conn.commit()

print("✅ Database Reset! Everyone is marked as Pending.")
conn.close()