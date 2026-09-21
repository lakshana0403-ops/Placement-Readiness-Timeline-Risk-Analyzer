import io
import csv
from fpdf import FPDF

def create_csv_report(resume_text, job_desc, matched, missing, score, ats_score, ai_feedback):
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["Placement Readiness Report"])
    writer.writerow(["Overall Score", f"{score}%"])
    writer.writerow(["ATS Match", f"{ats_score}%"])
    writer.writerow([])
    
    writer.writerow(["Matched Skills", ", ".join(matched)])
    writer.writerow(["Missing Skills", ", ".join(missing)])
    writer.writerow([])
    
    writer.writerow(["Learning Timeline"])
    writer.writerow(["Phase", "Skills to Focus On"])
    
    # Needs to match analysis.py format
    from placement.analysis import learning_timeline
    timeline = learning_timeline(missing)
    for phase, skills_list in timeline.items():
        # clean the skills list for CSV
        clean_skills = skills_list.replace('✅ ', '').replace('\n', ' | ').replace('**', '')
        writer.writerow([phase, clean_skills])
        
    writer.writerow([])
    writer.writerow(["AI Feedback"])
    writer.writerow([ai_feedback])
    
    return output.getvalue().encode('utf-8')


def create_pdf_report(resume_text, job_desc, matched, missing, score, ats_score, ai_feedback):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Placement Readiness Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Overall Score: {score}%", ln=True)
    pdf.cell(200, 10, txt=f"ATS Match: {ats_score}%", ln=True)
    pdf.cell(200, 10, txt="", ln=True)

    pdf.cell(200, 10, txt="Matched Skills:", ln=True)
    pdf.multi_cell(0, 10, txt=", ".join(matched))
    pdf.cell(200, 10, txt="Missing Skills:", ln=True)
    pdf.multi_cell(0, 10, txt=", ".join(missing))
    pdf.cell(200, 10, txt="", ln=True)

    pdf.cell(200, 10, txt="Learning Timeline:", ln=True)
    from placement.analysis import learning_timeline
    timeline = learning_timeline(missing)
    for phase, skills_list in timeline.items():
        # Remove emojis for FPDF which only supports latin-1
        clean_skills = skills_list.replace('✅ ', '').replace('\n', ' | ').replace('**', '')
        clean_phase = phase.replace('⏳', 'Time:')
        # Handle long lines in PDF
        pdf.multi_cell(0, 8, txt=f"{clean_phase}: {clean_skills}")

    pdf.cell(200, 10, txt="", ln=True)
    pdf.cell(200, 10, txt="AI Feedback:", ln=True)
    # Filter encoding issues
    clean_ai = ai_feedback.encode('latin-1', 'replace').decode('latin-1') if ai_feedback else "No feedback generated."
    pdf.multi_cell(0, 10, txt=clean_ai)

    return pdf.output(dest="S").encode('latin1')
