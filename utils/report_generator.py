from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import gray, lightblue, blue
from datetime import date
from io import BytesIO

# Register Unicode-safe font
pdfmetrics.registerFont(TTFont("DejaVuSans", "assets/DejaVuSans.ttf"))

def generate_service_pdf(name, phone, service_type, summary_text, ticket):
    # Defensive defaults
    name = name or "Customer"
    phone = phone or "N/A"
    service_type = service_type or "Service"

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ✅ Watermark
    c.saveState()
    c.setFont("DejaVuSans", 40)
    c.setFillColor(gray)
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, "JS Financial Services")
    c.restoreState()

    # ✅ Title
    c.setFont("DejaVuSans", 16)
    c.setFillColor(blue)
    c.drawString(50, height - 80, f"{service_type} Report")

    # ✅ Header details
    c.setFont("DejaVuSans", 12)
    c.setFillColor("black")
    c.drawString(50, height - 110, f"Date: {date.today().strftime('%d-%m-%Y')}")
    c.drawString(50, height - 130, f"Customer Name: {name}")
    c.drawString(50, height - 150, f"Ticket ID: {ticket}")
    c.drawString(50, height - 170, f"Phone: {phone}")

    # ✅ Body text (summary)
    text_object = c.beginText(50, height - 200)
    text_object.setFont("DejaVuSans", 12)
    for line in str(summary_text).split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    # ✅ Footer
    c.setFont("DejaVuSans", 10)
    c.setFillColor(gray)
    c.drawString(50, 100, "This is a system-generated report. No signature required.")

    c.save()
    buffer.seek(0)
    return buffer.read()  # ✅ Return bytes for Streamlit download