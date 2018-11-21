import os
from md2pdf.core import md2pdf


def convertation(md_path): # md_path - путь до папки с md файлами
	pdf_files = []
    pdf_path = os.path.join(os.curdir, './test_works') # папка для pdf
    if not (os.path.exists(pdf_path)):
        os.makedirs(os.path.join(os.curdir, './test_works'))
    md_list = os.listdir(md_path)
    for md_file in md_list:
        md2pdf(os.path.join(pdf_path, md_file[:-3] + '.pdf'), md_file_path=os.path.join(md_path, md_file),
        css_file_path=os.path.join(os.curdir, css_path))
        pdf_files.append(os.path.join(pdf_path, md_file[:-3] + '.pdf'))
    return pdf_files   