import os
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

STREAM_PROCESS = None

@app.route("/", methods=["GET", "POST"])
def index():
    global STREAM_PROCESS
    message = ""

    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        # Facebook RTMPS URL
        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        # إذا كان هناك بث قديم أوقفه
        if STREAM_PROCESS:
            STREAM_PROCESS.kill()

        # FFmpeg command
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

        STREAM_PROCESS = subprocess.Popen(cmd)
        message = "تم تشغيل البث بنجاح!"

    return render_template("index.html", message=message)


@app.route("/stop")
def stop():
    global STREAM_PROCESS
    if STREAM_PROCESS:
        STREAM_PROCESS.kill()
        STREAM_PROCESS = None
        return "تم إيقاف البث."
    return "لا يوجد بث شغّال."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))) 
