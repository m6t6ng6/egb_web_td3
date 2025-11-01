from flask import Flask, render_template, redirect, url_for
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

    # 1️⃣ Agregar al log CSV (modo append)
    with open(ruta_historial, "a") as f:
        f.write(f"{timestamp},set target {target},set minimo {minimo},set maximo {maximo}\n")

    # 2️⃣ Sobrescribir el estado actual en CSV (una sola línea)
    with open(ruta_estado, "w") as f:
        f.write(f"set target {target}, set minimo {minimo}, set maximo {maximo}")

    print(f"✅ Log agregado en {ruta_historial} y estado sobrescrito en {ruta_estado}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)