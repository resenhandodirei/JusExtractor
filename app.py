from flask import Flask, request, render_template, redirect, url_for
from collections import Counter
import json
import os
from extractor import extrair_dados_peticao

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("files[]")
    if not uploaded_files or uploaded_files[0].filename == '':
        return redirect(url_for('index'))

    # Salvar arquivos .txt na pasta uploads
    for file in uploaded_files:
        if file.filename.endswith('.txt'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

    return redirect(url_for('processar'))

@app.route('/processar')
def processar():
    dados_peticoes = []
    arquivos = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.txt')]
    print(f"Arquivos encontrados: {arquivos}")

    for arquivo in arquivos:
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], arquivo)
        print(f"Lendo arquivo: {caminho}")
        with open(caminho, 'r', encoding='utf-8') as f:
            texto = f.read()
            dados = extrair_dados_peticao(texto)
            print(f"Dados extraídos: {dados}")
            dados_peticoes.append(dados)

    if not dados_peticoes:
        print("Nenhum dado processado.")
        return "Nenhum dado processado ainda."

    # Agregando dados para os gráficos
    idades = [d['idade'] for d in dados_peticoes if d['idade'] is not None]
    tipos_infracao = [d['tipo_infracao'] for d in dados_peticoes if d['tipo_infracao']]

    contagem_idade = dict(Counter(idades))
    contagem_infracao = dict(Counter(tipos_infracao))
    contagem_genero = dict(Counter([d['genero'] for d in dados_peticoes if d['genero']]))
    contagem_escolaridade = dict(Counter([d['escolaridade'] for d in dados_peticoes if d['escolaridade']]))
    contagem_nacionalidade = dict(Counter([d['nacionalidade'] for d in dados_peticoes if d['nacionalidade']]))
    contagem_decisao = dict(Counter([d['decisao'] for d in dados_peticoes if d['decisao']]))


    return render_template(
    'dashboard.html',
    dados=dados_peticoes,
    contagem_idade=json.dumps(contagem_idade),
    contagem_infracao=json.dumps(contagem_infracao),
    contagem_genero=json.dumps(contagem_genero),
    contagem_escolaridade=json.dumps(contagem_escolaridade),
    contagem_nacionalidade=json.dumps(contagem_nacionalidade),
    contagem_decisao=json.dumps(contagem_decisao),
)


if __name__ == '__main__':
    app.run(debug=True)