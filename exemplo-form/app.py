from flask import Flask, request, render_template

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        return render_template('form.html', nome_processado=nome)
    return render_template('form.html')