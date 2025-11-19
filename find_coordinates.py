# find_coordinates.py
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# === CHANGE THESE NUMBERS UNTIL IT LOOKS GOOD ===
# x = Left/Right (0 is left, 600 is far right)
# y = Up/Down    (0 is bottom, 800 is top)
my_x = 385
my_y = 240
# ================================================

print(f"Testing position: X={my_x}, Y={my_y}")

# 1. Create the "Sticker" with the name
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=A4)
c.setFont("Helvetica-Bold", 30) # You can change the size (30) here too
c.drawCentredString(my_x, my_y, "Alex Smith") # drawCentredString helps it stay in the middle!
c.save()
packet.seek(0)

# 2. Load your blank certificate
template = PdfReader(open("template.pdf", "rb"))
sticker_pdf = PdfReader(packet)

# 3. Stick them together
output = PdfWriter()
page = template.pages[0]
page.merge_page(sticker_pdf.pages[0])
output.add_page(page)

# 4. Save the result
with open("test_result.pdf", "wb") as f:
    output.write(f)

print("Done! Open 'test_result.pdf' to see if the name is in the right spot.")