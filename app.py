from flask import Flask, render_template, request, send_file
import os
from extractor import extrair_dados_pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf_file']
    
    if file.filename.endswith('.pdf'):
        caminho_pdf = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(caminho_pdf)

        caminho_excel = extrair_dados_pdf(caminho_pdf)

        return send_file(
            caminho_excel,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True
        )
    else:
        return 'Arquivo inválido. Envie um PDF.', 400

if __name__ == '__main__':
    app.run(debug=True)
