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
    ('Anushka Kannawar',),
    ('Shivtej Ghorpade',),
    ('Sarthak Shantishwar Patil',),
    ('Darshan Bari',),
    ('Om Gupta',),
    ('Bhagyashri Ramrao Aale',),
    ('SHIVAM SHANKAR HIPPALGAVE',),
    ('Rishikesh katare',),
    ('Arib Momin',),
    ('Vikas Bhawarlal Choudhari',),
    ('Ashish kalaskar',),
    ('Indra Tammewar',),
    ('Siddharth Kumbhar',),
    ('Smita Santosh Sabale',),
    ('Vaibhavi Rasal',),
    ('Ashish Ganpurwar',),
    ('Sarthak Galande',),
    ('Soham Devanand Mundhe',),
    ('Mansi Kanhaiyalal Suryawanshi',),
    ('Somit Bante',),
    ('Riya Sharma',),
    ('Shreeya Shukla',),
    ('Tanmay Deepak Patharkar',),
    ('Chirag Mutha',),
    ('Sairaj Abhinandan Patil',),
    ('OMKAR SHANKAR JADHAV',),
    ('Samarth Hannure',),
    ('Sneha Sadanand Gurav',),
    ('Ashish Maruti Biradar',),
    ('Namrata Santosh Mane',),
    ('Pratik Bhopi',),
    ('Ayush Jha',),
    ('Vedant Desai',),
    ('Harshali Nimje',),
    ('Shreyas Uddhav Bhosale',),
    ('Sumeet Sandeep Patil',),
    ('Ketan Rakesh Chavan',),
    ('Jyotiraditya ukey',),
    ('Shreya Shrikrishna Sankpal',),
    ('Srushti Kapase',),
    ('Manasvi Sandeep Gite',),
    ('Chanchal Sharma',),
    ('Yash jayram mane',),
    ('Ajinkya Santosh Gund',),
    ('Sumit Chame',),
    ('Mahir Amar Mulani',),
    ('Pawan Ramesh Dhatbale',),
    ('Sushrut kale',),
    ('Aditya Navnath Tarle',),
    ('Lalitlaxmi Dyawarkonda',),
    ('Mitesh Prashant Bandgar',),
    ('Samrudhi bapurav ithape',),
    ('Shaikh Sahil Abdul Rahim',),
    ('Aditya Bhadade',),
    ('Ankit Chaudhari',),
    ('Shourya Satish Thorat',),
    ('Ishan Sandeep kanchan',),
    ('Yogita Umakant Gaikwad',),
    ('Siddhesh Abasaheb Mane',),
    ('ADITYA KEKAN',),
    ('Rima Vishwakarma',),
    ('Pushkar Parakh',),
    ('Niranjan Sanjay Shinde',),
    ('Krishna shirgire',),
    ('Yogeshwari Shailesh Thombare',),
    ('Shivani patale',),
    ('Akash Barage',),
    ('Jidnyesh Suryawanshi',),
    ('Saiprasad Ashokrao Kawdikar',),
    ('Raiyyan  Shaikh',),
    ('MEHUL MAHESH PATIL',),
    ('Prithviraj Patil',),
    ('Om praveen chawan',),
    ('Abhishek Vitthal Patil',),
    ('Aarsh Joshi',),
    ('Gauri Vinod Gandre',),
    ('Dipakshi Chanchlani',),
    ('Krutika Anil Korade',),
    ('Meghna dafade',),
    ('Sujal samadiya',),
    ('Mansi Gorakh Chandgude',),
    ('Rajdeep Ashok Avhad',),
    ('Swamini Bhagwat',),
    ('Vinayak ramdas barade',),
    ('Jayesh Bhikan Shimpi',),
    ('Kale Aniket Govind',),
    ('Khushi Roongta',),
    ('Esha hemant Khapane',),
    ('Rutuja Nitin Patil',),
    ('Umesh shivaji kuyate',),
    ('Yashraj Santosh Zagade',),
    ('Pritam Pramod Tatkari',),
    ('Anuj Kadlag',),
    ('Jayesh Gajanan Jadhav',),
    ('Utkarsha Khadse',),
    ('Jadhav Vishal Bhausaheb',)
]
cursor.executemany("INSERT INTO participants (full_name) VALUES (?)", names_to_add)

# Save (commit) the changes and close
conn.commit()
conn.close()

print("Done! Your 'participants.db' file is ready.")