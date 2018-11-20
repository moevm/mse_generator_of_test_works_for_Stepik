import os
from md2pdf.core import md2pdf


md_path = "" # путь до папки с md файлами
css_path = "./static/css/work.css" # путь до файла со стилем


def convertation(md_path):
    pdf_path = os.path.join(os.curdir, './test_works') # папка для pdf
    if not (os.path.exists(pdf_path)):
        os.makedirs(os.path.join(os.curdir, './test_works'))
    md_list = os.listdir(md_path)
    for md_file in md_list:
        md2pdf(os.path.join(pdf_path, md_file[:-3] + '.pdf'), md_file_path=os.path.join(md_path, md_file),
        css_file_path=os.path.join(os.curdir, css_path))

convertation(md_path)   