

import os
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def save_documents_to_pdf(documents, output_file="data/processed/debug_export.pdf"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    pdf = SimpleDocTemplate(output_file, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        title = doc.metadata.get("title", "")

        content.append(Paragraph(escape(f"{title} — {source}"), styles["Heading3"]))
        content.append(Spacer(1, 6))

      
        body = escape(doc.page_content[:3000])
        content.append(Paragraph(body, styles["BodyText"]))
        content.append(Spacer(1, 18))

    pdf.build(content)
    print(f"Saved debug export: {output_file}")


if __name__ == "__main__":
    import json

    from config import ALL_DOCS_JSON
    from langchain_core.documents import Document

    with open(ALL_DOCS_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)

    docs = [Document(page_content=d["content"], metadata=d["metadata"]) for d in raw]
    save_documents_to_pdf(docs)
