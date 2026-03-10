import os

from app.domain.study_material import StudyMaterial
from app.export.pdf_exporter import PDFExporter


def test_pdf_export(tmp_path):

    material = StudyMaterial(
        topic="Python",
        summary="Python is a programming language.",
        key_points=["Easy", "Popular", "Versatile"],
        questions=["What is Python?"],
        answers=["A programming language."]
    )

    filename = tmp_path / "test.pdf"

    PDFExporter.export(material, str(filename))

    assert os.path.exists(filename)