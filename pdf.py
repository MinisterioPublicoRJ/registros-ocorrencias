import io

from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LAParams


def le_pdf(filename_or_fobj):
    parser = PDFParser(filename_or_fobj)
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
