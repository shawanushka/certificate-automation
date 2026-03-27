import os
import io
import sqlite3
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ============================================================
# 👇👇👇 YOUR CONTROL PANEL 👇👇👇
# ============================================================
# ⚠️ PASTE YOUR NEW GOOGLE DRIVE FOLDER ID HERE:
GOOGLE_DRIVE_FOLDER_ID = '1miM4z_VbFiPMbWggui48ub2rtKgb3iRF'

DB_FILE = 'participants.db'
TEMPLATE_FILE = 'template.pdf'
TEMP_PDF = 'temp_certificate.pdf' 

# --- 1. POSITION ---
NAME_X = 421  
NAME_Y = 260  

# --- 2. FONT SETTINGS ---
try:
    pdfmetrics.registerFont(TTFont('Pinyon', 'PinyonScript-Regular.ttf'))
except Exception as e:
    print("❌ ERROR: Could not find 'PinyonScript-Regular.ttf' in the folder!")
    exit()

FONT_NAME = "Pinyon"    
START_FONT_SIZE = 74            
MINIMUM_FONT_SIZE = 40          
MAX_WIDTH_ALLOWED = 600         

# --- 3. COLOR SETTINGS ---
COLOR_R = 0.08
COLOR_G = 0.28
COLOR_B = 0.16

# --- GOOGLE DRIVE SETUP ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# ============================================================

def get_drive_service():
    """Authenticates and connects to Google Drive."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                os.remove('token.json')
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def create_certificate(name):
    """Draws the certificate and saves it as a temporary file."""
    print(f"  🎨 Drawing certificate for: {name}")
    name_to_print = name.strip().title()
    packet = io.BytesIO()
    
    c = canvas.Canvas(packet, pagesize=landscape(A4))
    c.setFillColorRGB(COLOR_R, COLOR_G, COLOR_B)
    current_font_size = START_FONT_SIZE
    c.setFont(FONT_NAME, current_font_size)
    
    name_width = c.stringWidth(name_to_print, FONT_NAME, current_font_size)
    while name_width > MAX_WIDTH_ALLOWED and current_font_size > MINIMUM_FONT_SIZE:
        current_font_size -= 2 
        c.setFont(FONT_NAME, current_font_size)
        name_width = c.stringWidth(name_to_print, FONT_NAME, current_font_size)

    c.drawCentredString(NAME_X, NAME_Y, name_to_print) 
    c.save()
    packet.seek(0)
    
    name_sticker = PdfReader(packet)
    template_pdf = PdfReader(open(TEMPLATE_FILE, "rb"))
    output_pdf_writer = PdfWriter()
    
    page = template_pdf.pages[0]
    page.merge_page(name_sticker.pages[0])
    output_pdf_writer.add_page(page)
    
    with open(TEMP_PDF, "wb") as f:
        output_pdf_writer.write(f)

def upload_to_drive(drive_service, name):
    """Uploads the temporary file to Google Drive."""
    file_metadata = {
        'name': f'Certificate_{name.replace(" ", "_")}.pdf',
        'parents': [GOOGLE_DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(TEMP_PDF, mimetype='application/pdf', resumable=True)
    print(f"  ☁️ Uploading to Drive...")
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def main():
    print("🔌 Connecting to Google Drive...")
    try:
        drive_service = get_drive_service()
    except Exception as e:
        print(f"❌ Could not connect to Google Drive: {e}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT full_name FROM participants WHERE status IS NULL OR status != 'Done'")
    people = cursor.fetchall()
    
    if not people:
        print("✅ No new participants. Add more using 'add_names.py'")
        conn.close()
        return
    
    print(f"✅ Found {len(people)} participants to process.\n")

    for (name,) in people:
        try:
            create_certificate(name)
            upload_to_drive(drive_service, name)
            
            update_cursor = conn.cursor()
            update_cursor.execute("UPDATE participants SET status = 'Done' WHERE full_name = ?", (name,))
            conn.commit()
            print(f"  ✨ Success!\n")
            
        except Exception as e:
            print(f"  ❌ Error for {name}: {e}")

    if os.path.exists(TEMP_PDF):
        os.remove(TEMP_PDF)

    conn.close()
    print("🎉 JOB COMPLETE! All certificates are safely in your Google Drive.")

if __name__ == '__main__':
    main()