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

        # إيقاف أي بث سابق
        if STREAM_PROCESS:
            try:
                STREAM_PROCESS.kill()
            except Exception as e:
                message += f"خطأ أثناء إيقاف البث السابق: {str(e)}\n"
            STREAM_PROCESS = None

        # أمر FFmpeg
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

        try:
            # تشغيل FFmpeg و التقاط الأخطاء
            STREAM_PROCESS = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            message = "تم تشغيل البث بنجاح!"
        except Exception as e:
            message = f"حدث خطأ أثناء تشغيل البث: {str(e)}"

    return render_template("index.html", message=message)


@app.route("/stop")
def stop():
    global STREAM_PROCESS
    if STREAM_PROCESS:
        try:
            STREAM_PROCESS.kill()
            STREAM_PROCESS = None
            return "تم إيقاف البث."
        except Exception as e:
            return f"حدث خطأ أثناء الإيقاف: {str(e)}"
    return "لا يوجد بث شغّال."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
