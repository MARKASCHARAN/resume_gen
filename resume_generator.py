from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

def generate_pdf(data):
    file_name = f"{data['name'].strip().replace(' ', '_')}.pdf"
    layout = SimpleDocTemplate(file_name, pagesize=LETTER, topMargin=30, bottomMargin=30, leftMargin=40, rightMargin=40)

    styles = getSampleStyleSheet()
    content = []

    heading = ParagraphStyle('main_heading', fontSize=18, alignment=1, spaceAfter=10, leading=22, fontName="Helvetica-Bold")
    subtext = ParagraphStyle('contact', fontSize=9, alignment=1, spaceAfter=12, textColor=colors.HexColor("#555555"))
    title = ParagraphStyle('section_title', fontSize=12, leading=14, spaceAfter=6, spaceBefore=12, fontName="Helvetica-Bold", underlineWidth=1.0, underlineOffset=-2)
    point = ParagraphStyle('point', bulletIndent=10, leftIndent=20, spaceAfter=4, fontSize=10)
    summary = ParagraphStyle('summary', parent=styles['Normal'], alignment=1, fontSize=11, leading=14, spaceAfter=6)
    regular = styles['Normal']

    def draw_line(target, before=6, after=6):
        target.append(Spacer(1, before))
        target.append(HRFlowable(width="100%", thickness=0.8, color=colors.grey))
        target.append(Spacer(1, after))

    content.append(Paragraph(f"<b>{data['name']}</b>", heading))
    contact = f"{data['email']} | {data['phone']} | {data['city']} | {data['github']} | {data['linkedin']}"
    content.append(Paragraph(contact, subtext))
    draw_line(content)
   

    content.append(Paragraph("Professional Summary", title))
    content.append(Paragraph(data['objective'], summary))
    draw_line(content)

    content.append(Paragraph("Technical Skills", title))
    skill_rows = []
    for category, items in data['skills'].items():
        if items:
            label = category.replace('_', ' ').title().replace("And", "&")
            skill_rows.append([Paragraph(f"<b>{label}:</b>", regular), ", ".join(items)])
    if skill_rows:
        skill_table = Table(skill_rows, hAlign='LEFT', colWidths=[160, 350])
        skill_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        content.append(skill_table)
        draw_line(content)

    if data.get('experience'):
        content.append(Paragraph("Professional Experience", title))
        for job in data['experience']:
            content.append(Paragraph(f"<b>{job['company']}</b> – {job['role']}", regular))
            content.append(Paragraph(f"<i>{job['duration']}</i>", regular))
            for task in job.get('responsibilities', []):
                content.append(Paragraph(f"• {task}", point))
            if job.get('technologies'):
                content.append(Paragraph(f"<b>Key Technologies:</b> {job['technologies']}", regular))
            content.append(Spacer(1, 6))
        draw_line(content)

    if data.get("projects"):
        content.append(Paragraph("Projects", title))
        for prj in data['projects']:
            content.append(Paragraph(f"<b>{prj['name']}</b>", regular))
            content.append(Paragraph(prj['description'], point))
            content.append(Paragraph(f"<b>Technologies Used:</b> {prj['technologies']}", regular))
            if prj.get("link"):
                content.append(Paragraph(f"<b>Link:</b> <a href='{prj['link']}'>{prj['link']}</a>", regular))
            content.append(Spacer(1, 6))
        draw_line(content)

    if data.get("education"):
        content.append(Paragraph("Education", title))
        for edu in data['education']:
            content.append(Paragraph(f"<b>{edu['degree']}</b> – {edu['institute']}", regular))
            content.append(Paragraph(f"Year: {edu['year']} | Grade: {edu['grade']}", regular))
            content.append(Spacer(1, 6))
        draw_line(content)

    if data.get("achievements"):
        content.append(Paragraph("Achievements", title))
        for ach in data['achievements']:
            content.append(Paragraph(f"• {ach}", point))
        draw_line(content)

    layout.build(content)
    return file_name
