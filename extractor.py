import PyPDF2

def extrair_dados_pdf(caminho_pdf):
    dados = []

    with open(caminho_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for i, pagina in enumerate(reader.pages):
            texto = pagina.extract_text() or ''
            dados.append({
                "arquivo": caminho_pdf.split("/")[-1],
                "pagina": i + 1,
                "conteudo": texto.strip()
            })

    return dados
