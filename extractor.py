from PyPDF2 import PdfReader

def extrair_dados_pdf(caminho_pdf):
    dados_extraidos = []

    reader = PdfReader(caminho_pdf)

    for i, page in enumerate(reader.pages):
        texto = page.extract_text()
        if texto:
            dados_extraidos.append({
                "pagina": i + 1,
                "conteudo": texto.strip()
            })

    return dados_extraidos
