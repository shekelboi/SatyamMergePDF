from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject

# Open the original PDF
input_pdf_path = "Split updated.pdf"  # Path to the original PDF file
output_pdf_path = "output.pdf"  # Path where the duplicated PDF will be saved

# Initialize the reader and writer
pdf_reader = PdfReader(input_pdf_path)
pdf_writer = PdfWriter()

# Add each page from the original PDF to the writer
for page_num in range(0, len(pdf_reader.pages), 2):
    page = pdf_reader.pages[page_num]

    new_page = PageObject.create_blank_page(pdf_writer, page.mediabox.width * 2, page.mediabox.height)
    new_page.merge_page(page)
    new_page.add_transformation(Transformation().translate(-page.mediabox.width, 0))

    if page_num + 1 < len(pdf_reader.pages):
        other_page = pdf_reader.pages[page_num + 1]
        new_page.merge_page(other_page)

    pdf_writer.add_page(new_page)

# Save the duplicated PDF to a new file
with open(output_pdf_path, "wb") as output_pdf:
    pdf_writer.write(output_pdf)

print(f"Duplicated PDF saved as {output_pdf_path}")
