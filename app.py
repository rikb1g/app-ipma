from flask import Flask, render_template, request
import requests

# Inicializa a aplicação Flask
app = Flask(__name__)

# Endpoint da API do IPMA 
API_ENDPOINT = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"

# Define a rota principal que suporta métodos GET e POST
@app.route("/", methods=['GET', 'POST'])
def index():

    # Inicializa as variáveis
    nome_cidade = None
    clima = None
    clima_dia_seguinte = None

    # Verifica se o método é POST
    if request.method == "POST":
        # Vai buscar o ID da cidade a partir do formulário
        cidade_id = request.form.get("cidade")

        # Se cidade_id for válido, realiza a chamada à API
        if cidade_id:
            response = requests.get(f"{API_ENDPOINT}{cidade_id}.json", verify=False)
            dados_clima = response.json()

            # Verifica se a API retornou as informações com sucesso
            if response.status_code == 200:
                # Extrai e formata os dados do clima
                clima = {
                    'temperatura_max': dados_clima['data'][0]['tMax'],
                    'temperatura_min': dados_clima['data'][0]['tMin'],
                    'probabilidade_prec': dados_clima['data'][0]['precipitaProb'],
                    'data_consulta': dados_clima['data'][0]['forecastDate']
                }

                clima_dia_seguinte = {
                    'temperatura_max1': dados_clima['data'][1]['tMax'],
                    'temperatura_min1': dados_clima['data'][1]['tMin'],
                    'probabilidade_prec1': dados_clima['data'][1]['precipitaProb'],
                    'data_consulta1': dados_clima['data'][1]['forecastDate']
                }

                # Mapeia o ID da cidade para o nome da cidade
                if cidade_id == "1110600":
                    nome_cidade = "Lisboa"
                elif cidade_id == "1030300":
                    nome_cidade = "Porto"
                elif cidade_id == "1141600":
                    nome_cidade = "Santarém"
            else:
                # Se a API falhar, define o clima como None
                clima = None

    # Renderiza o template com os dados
    return render_template('index.html', clima=clima, nome_cidade=nome_cidade, clima_dia_seguinte=clima_dia_seguinte)

# Inicia a aplicação em modo de debug
if __name__ == '__main__':
    app.run(debug=True)