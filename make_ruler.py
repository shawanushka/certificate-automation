from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

print("Generating ruler overlay...")

# 1. Create a temporary "Ruler" PDF
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=A4)

# --- DRAW THE GRID ---
c.setFont("Helvetica", 10)
c.setStrokeColorRGB(1, 0, 0) # Red lines

# Draw Vertical Lines (X axis) every 50 points
for x in range(0, 600, 50):
    c.line(x, 0, x, 850)
    c.drawString(x + 2, 10, str(x)) # Label at bottom
    c.drawString(x + 2, 400, str(x)) # Label in middle
    c.drawString(x + 2, 800, str(x)) # Label at top

# Draw Horizontal Lines (Y axis) every 50 points
for y in range(0, 900, 50):
    c.line(0, y, 600, y)
    c.drawString(5, y + 2, str(y)) # Label at left
    c.drawString(300, y + 2, str(y)) # Label in middle
    c.drawString(550, y + 2, str(y)) # Label at right

c.save()
packet.seek(0)
ruler_pdf = PdfReader(packet)

# 2. Merge it with your Template
template_pdf = PdfReader(open("template.pdf", "rb"))
output = PdfWriter()
page = template_pdf.pages[0]
page.merge_page(ruler_pdf.pages[0])
output.add_page(page)

# 3. Save
with open("measure_me.pdf", "wb") as f:
    output.write(f)

print("Done! Open 'measure_me.pdf' and read the numbers.")