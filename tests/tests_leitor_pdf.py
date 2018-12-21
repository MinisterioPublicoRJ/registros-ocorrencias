from unittest import TestCase, main

from pdf import le_pdf


class TestLeitorPdf(TestCase):
    def test_le_conteudo_file_obj(self):
        fobj = open('tests/fixtures/teste.pdf', 'rb')

        conteudo = le_pdf(fobj)
        esperado = 'Documento PDF\nConteúdo qualquer'

        self.assertEqual(conteudo, esperado)


if __name__ == "__main__":
    main()
