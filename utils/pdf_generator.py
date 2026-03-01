from reportlab.pdfgen import canvas

def generate_pdf(username, status, score, recommendations, file_path="nutrition_report.pdf"):
    c = canvas.Canvas(file_path)

    c.drawString(100, 800, "Nutrition Health Report")
    c.drawString(100, 770, f"User: {username}")
    c.drawString(100, 750, f"Health Status: {status}")
    c.drawString(100, 730, f"Overall Score: {score}")

    y = 700
    c.drawString(100, y, "Recommendations:")
    y -= 20

    for rec in recommendations:
        c.drawString(120, y, "- " + rec)
        y -= 20

    c.save()

    return file_path