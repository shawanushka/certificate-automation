import sqlite3
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload 

# ============================================================
# 👇👇👇 YOUR CONTROL PANEL - CHANGE SETTINGS HERE 👇👇👇
# ============================================================
GOOGLE_DRIVE_FOLDER_ID = '1J-bAv2meRSuk8HMeELgn0vbiy16IDTee' 
DB_FILE = 'participants.db'
TEMPLATE_FILE = 'template.pdf'

# --- 1. POSITION (Fixing the Centering) ---
# If there is more space on the RIGHT, increase this number.
# If there is more space on the LEFT, decrease this number.
NAME_X = 390  # I increased this from 385 to help center it
NAME_Y = 240  # Up/Down

# --- 2. FONT SETTINGS ---
# Options: "Helvetica-Bold", "Times-Bold", "Courier-Bold"
FONT_NAME = "Helvetica-Bold"    
START_FONT_SIZE = 30            # Starting size
MINIMUM_FONT_SIZE = 12          # Won't shrink smaller than this
MAX_WIDTH_ALLOWED = 360         # If wider than this, shrink logic starts

# --- 3. COLOR SETTINGS (RGB, 0.0 to 1.0) ---
# Example: Red=1,0,0 | Blue=0,0,1 | Black=0,0,0
COLOR_R = 0.0
COLOR_G = 0.0
COLOR_B = 0.0
# ============================================================


def get_drive_service():
    """Logs into Google and returns the drive service."""
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def create_certificate_in_memory(name):
    """
    Creates a PDF certificate using Title Case and auto-shrink logic.
    """
    print(f"  🎨 Drawing certificate for: {name}")
    
    # --- FIX #5: FORMAL FORMATTING (Title Case) ---
    # .strip() removes spaces at start/end (helps centering)
    # .title() makes "alex smith" -> "Alex Smith"
    name_to_print = name.strip().title()
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    
    # --- FIX #4: COLOR AND FONT ---
    c.setFillColorRGB(COLOR_R, COLOR_G, COLOR_B)
    current_font_size = START_FONT_SIZE
    c.setFont(FONT_NAME, current_font_size)
    
    # --- FIX #1: AUTO-SHRINK LOGIC ---
    # Calculate how wide the name is
    name_width = c.stringWidth(name_to_print, FONT_NAME, current_font_size)
    
    # Loop: While name is too wide AND font is above minimum...
    while name_width > MAX_WIDTH_ALLOWED and current_font_size > MINIMUM_FONT_SIZE:
        current_font_size -= 2 # Shrink by 2 points
        print(f"    ...Name is long. Shrinking font to {current_font_size}pt")
        c.setFont(FONT_NAME, current_font_size)
        name_width = c.stringWidth(name_to_print, FONT_NAME, current_font_size)

    # --- FIX #2: DRAWING AT COORDINATES ---
    c.drawCentredString(NAME_X, NAME_Y, name_to_print) 
    c.save()
    packet.seek(0)
    
    # Merge with Template
    name_sticker = PdfReader(packet)
    template_pdf = PdfReader(open(TEMPLATE_FILE, "rb"))
    
    output_pdf_writer = PdfWriter()
    page = template_pdf.pages[0]
    page.merge_page(name_sticker.pages[0])
    output_pdf_writer.add_page(page)
    
    # Save to Memory
    final_pdf_in_memory = io.BytesIO()
    output_pdf_writer.write(final_pdf_in_memory)
    final_pdf_in_memory.seek(0)
    
    return final_pdf_in_memory

def main():
    print("🔑 Connecting to Google Drive...")
    try:
        drive_service = get_drive_service()
    except FileNotFoundError:
        print("❌ ERROR: Could not find 'credentials.json'!")
        return

    print("🗄️  Reading names from database...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check for 'status' column
    try:
        cursor.execute("SELECT full_name FROM participants WHERE status IS NULL OR status != 'Done'")
        people = cursor.fetchall()
    except sqlite3.OperationalError:
        print("❌ ERROR: Run 'python upgrade_database.py' first to add the status column.")
        return
    
    if not people:
        print("✅ No new participants. Add more using 'add_names.py'")
        conn.close()
        return
    
    print(f"✅ Found {len(people)} new participants.\n")

    for (name,) in people:
        try:
            # Make PDF
            pdf_bytes_io = create_certificate_in_memory(name)
            
            # Upload
            pdf_filename = f"Certificate_{name.replace(' ', '_')}.pdf"
            print(f"  ☁️  Uploading {pdf_filename}...")
            
            file_metadata = {
                'name': pdf_filename,
                'parents': [GOOGLE_DRIVE_FOLDER_ID]
            }
            
            media = MediaIoBaseUpload(pdf_bytes_io, mimetype='application/pdf', resumable=True)
            
            drive_service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()
            
            print(f"  ✨ Success! {name} is done.\n")
            
            # Update Status
            update_cursor = conn.cursor()
            update_cursor.execute("UPDATE participants SET status = 'Done' WHERE full_name = ?", (name,))
            conn.commit()
            
        except Exception as e:
            print(f"  ❌ Error for {name}: {e}")

    conn.close()
    print("🎉 JOB COMPLETE!")

if __name__ == '__main__':
    main()