import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .analysis import learning_timeline


def create_csv_report(resume_text, job_desc, matched, missing, score, ats_score, ai_feedback):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Placement Readiness Analyzer Report"])
    writer.writerow([])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Readiness Score", f"{score}%"])
    writer.writerow(["ATS Score", f"{ats_score}%"])
    writer.writerow(["Matched Skills", ", ".join(matched)])
    writer.writerow(["Missing Skills", ", ".join(missing)])
    writer.writerow([])
    writer.writerow(["Personalized Learning Timeline"])
    timeline = learning_timeline(missing)
    for week, (skill, reason) in timeline.items():
        writer.writerow([week, f"{skill} - {reason}"])
    writer.writerow([])
    writer.writerow(["AI Feedback"])
    writer.writerow([ai_feedback or ""])

    return output.getvalue().encode("utf-8")


def create_pdf_report(resume_text, job_desc, matched, missing, score, ats_score, ai_feedback):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 72
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "Placement Readiness Analyzer Report")
    y -= 28

    c.setFont("Helvetica", 12)
    c.drawString(72, y, f"Readiness Score: {score}%   ATS Score: {ats_score}%")
    y -= 18
    c.drawString(72, y, f"Matched Skills: {', '.join(matched)}")
    y -= 16
    c.drawString(72, y, f"Missing Skills: {', '.join(missing)}")
    y -= 22

    c.setFont("Helvetica-Bold", 13)
    c.drawString(72, y, "Personalized Learning Timeline:")
    y -= 16
    c.setFont("Helvetica", 11)
    timeline = learning_timeline(missing)
    for week, (skill, reason) in timeline.items():
        if y < 100:
            c.showPage()
            y = height - 72
            c.setFont("Helvetica", 11)
        c.drawString(84, y, f"{week}: {skill} - {reason}")
        y -= 14

    if ai_feedback:
        if y < 200:
            c.showPage()
            y = height - 72
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, "AI Feedback:")
        y -= 18
        text_obj = c.beginText(84, y)
        text_obj.setFont("Helvetica", 11)
        for line in (ai_feedback or "").splitlines():
            while len(line) > 100:
                text_obj.textLine(line[:100])
                line = line[100:]
            text_obj.textLine(line)
        c.drawText(text_obj)

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
