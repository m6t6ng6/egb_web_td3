from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Variable global para el contador
contador = 0

@app.route('/')
def index():
    return render_template('index.html', contador=contador)

@app.route('/aumentar', methods=['POST'])
def aumentar():
    global contador
    contador += 1
    return redirect(url_for('index'))

@app.route('/disminuir', methods=['POST'])
def disminuir():
    global contador
    contador -= 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)