# Library imports
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def form():
    return render_template('index.html')


@app.route("/", methods=['POST', 'GET'])
def tracker():
    errors = []
    results = []
    if request.method == 'POST':
        try:
            code = request.form['trackingcode']
            req = requests.post(url='https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?',
                                data={'objetos': code})
            soup = BeautifulSoup(req.text, 'html.parser')
            status = soup.find('td', {'class': 'sroLbEvent'}).strong.text
            results.append(status)
            date = soup.find(id='UltimoEvento').text.split()[-1]
            results.append(date)
            return render_template('index.html', results=results)
        except:
            errors.append("O código é inválido. Por favor verifique e tente novamente.")
            return render_template('index.html', errors=errors)


if __name__ == "__main__":
    app.run()
    
