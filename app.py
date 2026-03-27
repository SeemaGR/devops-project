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
    return jsonify({"status": "running", "message": "App is healthy!"})

@app.route('/monitor')
def monitor():
    try:
        result = subprocess.run(
            ['docker', 'inspect', '--format',
             '{{.State.Status}} {{.RestartCount}}', 'flask-app'],
            capture_output=True, text=True
        )
        output = result.stdout.strip().split()
        status = output[0] if output else "unknown"
        restarts = output[1] if len(output) > 1 else "0"
    except Exception as e:
        status = "error"
        restarts = "0"

    uptime = str(datetime.datetime.now() - start_time).split('.')[0]
    return jsonify({
        "container_status": status,
        "restart_count": restarts,
        "uptime": uptime
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
