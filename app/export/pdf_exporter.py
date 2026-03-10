import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
from app.domain.study_material import StudyMaterial

class PDFExporter:

    @staticmethod
    def export(material: StudyMaterial, filename: str):
        export_folder = "study_export"
        os.makedirs(export_folder, exist_ok=True)
        full_path = os.path.join(export_folder, filename)

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        left_margin = 50
        right_margin = 50
        max_width = width - left_margin - right_margin

        y = height - 50

        def draw_wrapped_text(text, font_name="Helvetica", font_size=10, indent=0, line_spacing=12):
            nonlocal y
            c.setFont(font_name, font_size)
            wrapped_lines = wrap(text, width=95)  # Adjust width according to font size
            for line in wrapped_lines:
                c.drawString(left_margin + indent, y, line)
                y -= line_spacing
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont(font_name, font_size)

        # Title
        draw_wrapped_text(f"Study Material: {material.topic}", "Helvetica-Bold", 16, 0, 20)
        y -= 10

        # Summary
        draw_wrapped_text("Summary:", "Helvetica-Bold", 12, 0, 15)
        draw_wrapped_text(material.summary, "Helvetica", 10, 10, 12)
        y -= 10

        # Key Points
        draw_wrapped_text("Key Points:", "Helvetica-Bold", 12, 0, 15)
        for kp in material.key_points:
            draw_wrapped_text(f"- {kp}", "Helvetica", 10, 10, 12)
        y -= 10

        # Questions & Answers
        draw_wrapped_text("Questions & Answers:", "Helvetica-Bold", 12, 0, 15)
        for q, a in zip(material.questions, material.answers):
            draw_wrapped_text(f"Q: {q}", "Helvetica", 10, 10, 12)
            draw_wrapped_text(f"A: {a}", "Helvetica", 10, 20, 12)
            y -= 5

        c.save()