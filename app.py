import subprocess
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Stream Restream</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial; 
            background:#ececec; 
            padding:20px; 
            margin:0;
        }
        .box { 
            background:white; 
            padding:20px; 
            border-radius:10px; 
            max-width: 100%; 
            width: 100%; 
            margin:auto; 
            box-sizing: border-box;
        }
        input, button { 
            width:100%; 
            padding:12px; 
            margin-top:10px; 
            border-radius:6px; 
            box-sizing: border-box;
            font-size: 16px;
        }
        button { 
            background:#007bff; 
            color:white; 
            border:none; 
        }
        h2 { 
            text-align:center; 
            font-size: 20px;
        }

        /* تحسينات للشاشات الصغيرة فقط */
        @media (max-width: 480px) {
            body { padding: 10px; }
            .box { padding: 15px; }
            input, button { padding: 10px; font-size: 14px; }
            h2 { font-size: 18px; }
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>M3U8 → Facebook Live</h2>
        <form method="POST">
            <label>M3U8 Stream URL:</label>
            <input name="m3u8" placeholder="Enter m3u8 link" required>

            <label>Facebook Stream Key:</label>
            <input name="key" placeholder="FB-xxxxxxxxxxxxx" required>

            <button type="submit">Start Streaming</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        cmd = [
            "ffmpeg",
            "-re",
            "-i", m3u8,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "flv",
            fb_url
        ]

        subprocess.Popen(cmd)
        return "Streaming started successfully!"

    return render_template_string(HTML)

app.run(host="0.0.0.0", port=6080) 
