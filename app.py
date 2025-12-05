import os
from flask import Flask, render_template, request
import subprocess
import threading

app = Flask(__name__)
STREAM_PROCESSES = []

MAX_BROADCASTS = 2  # عدد البثات التي يعتمد على CPU

def run_stream(m3u8, key):
    fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"
    cmd = [
        "ffmpeg",
        "-re",
        "-i", m3u8,
        "-c:v", "copy",  # لا ترميز الفيديو → أقل RAM
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "flv",
        fb_url
    ]
    # تشغيل FFmpeg مع عدم تخزين stdout/stderr في RAM
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        if len(STREAM_PROCESSES) >= MAX_BROADCASTS:
            message = f"وصلت للحد الأقصى من البثات حسب CPU: {MAX_BROADCASTS}"
        else:
            thread = threading.Thread(target=run_stream, args=(m3u8, key), daemon=True)
            thread.start()
            STREAM_PROCESSES.append(thread)
            message = "تم تشغيل البث! يعتمد فقط على CPU الآن."

    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
