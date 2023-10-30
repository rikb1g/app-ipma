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
    imagem = None
    video = obter_video(1)
    

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
                    'data_consulta': dados_clima['data'][0]['forecastDate'],
                    'id_estado_tempo': dados_clima['data'][0]['idWeatherType']
                }
                
                video = obter_video(clima['id_estado_tempo'])
                nome_cidade = obter_cidade(cidade_id)
                imagem = obter_icone_tempo(clima['id_estado_tempo'])

                
                

    # Renderiza o template com os dados
    return render_template('index.html', clima=clima, nome_cidade=nome_cidade,imagem = imagem, video= video)

@app.route("/prev5dias", methods=['GET', 'POST'])
def prev5dias():
    cidade_id = session.get('cidade_id')
    nome_cidade = None
    clima_1 = None
    clima_2 = None
    clima_3 = None
    clima_4 = None
    video = obter_video(1)

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
                'data_consulta1': dados_clima['data'][1]['forecastDate'],
                'id_estado_tempo1': dados_clima['data'][1]['idWeatherType']
            }
            imagem_1 = obter_icone_tempo(clima_1['id_estado_tempo1'])
            clima_2 = {
                'temperatura_max2': dados_clima['data'][2]['tMax'],
                'temperatura_min2': dados_clima['data'][2]['tMin'],
                'probabilidade_prec2': dados_clima['data'][2]['precipitaProb'],
                'data_consulta2': dados_clima['data'][2]['forecastDate'],
                'id_estado_tempo2': dados_clima['data'][2]['idWeatherType']
            }
            imagem_2 = obter_icone_tempo(clima_2['id_estado_tempo2'])
            
            clima_3 = {
                'temperatura_max3': dados_clima['data'][3]['tMax'],
                'temperatura_min3': dados_clima['data'][3]['tMin'],
                'probabilidade_prec3': dados_clima['data'][3]['precipitaProb'],
                'data_consulta3': dados_clima['data'][3]['forecastDate'],
                'id_estado_tempo3': dados_clima['data'][3]['idWeatherType']
            }
            imagem_3 = obter_icone_tempo(clima_3['id_estado_tempo3'])
            clima_4 = {
                'temperatura_max4': dados_clima['data'][4]['tMax'],
                'temperatura_min4': dados_clima['data'][4]['tMin'],
                'probabilidade_prec4': dados_clima['data'][4]['precipitaProb'],
                'data_consulta4': dados_clima['data'][4]['forecastDate'],
                'id_estado_tempo4': dados_clima['data'][4]['idWeatherType']
            }
            imagem_4 = obter_icone_tempo(clima_4['id_estado_tempo4'])
            
            video = obter_video()
            nome_cidade = obter_cidade(cidade_id)


            return render_template('prev5dias.html', nome_cidade= nome_cidade, clima_1=clima_1, clima_2=clima_2, clima_3=clima_3, clima_4=clima_4, imagem_1 = imagem_1, imagem_2= imagem_2, imagem_3= imagem_3, imagem_4= imagem_4)
    else:
        return "Cidade não encontrada na sessão"

# Inicia a aplicação

def obter_cidade(cidade_id):
    if cidade_id == "1110600":
        return "Lisboa"
    elif cidade_id == "1131200":
        return "Porto"
    elif cidade_id == "1141600":
        return "Santarém"
    elif cidade_id == "1010500":
        return "Aveiro"
    elif cidade_id == "1020500":
        return "Beja"
    elif cidade_id == "1030300":
        return "Braga"
    elif cidade_id == "1040200":
        return "Bragança"
    elif cidade_id == "1050200":
        return "Castelo Branco"
    elif cidade_id == "1060300":
        return "Coimbra"
    elif cidade_id == "1070500":
        return "Évora"
    elif cidade_id == "1080500":
        return "Faro"
    elif cidade_id == "1090700":
        return "Guarda"
    elif cidade_id == "1100900":
        return "Leiria"
    elif cidade_id == "1151200":
        return "Setúbal"
    elif cidade_id == "1160900":
        return "Viana do Castelo"
    elif cidade_id == "1171400":
        return "Vila Real"
    elif cidade_id == "1182300":
        return "Viseu"
    return None


# obter o icone mediante o id do estado do tempo
def obter_icone_tempo(id_estado_tempo):
    if id_estado_tempo <=1:
        return url_for('static', filename='imagens/sol.svg')
    elif id_estado_tempo <=5:
        return url_for('static', filename='imagens/nublado.svg')
    elif id_estado_tempo <= 7:
        return url_for('static', filename='imagens/aguaceiros.svg')
    elif id_estado_tempo <= 15:
        return url_for('static', filename='imagens/chuva.svg')
    elif id_estado_tempo <= 17:
        return url_for('static', filename='imagens/nevoeiro.svg')
    elif id_estado_tempo == 19:
        return url_for('static', filename='imagens/neve.svg')
    return url_for('static', filename='imagens/padrao.svg')


# funçao para obter o video
def obter_video(id_estado_tempo):
    if id_estado_tempo <=1:
        return url_for('static', filename='videos/sol.mp4')
    elif id_estado_tempo <=5:
        return url_for('static', filename='videos/nublado.mp4')
    elif id_estado_tempo <= 7:
        return url_for('static', filename='videos/chuva.mp4')
    elif id_estado_tempo <= 15:
        return url_for('static', filename='videos/chuva.mp4')
    elif id_estado_tempo <= 17:
        return url_for('static', filename='videos/nublado.mp4')
    elif id_estado_tempo == 19:
        return url_for('static', filename='videos/neve.mp4')
    return url_for('static', filename='videos/sol.mp4')

    
                

# Inicia a aplicação em modo de debug
if __name__ == '__main__':
    app.run(debug=True)
