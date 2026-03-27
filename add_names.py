import sqlite3

# The absolutely final, perfectly capitalized master list!
final_participants = [
    "Ajinkya Prabhakar Magar", "Krushna Donge", "Rohit Marewar", "Kiran Nandi",
    "Vishal Sanjay Daregave", "Om Gajanan Sapdhare", "Purva Jagannath Jadhav",
    "Pranjali Bhushan Bhandari", "Gayatri Pandharinath Gaikwad", "Ashish Kalaskar", 
    "Prajeeta Pathare", "Nutan Wagh", "Varsharani Shivaji Patil", "Kajal Kondaji Sawant", 
    "Ashwam Wankhede", "Prathamesh Raju Dalvi", "Dipali Khamkar", "Kunal Rushikesh Patil", 
    "Bhoomi Sengar", "Chakradhar", "Pawan Balu Gorad", "Arya Milind Dilliwale", 
    "Samruddhi Bhausaheb Mate", "Komal Machhindra Yerkal", "Diksha Sanjay Anandpure", 
    "Gayatri Digambar Udage", "Pranav Prashant Shripannavar", "Nayna Sanjay Mahajan", 
    "Anushka Shaw", "Aditya Sonakanalli", "Gauri Gandre", "Kritika Nitin Agrawal", 
    "Toshal Patil", "Siddhi Garg", "Aman Deep Singh", "Balaji Navnath Jagdale", 
    "Tanaya Sudhir Mukwane", "Vaishnavi Sanjay Bade", "Naman Ram Dhanwala", "Aryan Late", 
    "Gurpratap Singh Sandhu", "Kaushal Hadke", "Samiksha Sunil Hubale", "Tejas Maddewad", 
    "Chetan Pradip Lokhande", "Preeti Kamble", "Ayush Nilesh Shinde", "Anushka Namdev Roman", 
    "Bapurao Pandit Pimparkar", "Tejas Nagpure", "Pooja Kauchale", "Sahil Karande", 
    "Sarthak Joshi", "Akash Jigjeni", "Avinash Borkar", "Purvesh", "Prathmesh Bhadule", 
    "Shreya Pramod Babar", "Avinash Shaw"
]

def main():
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    # Wipe the database clean for the final run
    cursor.execute("DELETE FROM participants")
    print("🗑️ Database wiped clean!")

    added_count = 0
    for name in final_participants:
        try:
            # We are inserting them as 'Pending' so the factory processes them
            cursor.execute("INSERT INTO participants (full_name, status) VALUES (?, 'Pending')", (name,))
            added_count += 1
        except Exception as e:
            print(f"  ⚠️ Could not add {name}: {e}")

    conn.commit()
    print(f"✅ Successfully loaded {added_count} Title-Cased names into the queue!")
    conn.close()

if __name__ == '__main__':
    main()