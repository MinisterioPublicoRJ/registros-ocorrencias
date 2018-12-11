import re

from collections import namedtuple


def prepara_documento(doc):
    return re.sub(r'\s+', ' ', doc)


def extrai_blocos_envolvidos(doc):
    doc = prepara_documento(doc)
    resultado = re.finditer(
        r'((Testemunha|Autor|Lesado|V[ií]tima|Representante|Adolescente)\s+-|'
        '(Bem\(ns\)\s+'
        'Envolvido\(s\)|Din[aâ]mica do Fato))',
        doc,
        re.IGNORECASE
    )
    posicoes = [r.span()[0] for r in resultado]
    blocos = zip(posicoes[::1], posicoes[1::1])

    return [doc[slice(*bloco)] for bloco in blocos]


def extrai_nome_bloco(bloco):
    tipo = ''
    nome = ''

    nome_encontrado = re.search(r'(Nome:)\s?(.*?-)', bloco)
    if nome_encontrado is not None:
        nome = nome_encontrado.group(2).replace('-', '').strip()

    tipo_encontrado = re.match(r'.*?-', bloco)
    if tipo_encontrado is not None and nome:
        tipo = tipo_encontrado.group(0).replace('-', '').strip().lower()

    return {'nome': nome, 'tipo': tipo}


def extrai_documento_bloco(bloco):
    tipo_obj = namedtuple('Tipo', ['tipo', 'regex'])
    docs = [
        tipo_obj('identidade', '(Identidade Nº\s+)(\d+-?\d+)'),
        tipo_obj('cpf_cic', '(CPF/CIC Nº\s+)(\d{3}\.\d{3}\.\d{3}-\d{2})'),
        tipo_obj('carteira_funcional', '(Carteira funcional Nº\s+)([\d+.]+)')
    ]
    documentos = []
    for doc in docs:
        encontrado = re.search(doc.regex, bloco)
        if encontrado is not None:
            documentos.append({
                'documento': encontrado.group(2),
                'tipo': doc.tipo
            })

    return {'documentos': documentos}


def extrai_filiacao_bloco(bloco):
    filiacao = ''
    encontrado = re.search(
        '(Filho de:\s?)(.*?)\s+(?=Data)',
        bloco,
        re.IGNORECASE
    )
    if encontrado is not None:
        filiacao = encontrado.group(2)

    return {'filiacao': filiacao}


def extrai_dnascimento_bloco(bloco):
    data_nasc = ''
    encontrado = re.search(
        '(Data de nascimento:\s+)(\d{2}/\d{2}/\d{4})',
        bloco
    )

    if encontrado is not None:
        data_nasc = encontrado.group(2)

    return {'data_nascimento': data_nasc}


def extrai_naturalidade_bloco(bloco):
    naturalidade = ''
    encontrado = re.search(
        '(Naturalidade:\s+)(.*?)\s+(Nacionalidade:)',
        bloco
    )
    if encontrado is not None:
        naturalidade = encontrado.group(2)

    return {'naturalidade': naturalidade}


def extrai_informacoes_bloco(bloco):
    funcs = [
        extrai_nome_bloco,
        extrai_documento_bloco,
        extrai_filiacao_bloco,
        extrai_dnascimento_bloco,
        extrai_naturalidade_bloco
    ]

    info = {}
    for fun in funcs:
        info.update(fun(bloco))

    return info if info['nome'] else None


def extrai_artigos(doc):
    encontrado = re.finditer(
        r'(art|art\.|artigos?)\s+(\d+).*?((do )?(inciso\d+|CPBO|C[oó]digo'
        ' Penal|CP|CTBO|CT|C\.P|DL|C[óo]digo de processo Penal|Lei\s+[\d./]'
        '+))',
        doc,
        re.IGNORECASE
    )
    return {'artigos': [artigo.group(0) for artigo in encontrado]}


# TODO: transforma essas funções de extracoes em uma função genérica
def extrai_local(doc):
    local = ''
    encontrado = re.search(r'(Local:\s+)(.*?)(Bairro:)', doc, re.IGNORECASE)

    if encontrado is not None:
        local = encontrado.group(2).strip()

    return {'local': local}


def extrai_bairro(doc):
    bairro = ''
    encontrado = re.search(
        r'(Bairro:\s+)(.*?)(Munic[ií]pio)',
        doc,
        re.IGNORECASE
    )

    if encontrado is not None:
        bairro = encontrado.group(2).strip()

    return {'bairro': bairro}


def extrai_municipio(doc):
    municipio = ''
    encontrado = re.search(
        r'(Munic[ií]pio:\s+)(.*?\s?-\s?RJ)',
        doc,
        re.IGNORECASE
    )
    if encontrado is not None:
        municipio = encontrado.group(2).strip()

    return {'municipio': municipio}


def extrai_data_hora(doc):
    data_hora = ''
    encontrado = re.search(
        r'(Data e Hora do fato:\s?)(\d{2}/\d{2}/\d{4}\s?\d{2}:\d{2}\s?[ae]?\s?'
        '\d{2}/\d{2}/\d{4}\s?\d{2}:\d{2})',
        doc,
        re.IGNORECASE
    )

    if encontrado is not None:
        data_hora = encontrado.group(2)

    return {'data_hora': data_hora}


def extrai_atributos_ocorrencias(doc):
    info = {}
    info.update(extrai_artigos(doc))
    info.update(extrai_local(doc))
    info.update(extrai_bairro(doc))
    info.update(extrai_municipio(doc))
    info.update(extrai_data_hora(doc))

    return info
