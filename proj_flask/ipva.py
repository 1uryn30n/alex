from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def get_data():
    apiEstados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    apiFipe = 'https://parallelum.com.br/fipe/api/v1/'
    data = []
    dataForm = []
    response = requests.get(apiEstados)
    
    if response.status_code == 200:
        data.append(response.json())
        # return jsonify(dados_api)
        # data[0] = dados_api
        dataForm.append(request.args.get('estado'))
        dataForm.append(request.args.get('tipoVeiculo'))
        dataForm.append(request.args.get('marca'))
        dataForm.append(request.args.get('modelo'))
        if dataForm[1]:
          
            if dataForm[1] == '1':
                type = 'caminhoes'
            elif dataForm[1]  == '2':
                type = 'carros'
            else:
                type = 'motos'

            apiFipe = apiFipe+type+'/marcas'
            data.append(getAPI(apiFipe))
        apiFipe = apiFipe+type+'/marcas'+'/modelos'
        data.append(getAPI(apiFipe))
        
            
        return render_template('estados.html', data = data, dataForm = dataForm )
    else:
        return jsonify({'message': 'Erro ao acessar a API'}), 500

def getAPI(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        return jsonify({'message': 'Erro ao acessar a API'}), 500

if __name__ == '__main__':

    app.run(debug=True)
