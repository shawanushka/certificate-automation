# setup_database.py
import sqlite3

# This creates or opens the database file
conn = sqlite3.connect('participants.db')
cursor = conn.cursor()

# Makes the "folder" (table) to hold names
cursor.execute('''
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL
)
''')

# Add some names (you can add more!)
print("Adding names to the database...")
names_to_add = [
    ('Sarthak Patil',),
('Darshan Bari',),
('Om Gupta',),
('Bhagyashri Aale',),
('Shivam Hippalgave',),
('Arib Momin',),
('Vikas Choudhari',),
('Ashish Kalaskar',),
('Indra Tammewar',),
('Siddharth Kumbhar',),
('Smita Sabale',),
('Vaibhavi Rasal',),
('Ashish Ganpurwar',),
('Sarthak Galande',),
('Soham Mundhe',),
('Mansi Suryawanshi',),
('Somit Bante',),
('Riya Sharma',),
('Shreeya Shukla',),
('Tanmay Patharkar',),
('Chirag Mutha',),
('Sairaj Patil',),
('Omkar Jadhav',),
('Samarth Hannure',),
('Ashish Biradar',),
('Pratik Bhopi',),
('Ayush Jha',),
('Harshali Nimje',),
('Shreyas Bhosale',),
('Ketan Chavan',),
('Jyotiraditya Ukey',),
('Shreya Sankpal',),
('Srushti Kapase',),
('Manasvi Gite',),
('Chanchal Sharma',),
('Ajinkya Gund',),
('Sumit Chame',),
('Pawan Dhatbale',),
('Sushrut Kale',),
('Lalitlaxmi Dyawarkonda',),
('Mitesh Bandgar',),
('Samrudhi Ithape',),
('Shaikh Sahil Abdul Rahim',),
('Ankit Chaudhari',),
('Shourya Thorat',),
('Ishan Kanchan',),
('Yogita Gaikwad',),
('Siddhesh Mane',),
('Rima Vishwakarma',),
('Pushkar Parakh',),
('Niranjan Shinde',),
('Yogeshwari Thombare',),
('Jidnyesh Suryawanshi',),
('Raiyyan Shaikh',),
('Mehul Patil',),
('Om Chawan',),
('Abhishek Patil',),
('Aarsh Joshi',),
('Gauri Gandre',),
('Meghna Dafade',),
('Sujal Samadiya',),
('Mansi Chandgude',),
('Swamini Bhagwat',),
('Jayesh Shimpi',),
('Aniket Kale',),
('Khushi Roongta',),
('Esha Khapane',),
('Rutuja Nitin Patil',),
('Umesh Kuyate',),
('Yashraj Zagade',),
('Pritam Tatkari',),
('Anuj Kadlag',),
('Utkarsha Khadse',),
('Vishal Jadhav',)

]
cursor.executemany("INSERT INTO participants (full_name) VALUES (?)", names_to_add)

# Save (commit) the changes and close
conn.commit()
conn.close()

print("Done! Your 'participants.db' file is ready.")