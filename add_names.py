import sqlite3

# The final 8 names with their missing letters restored!
final_names = [
    "Pranjali Bhushan Bhandari",
    "SAMRUDDHI BHAUSAHEB MATE",
    "Komal Machhindra Yerkal",
    "Diksha Sanjay Anandpure",
    "Gayatri Digambar Udage",
    "Pranav Prashant Shripannavar",
    "Anushka Namdev Roman",
    "Bapurao Pandit Pimparkar"
]

def main():
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    added_count = 0
    for name in final_names:
        try:
            # Adding them as 'Pending' so the factory picks them up
            cursor.execute("INSERT INTO participants (full_name, status) VALUES (?, 'Pending')", (name,))
            added_count += 1
        except Exception as e:
            print(f"  ⚠️ Could not add {name}: {e}")

    conn.commit()
    print(f"✅ Successfully added the final {added_count} names!")
    conn.close()

if __name__ == '__main__':
    main()