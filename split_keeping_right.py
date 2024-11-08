from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject

# Open the original PDF
input_pdf_path = "full.pdf"  # Path to the original PDF file
output_pdf_path = "out_full.pdf"  # Path where the duplicated PDF will be saved

# Initialize the reader and writer
pdf_reader = PdfReader(input_pdf_path)
pdf_writer = PdfWriter()

# Add each page from the original PDF to the writer
for page_num in range(0, len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    page.add_transformation(Transformation().translate(-page.mediabox.width / 2, 0))
    pdf_writer.add_page(page)

# Save the duplicated PDF to a new file
with open(output_pdf_path, "wb") as output_pdf:
    pdf_writer.write(output_pdf)

print(f"Duplicated PDF saved as {output_pdf_path}")
