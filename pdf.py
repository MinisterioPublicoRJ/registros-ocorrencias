import io

from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LAParams


def get_filename_and_fobj(filename_or_fobj):
    if isinstance(filename_or_fobj, str):
        fobj = open(filename_or_fobj, 'rb')
        filename = filename_or_fobj
    else:
        fobj = filename_or_fobj
        filename = getattr(fobj, 'name', None)

    return filename, fobj


def le_pdf(filename_or_fobj):
    filename, fobj = get_filename_and_fobj(filename_or_fobj)
    parser = PDFParser(fobj)
    doc = PDFDocument(parser)
    texto = ''
    for num_pagina, pagina in enumerate(PDFPage.create_pages(doc), start=1):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        resultado = io.StringIO()
        conversor = TextConverter(rsrcmgr, resultado, laparams=laparams)
        interpretador = PDFPageInterpreter(rsrcmgr, conversor)
        interpretador.process_page(pagina)
        texto += resultado.getvalue()

    return texto.strip()
