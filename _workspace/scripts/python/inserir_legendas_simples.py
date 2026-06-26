"""
inserir_legendas_simples.py
Insere "Foto 1", "Foto 2", ... abaixo de cada imagem em relatórios .docx preventivos.

Regras de escopo:
  - Inicia a contar a partir da primeira imagem APÓS o parágrafo "Dados da Dependência"
  - Para de contar ao encontrar o parágrafo "Resumo Geral:"
  - Imagens fora dessa faixa (capa, cabeçalho, assinaturas) são ignoradas

Uso:
    python inserir_legendas_simples.py <input.docx> [output.docx]
    Se output não for informado, gera <input>_LEGENDADO.docx no mesmo diretório.
"""

import sys
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'

MARCA_INICIO = re.compile(r'dados da depend', re.IGNORECASE)
MARCA_FIM    = re.compile(r'^\s*resumo geral', re.IGNORECASE)


def has_blip(elem):
    return bool(elem.findall('.//' + qn('a:blip'), {'a': A_NS}))


def get_text(elem):
    return ''.join(t.text or '' for t in elem.findall('.//' + qn('w:t')))


def is_caption(elem):
    return bool(re.match(r'^\s*Foto\s*\d', get_text(elem), re.IGNORECASE))


def make_caption_para(foto_num):
    """Cria parágrafo 'Foto N' centralizado, sem negrito."""
    p = OxmlElement('w:p')

    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    p.append(pPr)

    r = OxmlElement('w:r')
    t = OxmlElement('w:t')
    t.text = f'Foto {foto_num}'
    r.append(t)
    p.append(r)

    return p


def encontrar_faixa(children):
    """
    Retorna (idx_inicio, idx_fim) — índices do body onde contar imagens.
    idx_inicio: índice logo após o parágrafo 'Dados da Dependência'
    idx_fim: índice do parágrafo 'Resumo Geral:' (exclusive)
    """
    idx_inicio = None
    idx_fim = len(children)

    for i, child in enumerate(children):
        txt = get_text(child).strip()
        if idx_inicio is None and MARCA_INICIO.search(txt):
            idx_inicio = i + 1  # começa no elemento seguinte
        if MARCA_FIM.match(txt):
            idx_fim = i
            break

    if idx_inicio is None:
        print("AVISO: 'Dados da Dependência' não encontrado — processando documento inteiro.")
        idx_inicio = 0

    return idx_inicio, idx_fim


def coletar_operacoes(body):
    """
    Retorna lista de elementos (âncoras) que precisam de legenda inserida logo após,
    respeitando a faixa definida por Dados da Dependência → Resumo Geral.
    """
    ops = []
    children = list(body)
    idx_inicio, idx_fim = encontrar_faixa(children)

    print(f"Faixa de processamento: elementos [{idx_inicio}] a [{idx_fim - 1}]")

    for i in range(idx_inicio, idx_fim):
        child = children[i]
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p' and has_blip(child):
            nxt = children[i + 1] if i + 1 < len(children) else None
            if nxt is None or not is_caption(nxt):
                ops.append(child)

        elif tag == 'tbl' and has_blip(child):
            for row in child.findall(qn('w:tr')):
                for cell in row.findall(qn('w:tc')):
                    paras = cell.findall(qn('w:p'))
                    for pi, para in enumerate(paras):
                        if has_blip(para):
                            nxt = paras[pi + 1] if pi + 1 < len(paras) else None
                            if nxt is None or not is_caption(nxt):
                                ops.append(para)

    return ops


def inserir_legendas(input_path, output_path):
    print(f"Carregando: {input_path}")
    doc = Document(input_path)
    body = doc.element.body

    ops = coletar_operacoes(body)
    total = len(ops)
    print(f"Imagens sem legenda encontradas: {total}")

    if total == 0:
        print("Nenhuma legenda a inserir. Documento já está completo.")
        doc.save(output_path)
        return

    # Inserir de trás para frente para não deslocar posições
    for idx, anchor in enumerate(reversed(ops)):
        foto_num = total - idx
        anchor.addnext(make_caption_para(foto_num))

    doc.save(output_path)
    print(f"Legendas inseridas: {total} (Foto 1 a Foto {total})")
    print(f"Salvo em: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python inserir_legendas_simples.py <input.docx> [output.docx]")
        sys.exit(1)

    input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        p = Path(input_path)
        output_path = str(p.parent / (p.stem + '_LEGENDADO' + p.suffix))

    inserir_legendas(input_path, output_path)
