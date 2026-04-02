from flask import Flask, render_template, jsonify, request
import subprocess
import datetime

app = Flask(__name__)
start_time = datetime.datetime.now()
restart_count = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "running", "message": "App is healthy - Version 3.0!"})

@app.route('/crash')
def crash():
    import os
    os.abort()

@app.route('/set-restarts/<int:count>')
def set_restarts(count):
    global restart_count
    restart_count = count
    return jsonify({"restart_count": restart_count, "message": "Updated!"})

@app.route('/monitor')
def monitor():
    global restart_count
    uptime = str(datetime.datetime.now() - start_time).split('.')[0]
    return jsonify({
        "container_status": "running",
        "restart_count": restart_count,
        "uptime": uptime
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)