from flask import Flask, render_template, redirect, url_for, Response
from datetime import datetime
import os

app = Flask(__name__)

# Variables globales
target = 5
minimo = 4
maximo = 6

# Rutas de archivo
ruta_historial = "comandos_logs.csv"
ruta_estado = "current_state.csv"

# Crear encabezado si no existe
if not os.path.exists(ruta_historial):
    with open(ruta_historial, "w") as f:
        f.write("timestamp,set_target,set_minimo,set_maximo\n")


@app.route('/')
def index():
    return render_template('index.html', target=target, minimo=minimo, maximo=maximo)


# === TARGET ===
@app.route('/target/incrementar', methods=['POST'])
def target_inc():
    global target, minimo, maximo
    if target < 28:
        target += 1
        if minimo >= target:
            minimo = max(5, target - 1)
        if maximo <= target:
            maximo = min(33, target + 1)
    return redirect(url_for('index'))


@app.route('/target/decrementar', methods=['POST'])
def target_dec():
    global target, minimo, maximo
    if target > 5:
        target -= 1
        if minimo >= target:
            minimo = max(5, target - 1)
        if maximo <= target:
            maximo = min(33, target + 1)
    return redirect(url_for('index'))


# === MÍNIMO ===
@app.route('/minimo/incrementar', methods=['POST'])
def minimo_inc():
    global minimo, target
    if minimo < target - 1:
        minimo += 1
    return redirect(url_for('index'))


@app.route('/minimo/decrementar', methods=['POST'])
def minimo_dec():
    global minimo
    if minimo > 5:
        minimo -= 1
    return redirect(url_for('index'))


# === MÁXIMO ===
@app.route('/maximo/incrementar', methods=['POST'])
def maximo_inc():
    global maximo
    if maximo < 33:
        maximo += 1
    return redirect(url_for('index'))


@app.route('/maximo/decrementar', methods=['POST'])
def maximo_dec():
    global maximo, target
    if maximo > target + 1:
        maximo -= 1
    return redirect(url_for('index'))


# === EJECUTAR ===
@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    global target, minimo, maximo
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1️⃣ Agregar al CSV de logs
    with open(ruta_historial, "a") as f:
        f.write(f"{timestamp},set target {target},set minimo {minimo},set maximo {maximo}\n")

    # 2️⃣ Sobrescribir estado actual
    with open(ruta_estado, "w") as f:
        f.write(f"set target {target}, set minimo {minimo}, set maximo {maximo}")

    print(f"✅ Log agregado en {ruta_historial} y estado sobrescrito en {ruta_estado}")
    return redirect(url_for('index'))


# === VER LOGS EN UNA NUEVA PÁGINA ===
@app.route('/ver_logs')
def ver_logs():
    """Muestra el contenido del archivo comandos_logs.csv en una nueva ventana."""
    if not os.path.exists(ruta_historial):
        return "<h3>Sin registros todavía.</h3>"

    with open(ruta_historial, "r") as f:
        lineas = f.readlines()

    html = """
    <html><head>
    <title>Logs de comandos</title>
    <style>
        body { font-family: monospace; background-color: #f8f8f8; padding: 1rem; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
        th { background-color: #e8e8e8; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style></head><body>
    <h2>📜 Registro de comandos ejecutados</h2>
    <table>
    <tr><th>Timestamp</th><th>Target</th><th>Mínimo</th><th>Máximo</th></tr>
    """
    for linea in lineas[1:]:
        campos = linea.strip().split(',')
        if len(campos) == 4:
            html += f"<tr><td>{campos[0]}</td><td>{campos[1]}</td><td>{campos[2]}</td><td>{campos[3]}</td></tr>"
    html += "</table></body></html>"
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)