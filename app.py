from flask import Flask, render_template, request
from datetime import datetime
import subprocess
import psutil

app = Flask(__name__)

# قائمة سجلات البث
stream_logs = []

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""

    if request.method == 'POST':
        m3u8 = request.form.get('m3u8')
        key = request.form.get('key')

        # رابط RTMPS للفيسبوك
        rtmps_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        # وقت بداية البث
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # تشغيل FFmpeg
        try:
            subprocess.Popen([
                "ffmpeg",
                "-i", m3u8,
                "-c:v", "copy",
                "-c:a", "aac",
                "-f", "flv",
                rtmps_url
            ])

            # سجل البث
            stream_logs.append({
                "m3u8": m3u8,
                "key": key,
                "start_time": start_time,
                "cpu": psutil.cpu_percent()
            })

            message = f"تم بدء البث في {start_time}"

        except Exception as e:
            message = f"خطأ أثناء بدء البث: {str(e)}"

    cpu_percent = psutil.cpu_percent()
    return render_template("index.html", cpu_percent=cpu_percent, message=message, logs=stream_logs)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
