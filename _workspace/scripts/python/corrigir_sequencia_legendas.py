"""
corrigir_sequencia_legendas.py
Encontra todos os parágrafos "Foto N" entre "Dados da Dependência" e "Resumo Geral:"
e renumera em sequência correta. Identifica e reporta onde a sequência estava quebrada.

Uso:
    python corrigir_sequencia_legendas.py <input.docx> [output.docx]
    Se output não for informado, gera <input>_CORRIGIDO.docx no mesmo diretório.
"""

import sys
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

CAPTION_RE   = re.compile(r'^\s*Foto\s*(\d+)\s*$', re.IGNORECASE)
MARCA_INICIO = re.compile(r'dados da depend', re.IGNORECASE)
MARCA_FIM    = re.compile(r'^\s*resumo geral', re.IGNORECASE)


def get_text(elem):
    return ''.join(t.text or '' for t in elem.findall('.//' + qn('w:t')))


def set_text(elem, new_text):
    """Substitui o texto no primeiro w:t e limpa os demais."""
    t_elems = elem.findall('.//' + qn('w:t'))
    if not t_elems:
        return
    t_elems[0].text = new_text
    for t in t_elems[1:]:
        t.text = ''


def encontrar_faixa(children):
    idx_inicio = None
    idx_fim = len(children)
    for i, child in enumerate(children):
        txt = get_text(child).strip()
        if idx_inicio is None and MARCA_INICIO.search(txt):
            idx_inicio = i + 1
        if MARCA_FIM.match(txt):
            idx_fim = i
            break
    if idx_inicio is None:
        print("AVISO: 'Dados da Dependência' não encontrado — processando documento inteiro.")
        idx_inicio = 0
    return idx_inicio, idx_fim


def coletar_legendas(body):
    """
    Percorre parágrafos e tabelas dentro da faixa definida.
    Retorna lista de tuplas: (elem_paragrafo, numero_atual)
    """
    legendas = []
    children = list(body)
    idx_inicio, idx_fim = encontrar_faixa(children)

    print(f"Faixa de processamento: elementos [{idx_inicio}] a [{idx_fim - 1}]")

    def verificar_para(p):
        txt = get_text(p).strip()
        m = CAPTION_RE.match(txt)
        if m:
            legendas.append((p, int(m.group(1))))

    for i in range(idx_inicio, idx_fim):
        child = children[i]
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p':
            verificar_para(child)
        elif tag == 'tbl':
            for row in child.findall(qn('w:tr')):
                for cell in row.findall(qn('w:tc')):
                    for para in cell.findall(qn('w:p')):
                        verificar_para(para)

    return legendas


def corrigir_sequencia(input_path, output_path):
    print(f"Carregando: {input_path}")
    doc = Document(input_path)
    body = doc.element.body

    legendas = coletar_legendas(body)
    total = len(legendas)
    print(f"Legendas encontradas: {total}")

    if total == 0:
        print("Nenhuma legenda 'Foto N' encontrada no intervalo.")
        sys.exit(0)

    # Detectar quebras na sequência original
    numeros_originais = [n for _, n in legendas]
    quebras = []
    for i in range(1, len(numeros_originais)):
        esperado = numeros_originais[i - 1] + 1
        atual = numeros_originais[i]
        if atual != esperado:
            quebras.append((i, numeros_originais[i - 1], atual))

    if quebras:
        print(f"\n  Quebras de sequencia detectadas ({len(quebras)}):")
        for pos, anterior, atual in quebras:
            print(f"   Posicao {pos + 1}: apos Foto {anterior} veio Foto {atual} (esperado Foto {anterior + 1})")
    else:
        print("Sequencia ja esta correta — apenas verificando e salvando.")

    # Renumerar em sequência correta (1, 2, 3, ...)
    alteracoes = 0
    for idx, (elem, num_original) in enumerate(legendas):
        num_correto = idx + 1
        if num_original != num_correto:
            set_text(elem, f'Foto {num_correto}')
            alteracoes += 1

    print(f"\nLegendas renumeradas: {alteracoes} alteracoes")
    print(f"Sequencia final: Foto 1 a Foto {total}")

    doc.save(output_path)
    print(f"Salvo em: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python corrigir_sequencia_legendas.py <input.docx> [output.docx]")
        sys.exit(1)

    input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        p = Path(input_path)
        output_path = str(p.parent / (p.stem + '_CORRIGIDO' + p.suffix))

    corrigir_sequencia(input_path, output_path)
