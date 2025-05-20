import os
import zipfile
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # necessário para flash messages

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extrair_dados_txt(caminho_txt):
    with open(caminho_txt, 'r', encoding='utf-8') as file:
        texto = file.read()
    return [{
        "arquivo": os.path.basename(caminho_txt),
        "pagina": 1,
        "conteudo": texto.strip()
    }]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'zip_file' not in request.files:
            flash('Nenhum arquivo enviado')
            return redirect(request.url)

        file = request.files['zip_file']

        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            caminho_zip = os.path.join(UPLOAD_FOLDER, filename)
            file.save(caminho_zip)

            # Extrair ZIP
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(UPLOAD_FOLDER)

            dados_extraidos = []
            # Percorrer arquivos extraídos procurando .txt
            for nome_arquivo in os.listdir(UPLOAD_FOLDER):
                if nome_arquivo.lower().endswith('.txt'):
                    caminho_txt = os.path.join(UPLOAD_FOLDER, nome_arquivo)
                    dados_extraidos.extend(extrair_dados_txt(caminho_txt))

            if not dados_extraidos:
                flash('Nenhum arquivo .txt encontrado no ZIP enviado')
                return redirect(request.url)

            return render_template('dashboard_link.html', dados=dados_extraidos)

        else:
            flash('Arquivo enviado não é um ZIP válido')
            return redirect(request.url)

    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True)
