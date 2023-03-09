from docx2pdf import convert
from to_docx import to_docx


if __name__ == '__main__':
    to_docx()
    convert("./Manual.docx")
