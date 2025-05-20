# extractor.py
import re

def extrair_dados_peticao(texto):
    dados = {}

    dados['processo'] = re.search(r'Processo nº:\s*(.+)', texto)
    dados['processo'] = dados['processo'].group(1).strip() if dados['processo'] else None

    dados['nome'] = re.search(r'Nome:\s*(.+)', texto)
    dados['nome'] = dados['nome'].group(1).strip() if dados['nome'] else None

    dados['idade'] = re.search(r'Idade:\s*(\d+)', texto)
    dados['idade'] = int(dados['idade'].group(1)) if dados['idade'] else None

    dados['genero'] = re.search(r'Gênero:\s*(.+)', texto)
    dados['genero'] = dados['genero'].group(1).strip() if dados['genero'] else None

    dados['escolaridade'] = re.search(r'Escolaridade:\s*(.+)', texto)
    dados['escolaridade'] = dados['escolaridade'].group(1).strip() if dados['escolaridade'] else None

    dados['bairro'] = re.search(r'Bairro:\s*(.+)', texto)
    dados['bairro'] = dados['bairro'].group(1).strip() if dados['bairro'] else None

    dados['nacionalidade'] = re.search(r'Nacionalidade:\s*(.+)', texto)
    dados['nacionalidade'] = dados['nacionalidade'].group(1).strip() if dados['nacionalidade'] else None

    dados['fato_ocorrido'] = re.search(r'Fato ocorrido em:\s*([\d/]+)', texto)
    dados['fato_ocorrido'] = dados['fato_ocorrido'].group(1).strip() if dados['fato_ocorrido'] else None

    infracao = re.search(r'ato infracional análogo ao crime de (.+?),', texto)
    dados['tipo_infracao'] = infracao.group(1).strip() if infracao else None

    decisao = re.search(r'A decisão atual é (.+?),', texto)
    dados['decisao'] = decisao.group(1).strip() if decisao else None

    medida = re.search(r'Foi aplicada a medida socioeducativa de (.+?),', texto)
    dados['medida_socioeducativa'] = medida.group(1).strip() if medida else None

    return dados
