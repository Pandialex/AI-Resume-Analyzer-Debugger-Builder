# from io import BytesIO
# # from xhtml2pdf import pisa
# from docx import Document

# # ==============================
# # Generate PDF
# # ==============================
# def generate_pdf(html_content):
#     """Converts HTML to PDF bytes."""
#     pdf_buffer = BytesIO()
#     pisa.CreatePDF(html_content, dest=pdf_buffer)
#     pdf_buffer.seek(0)
#     return pdf_buffer.getvalue()


# # ==============================
# # Generate DOCX
# # ==============================
# def generate_docx(data):
#     """Creates DOCX resume using provided data."""
#     doc = Document()
#     doc.add_heading(data.get("full_name", "Your Name"), level=1)
#     doc.add_paragraph(data.get("job_title", ""))
#     doc.add_paragraph(f"Email: {data.get('email', '')} | Phone: {data.get('phone', '')}")
#     doc.add_paragraph(data.get("address", ""))

#     doc.add_heading("Profile Summary", level=2)
#     doc.add_paragraph(data.get("summary", ""))

#     doc.add_heading("Education", level=2)
#     doc.add_paragraph(data.get("education", ""))

#     if data.get("experience"):
#         doc.add_heading("Experience", level=2)
#         doc.add_paragraph(data.get("experience", ""))

#     if data.get("projects"):
#         doc.add_heading("Projects", level=2)
#         doc.add_paragraph(data.get("projects", ""))

#     if data.get("certifications"):
#         doc.add_heading("Certifications", level=2)
#         doc.add_paragraph(data.get("certifications", ""))

#     doc.add_heading("Skills", level=2)
#     doc.add_paragraph(data.get("skills", ""))

#     buffer = BytesIO()
#     doc.save(buffer)
#     buffer.seek(0)
#     return buffer
