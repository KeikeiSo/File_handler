
from PyPDF2 import PdfFileReader


# 1
pdf_reader = PdfFileReader(str(pdf_path))
output_file_path = Path.home() / "Pride_and_Prejudice.txt"

# 2
with output_file_path.open(mode="w") as output_file:
    # 3
    title = pdf_reader.documentInfo.title
    num_pages = pdf_reader.getNumPages()
    output_file.write(f"{title}\\nNumber of pages: {num_pages}\\n\\n")

    # 4
    for page in pdf_reader.pages:
        text = page.extractText()
        output_file.write(text)
