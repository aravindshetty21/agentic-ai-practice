import pymupdf
import re

# doc = pymupdf.open("resume.pdf") # open a document
# out = open("output.txt", "wb") # create a text output
# for page in doc: # iterate the document pages
#     text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
#     out.write(text) # write text of page
#     out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
# out.close()

def extract_text(path):
    """Extract text from PDF file"""
    doc = pymupdf.open(path)
    out = ""
    for page in doc:
        text = page.get_text()
        out += text
    return out

def clean_text(text):
    """Clean text from PDF file"""
    text = text.replace('\r', '\n')

    # Remove bullet symbols
    text = re.sub(r'[•▪●◦■◆★▶►]', '', text)

    # Replace multiple newlines with max two
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove extra spaces per line
    text = "\n".join(line.strip() for line in text.splitlines())

    return text.strip()