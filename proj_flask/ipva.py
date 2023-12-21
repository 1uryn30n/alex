from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def get_data():
    apiEstados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    apiFipe = 'https://parallelum.com.br/fipe/api/v1/'
    data = []
    dataForm = []
    valor_sem =''
    response = requests.get(apiEstados)
    
    if response.status_code == 200:

        data.append(response.json()) # data[0]

        dataForm.append(request.args.get('estado')) # dataForm[0]
        dataForm.append(request.args.get('tipoVeiculo')) # dataForm[1]
        dataForm.append(request.args.get('marca')) # dataForm[2]
        dataForm.append(request.args.get('modelo')) # dataForm[3]
        dataForm.append(request.args.get('ano')) # dataForm[4]

        if dataForm[1]: # TIPO VEICULO
            if dataForm[1] == '1':
                type = 'caminhoes'
            elif dataForm[1]  == '2':
                type = 'carros'
            else:
                type = 'motos'

            apiFipe = apiFipe+type+'/marcas/'
            data.append(getAPI(apiFipe)) # data[1]

        if dataForm[2]: 
            apiFipe = apiFipe+dataForm[2]+'/modelos/'
            data.append(getAPI(apiFipe)) # data[2]

        if dataForm[3]: 
            apiFipe = apiFipe+dataForm[3]+'/anos/'
            data.append(getAPI(apiFipe)) # data[3]

        if dataForm[4]: 
            apiFipe = apiFipe+dataForm[4]
            obj = getAPI(apiFipe) # data[4]  !! DADOS FINAIS !!
            valor_sem = obj['Valor']
            valor_sem = valor_sem.replace('R$', '')
            valor_sem = valor_sem.replace('.', '')
            valor_sem = valor_sem.replace(',', '.')
            valor_sem = float(valor_sem)
           
            data.append(calc(dataForm[0], dataForm[1],valor_sem))



        
        return render_template('estados.html', data = data, dataForm = dataForm, valor_sem = valor_sem)
    
    else:
        return jsonify({'message': 'Erro ao acessar a API'}), 500
    
# Estado	            Carro	Caminhoes	Motocicletas
# Acre	                2,00%	1,00%	    1,00%
# Alagoas	            3,00%	3,25%	    1,00%
# Amapá	                3,00%	3,00%	    1,50%
# Amazonas	            3,00%	3,00%	    2,00%
# Bahia	                2,50%	2,50%	    2,50%
# Ceará	                2,50%	2,50%	    2,00%
# Distrito Federal	    2,00%	2,00%	    1,00%
# Espírito Santo	    2,00%	2,00%	    1,00%
# Goiás	                3,75%	3,45%	    3,00%
# Maranhão	            2,50%	2,50%	    2,00%
# Minas Gerais	        4,00%	3,00%	    2,00%
# Mato Grosso	        3,00%	2,50%	    2,50%
# Mato Grosso do Sul	3,00%	3,00%	    2,00%
# Pará	                2,50%	2,50%	    1,00%
# Paraíba	            2,50%	2,50%	    2,50%
# Paraná	            3,50%	3,50%	    3,50%
# Pernambuco	        2,50%	2,50%	    2,00%
# Piauí	                2,50%	2,50%	    2,00%
# Rio de Janeiro	    4,00%	3,00%	    2,00%
# Rio Grande do Norte	3,00%	3,00%   	1,50%
# Rio Grande do Sul	    3,00%	3,00%   	2,00%
# Rondônia	            3,00%	3,00%   	2,00%
# Roraima	            3,00%	2,00%   	2,00%
# Santa Catarina	    2,00%	2,00%   	1,00%
# Sergipe	            3,00%	2,50%   	2,00%
# São Paulo	            4,00%	2,00%     	2,00%
# Tocantins	            2,00%	3,00%   	2,00%

aliquota = [
    [2.00, 1.00, 1.00], # LINHA 0: ACRE , COLUNA 0: CAMINHOES
    [3.00, 3.25, 1.00],
    [3.00, 3.00, 1.50],
    [3.00, 3.00, 2.00],
    [2.50, 2.50, 2.50],
    [2.50, 2.50, 2.00],
    [2.00, 2.00, 1.00],
    [2.00, 2.00, 1.00],
    [3.75, 3.45, 3.00],
    [2.50, 2.50, 2.00],
    [4.00, 3.00, 2.00],
    [3.00, 2.50, 2.50],
    [3.00, 3.00, 2.00],
    [2.50, 2.50, 1.00],
    [2.50, 2.50, 2.50],
    [3.50, 3.50, 3.50],
    [2.50, 2.50, 2.00],
    [2.50, 2.50, 2.00],
    [4.00, 3.00, 2.00],
    [3.00, 3.00, 1.50],
    [3.00, 3.00, 2.00],
    [3.00, 3.00, 2.00],
    [3.00, 2.00, 2.00],
    [2.00, 2.00, 1.00],
    [3.00, 2.50, 2.00],
    [4.00, 2.00, 2.00],
    [2.00, 3.00, 2.00]
]

#elemento = aliquota[1]
#print(elemento)


def calc(estado, tipoVeiculo, valor):
    # ESTADO ID: 50
    if estado == '50': # SE FOR ESTADO TAL

        if tipoVeiculo == '1': # SE FOR CAMINHAO
            return ((valor / 100) * 3)
        
        elif tipoVeiculo == '2': # SE FOR CARRO
            return ((valor / 100) * 3)
        
        else: # SE FOR MOTO
            return ((valor / 100) * 2)
        
    # ESTADO ID: 35
    if estado == '35': # SE FOR ESTADO TAL

        if tipoVeiculo == '1': # SE FOR CAMINHAO
            return ((valor / 100) * 2)
        
        elif tipoVeiculo == '2': # SE FOR CARRO
            return ((valor / 100) * 4)
        
        else: # SE FOR MOTO
            return ((valor / 100) * 2)    
    
 

def getAPI(url):

    res = requests.get(url)

    if res.status_code == 200:
        return res.json()
    
    else:
        return jsonify({'message': 'Erro ao acessar a API'}), 500

if __name__ == '__main__':

    app.run(debug=True)
