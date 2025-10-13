from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Unicode-safe font
pdfmetrics.registerFont(TTFont("DejaVuSans", "assets/DejaVuSans.ttf"))

def generate_loan_sanction_letter(name, amount, tenure, decision_text, score):
    safe_name = str(name).replace(" ", "_").replace("/", "_")
    filename = f"sanction_letter_{safe_name}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("DejaVuSans", 14)
    c.drawString(50, height - 50, "Loan Sanction Letter")
    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 100, f"Date: 13-10-2025")
    c.drawString(50, height - 130, f"Name: {name}")
    c.drawString(50, height - 160, f"Amount: ₹{amount:,} only")
    c.drawString(50, height - 190, f"Tenure: {tenure} years")
    c.drawString(50, height - 210, f"Credit Score: {score}")

    # Multiline decision block
    text_obj = c.beginText(50, height - 230)
    text_obj.setFont("DejaVuSans", 12)
    text_obj.textLines(f"Decision: {decision_text}")
    c.drawText(text_obj)

    c.save()
    return filename