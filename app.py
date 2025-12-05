import os
from flask import Flask, render_template, request, redirect, url_for
import subprocess
import threading
import psutil  # لقياس CPU

app = Flask(__name__)
STREAM_PROCESSES = []
MAX_BROADCASTS = 10  # يعتمد على CPU cores

def run_stream(m3u8, key):
    fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"
    cmd = [
        "ffmpeg",
        "-re",
        "-i", m3u8,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "flv",
        fb_url
    ]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route("/", methods=["GET", "POST"])
def index():
    cpu_percent = psutil.cpu_percent(interval=1)
    if request.method == "POST":
        return redirect(url_for("add_stream"))
    return render_template("add_stream.html", cpu_percent=cpu_percent, message="")

@app.route("/add", methods=["GET", "POST"])
def add_stream():
    message = ""
    cpu_percent = psutil.cpu_percent(interval=1)
    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        if len(STREAM_PROCESSES) >= MAX_BROADCASTS:
            message = f"وصلت الحد الأقصى للبثات حسب CPU: {MAX_BROADCASTS}"
        else:
            thread = threading.Thread(target=run_stream, args=(m3u8, key), daemon=True)
            thread.start()
            STREAM_PROCESSES.append(thread)
            message = "تم تشغيل البث بنجاح!"

    return render_template("add_stream.html", cpu_percent=cpu_percent, message=message)

@app.route("/stop")
def stop():
    global STREAM_PROCESSES
    for p in STREAM_PROCESSES:
        try:
            p.join(0)
        except:
            pass
    STREAM_PROCESSES = []
    return "تم إيقاف كل البثات."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
