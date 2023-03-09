from Markdown2docx import Markdown2docx


def to_docx():
    project = Markdown2docx('Manual')
    project.eat_soup()
    project.save()    


if __name__ == '__main__':
    to_docx()
