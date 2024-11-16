from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-i', '--input', metavar='input_path', type=str, help='Input path of the PDF.', default='input.pdf')
parser.add_argument('-o', '--output', metavar='output_path', type=str, help='Name of the created PDF file.',
                    default='output.pdf')
parser.add_argument('-s', '--side', metavar='side', type=str, help='Which side to save (left/right)', default='left')

args = parser.parse_args()
if args.side not in ['left', 'right']:
    print('Wrong side selected. Valid values: left, right.')
    exit(1)


def extract_from_pdf(input, output, side):
    # Initialize the reader and writer
    pdf_reader = PdfReader(input)
    pdf_writer = PdfWriter()

    # Add each page from the original PDF to the writer
    for page_num in range(0, len(pdf_reader.pages), 2):
        is_pagelength_even = len(pdf_reader.pages) % 2 == 0
        print(f'Progress: {(page_num + 2 if is_pagelength_even else page_num + 1) / len(pdf_reader.pages) * 100:5.2f}%')
        page = pdf_reader.pages[page_num]

        new_page = PageObject.create_blank_page(pdf_writer, page.mediabox.width, page.mediabox.height)

        if side == 'left':
            page.mediabox.upper_right = page.mediabox.width / 2, page.mediabox.height
        else:
            page.add_transformation(Transformation().translate(-page.mediabox.width / 2, 0))

        new_page.merge_page(page)

        if page_num + 1 < len(pdf_reader.pages):
            other_page = pdf_reader.pages[page_num + 1]

            if side == 'left':
                other_page.add_transformation(Transformation().translate(other_page.mediabox.width / 2, 0))
            else:
                other_page.mediabox.upper_left = other_page.mediabox.width / 2, other_page.mediabox.height
                
            new_page.merge_page(other_page)

        pdf_writer.add_page(new_page)

    # Save the duplicated PDF to a new file
    with open(output, "wb") as output_pdf:
        pdf_writer.write(output_pdf)


print('Extraction started!')
extract_from_pdf(args.input, args.output, args.side)
print(f"Extracted PDF saved as {args.output}!")
