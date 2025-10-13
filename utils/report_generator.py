from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
import os

def generate_service_pdf(name, phone, service_type, summary_text, ticket):
    # Defensive defaults — prevents NoneType errors
    name = name or "Customer"
    phone = phone or "N/A"
    service_type = service_type or "Service"

    # Clean filename (replace spaces and illegal chars)
    safe_name = str(name).replace(" ", "_").replace("/", "_")
    file_path = f"{service_type}_Report_{safe_name}.pdf"

    pdfmetrics.registerFont(TTFont("DejaVuSans", "assets/DejaVuSans.ttf"))

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 80, f"{service_type} Report")

    # Header details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 110, f"Date: {date.today().strftime('%d-%m-%Y')}")
    c.drawString(50, height - 130, f"Customer Name: {name}")
    c.drawString(50, height - 150, f"Ticket ID: {ticket}")
    c.drawString(50, height - 170, f"Phone: {phone}")

    # Body text (summary)
    text_object = c.beginText(50, height - 180)
    text_object.setFont("Helvetica", 12)
    for line in str(summary_text).split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 100, "This is a system-generated report. No signature required.")
    c.showPage()
    c.save()

    return file_path
