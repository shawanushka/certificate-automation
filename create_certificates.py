import sqlite3
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape  # <-- Added Landscape!
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os

# ============================================================
# 👇👇👇 YOUR CONTROL PANEL 👇👇👇
# ============================================================
OUTPUT_FOLDER = 'GenAI_Certificates'
DB_FILE = 'participants.db'
TEMPLATE_FILE = 'template.pdf'

# --- 1. POSITION ---
NAME_X = 421  # Dead center of a landscape A4 page
NAME_Y = 260  # <-- Moved DOWN so it doesn't overlap!

# --- 2. FONT SETTINGS ---
try:
    pdfmetrics.registerFont(TTFont('Pinyon', 'PinyonScript-Regular.ttf'))
except Exception as e:
    print("❌ ERROR: Could not find 'PinyonScript-Regular.ttf' in the folder!")
    exit()

FONT_NAME = "Pinyon"    
START_FONT_SIZE = 74            
MINIMUM_FONT_SIZE = 40          
MAX_WIDTH_ALLOWED = 600       # <-- Gave it much more breathing room!  

# --- 3. COLOR SETTINGS ---
COLOR_R = 0.08
COLOR_G = 0.28
COLOR_B = 0.16
# ============================================================

def create_certificate(name):
    print(f"  🎨 Drawing certificate for: {name}")
    name_to_print = name.strip().title()
    packet = io.BytesIO()
    
    # FIX: We are now using a Landscape canvas so long names don't get cut off!
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
    
    return output_pdf_writer

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT full_name FROM participants WHERE status IS NULL OR status != 'Done'")
    people = cursor.fetchall()
    
    if not people:
        print("✅ No new participants. Add more using 'add_names.py'")
        conn.close()
        return
    
    for (name,) in people:
        try:
            output_pdf_writer = create_certificate(name)
            pdf_filename = f"Certificate_{name.replace(' ', '_')}.pdf"
            save_path = os.path.join(OUTPUT_FOLDER, pdf_filename)
            
            with open(save_path, "wb") as f:
                output_pdf_writer.write(f)
            
            update_cursor = conn.cursor()
            update_cursor.execute("UPDATE participants SET status = 'Done' WHERE full_name = ?", (name,))
            conn.commit()
            
        except Exception as e:
            print(f"  ❌ Error for {name}: {e}")

    conn.close()
    print("\n🎉 JOB COMPLETE! Check the 'GenAI_Certificates' folder on your computer.")

if __name__ == '__main__':
    main()