from flask import Flask, render_template, request
from datetime import datetime
import psutil

app = Flask(__name__)

# قائمة لتخزين سجلات البث
stream_logs = []

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        m3u8 = request.form.get('m3u8')
        key = request.form.get('key')
        cpu_percent = psutil.cpu_percent(interval=1)
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # تسجيل البث
        stream_logs.append({
            "m3u8": m3u8,
            "key": key,
            "cpu": cpu_percent,
            "start_time": start_time
        })
        message = f"Stream started at {start_time}"

    cpu_percent = psutil.cpu_percent(interval=1)
    return render_template('add_stream.html', cpu_percent=cpu_percent, message=message, logs=stream_logs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
