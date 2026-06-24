from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def save_documents_to_pdf(documents, output_file):

    pdf = SimpleDocTemplate(output_file)

    styles = getSampleStyleSheet()

    content = []

    for doc in documents:

        source = doc.metadata["source"]

        content.append(
            Paragraph(
                f"<b>{source}</b>",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                doc.page_content[:5000],
                styles["BodyText"]
            )
        )

    pdf.build(content)