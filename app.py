from flask import Flask, render_template, jsonify
import subprocess
import datetime

app = Flask(__name__)
start_time = datetime.datetime.now()

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

@app.route('/monitor')
def monitor():
    uptime = str(datetime.datetime.now() - start_time).split('.')[0]
    
    try:
        result = subprocess.run(
            ['docker', 'inspect', '--format', '{{.RestartCount}}', 'flask-app'],
            capture_output=True, text=True, timeout=3
        )
        restarts = result.stdout.strip() if result.stdout.strip() else "0"
    except:
        restarts = "0"

    return jsonify({
        "container_status": "running",
        "restart_count": restarts,
        "uptime": uptime
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
