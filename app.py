from flask import Flask, render_template, request, session, redirect, url_for
import requests

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = 'chave_s'
# Endpoint da API do IPMA 
API_ENDPOINT = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"

# Define a rota principal que suporta métodos GET e POST
@app.route("/", methods=['GET', 'POST'])
def index():
    # Inicializa as variáveis
    nome_cidade = None
    clima = None

    # Verifica se o método é POST
    if request.method == "POST":
        # Vai buscar o ID da cidade a partir do formulário
        cidade_id = request.form.get("cidade")
        session['cidade_id'] = cidade_id
        
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

                # Mapeia o ID da cidade para o nome da cidade
                if cidade_id == "1110600":
                    nome_cidade = "Lisboa"
                elif cidade_id == "1030300":
                    nome_cidade = "Porto"
                elif cidade_id == "1141600":
                    nome_cidade = "Santarém"

    # Renderiza o template com os dados
    return render_template('index.html', clima=clima, nome_cidade=nome_cidade)

@app.route("/prev5dias", methods=['GET', 'POST'])
def prev5dias():
    cidade_id = session.get('cidade_id')
    nome_cidade = None
    clima_1 = None
    clima_2 = None
    clima_3 = None
    clima_4 = None

    if request.method == "POST":
        # Vai buscar o ID da cidade a partir do formulário
        cidade_id = request.form.get("cidade_5dias")
        session['cidade_id'] = cidade_id
    if cidade_id:
        response = requests.get(f"{API_ENDPOINT}{cidade_id}.json", verify=False)
        dados_clima = response.json()

        if response.status_code == 200:
            clima_1 = {
                'temperatura_max1': dados_clima['data'][1]['tMax'],
                'temperatura_min1': dados_clima['data'][1]['tMin'],
                'probabilidade_prec1': dados_clima['data'][1]['precipitaProb'],
                'data_consulta1': dados_clima['data'][1]['forecastDate']
            }
            clima_2 = {
                'temperatura_max2': dados_clima['data'][2]['tMax'],
                'temperatura_min2': dados_clima['data'][2]['tMin'],
                'probabilidade_prec2': dados_clima['data'][2]['precipitaProb'],
                'data_consulta2': dados_clima['data'][2]['forecastDate']
            }
            
            clima_3 = {
                'temperatura_max3': dados_clima['data'][3]['tMax'],
                'temperatura_min3': dados_clima['data'][3]['tMin'],
                'probabilidade_prec3': dados_clima['data'][3]['precipitaProb'],
                'data_consulta3': dados_clima['data'][3]['forecastDate']
            }
            clima_4 = {
                'temperatura_max4': dados_clima['data'][4]['tMax'],
                'temperatura_min4': dados_clima['data'][4]['tMin'],
                'probabilidade_prec4': dados_clima['data'][4]['precipitaProb'],
                'data_consulta4': dados_clima['data'][4]['forecastDate']
            }
            if cidade_id == "1110600":
                    nome_cidade = "Lisboa"
            elif cidade_id == "1030300":
                    nome_cidade = "Porto"
            elif cidade_id == "1141600":
                    nome_cidade = "Santarém"
            return render_template('prev5dias.html', nome_cidade= nome_cidade, clima_1=clima_1, clima_2=clima_2, clima_3=clima_3, clima_4=clima_4)
    else:
        return "Cidade não encontrada na sessão"

# Inicia a aplicação


# Inicia a aplicação em modo de debug
if __name__ == '__main__':
    app.run(debug=True)
