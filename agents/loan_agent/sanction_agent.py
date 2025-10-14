from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import green, lightgreen, gray
from io import BytesIO

# Register Unicode-safe font
pdfmetrics.registerFont(TTFont("DejaVuSans", "assets/DejaVuSans.ttf"))

def generate_loan_sanction_letter(name, amount, tenure, decision_text, score):
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

    # ✅ Header
    c.setFont("DejaVuSans", 14)
    c.drawString(50, height - 50, "Loan Sanction Letter")

    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 100, "Date: 13-10-2025")
    c.drawString(50, height - 130, f"Name: {name}")
    c.drawString(50, height - 160, f"Amount: ₹{amount:,} only")
    c.drawString(50, height - 190, f"Tenure: {tenure} years")
    c.drawString(50, height - 210, f"Credit Score: {score}")

    # ✅ Decision block (multiline)
    text_obj = c.beginText(50, height - 240)
    text_obj.setFont("DejaVuSans", 12)
    text_obj.textLines(f"Decision: {decision_text}")
    c.drawText(text_obj)

    # ✅ Approval Stamp
    c.setStrokeColor(green)
    c.setFillColor(lightgreen)
    c.rect(width - 180, height - 100, 120, 40, fill=1)
    c.setFont("DejaVuSans", 10)
    c.setFillColor(green)
    c.drawString(width - 170, height - 80, "✅ Approved")

    # ✅ Signature Block
    c.setFont("DejaVuSans", 12)
    c.drawString(50, 100, "Authorized Signatory")
    c.line(50, 95, 200, 95)
    c.drawString(50, 80, "JS Financial Services")

    c.save()
    buffer.seek(0)
    return buffer.read()