from dash import Dash, html, dcc, dash_table, Input, Output, callback_context
import dash_bootstrap_components as dbc

def create_dash_app(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = html.Div([
        html.H2("Dashboard JusExtractor"),
        html.P("Aqui estão os dados extraídos dos PDFs enviados."),
        dcc.Interval(id='interval', interval=1000, n_intervals=0, max_intervals=1),
        html.Div(id='tabela-container'),
    ])

    @dash_app.callback(
        Output('tabela-container', 'children'),
        Input('interval', 'n_intervals')
    )
    def atualizar_tabela(n):
        # Importar a variável global do Flask
        from app import dados_processados

        if not dados_processados:
            return html.Div("Nenhum dado processado ainda.")

        # Montar linhas para o DataTable
        linhas = []
        for item in dados_processados:
            nome = item.get('nome_arquivo', 'Arquivo desconhecido')
            dados = item.get('dados', {})
            # Para simplificar, vamos transformar dados em string
            dados_str = str(dados)
            linhas.append({'Arquivo': nome, 'Dados extraídos': dados_str})

        tabela = dash_table.DataTable(
            columns=[
                {"name": "Arquivo PDF", "id": "Arquivo"},
                {"name": "Dados Extraídos", "id": "Dados extraídos"},
            ],
            data=linhas,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'},
            page_size=10,
        )
        return tabela

    return dash_app
