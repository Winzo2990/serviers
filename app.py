import subprocess
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

PASSWORD = "556874"

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background:#0f0f17;
            color:white;
            font-family:Arial;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }
        .box {
            background:#1a1a27;
            padding:25px;
            border-radius:15px;
            width:90%;
            max-width:350px;
            text-align:center;
            box-shadow:0 0 20px #0008;
        }
        input, button {
            width:100%;
            padding:12px;
            margin-top:10px;
            border-radius:8px;
            border:none;
            font-size:15px;
        }
        input { background:#2a2a39; color:white; }
        button {
            background:#8b45ff;
            color:white;
            font-weight:bold;
        }
        .status{
            position:absolute;
            top:15px;
            right:15px;
            color:#7dff8b;
            font-size:16px;
        }
    </style>
</head>
<body>
    <div class="status">● Server Active</div>
    <div class="box">
        <h2>Enter Password</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
            <p style="color:red">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Control Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- أيقونات حقيقية -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <style>
        body {
            background:#0f0f17;
            color:white;
            font-family:Arial;
            padding:15px;
            margin:0;
        }
        .top {
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:20px;
        }
        .wifi {
            font-size:25px;
            color:#6b6bff;
        }
        .profile {
            font-size:25px;
            background:#8b45ff;
            padding:10px;
            border-radius:50%;
        }

        .title {
            font-size:23px;
            margin-bottom:15px;
            font-weight:bold;
        }

        .card {
            background:#1a1a27;
            padding:20px;
            border-radius:15px;
            box-shadow:0 0 15px #0006;
        }
        label {
            opacity:0.8;
            font-size:14px;
        }
        input {
            width:100%;
            padding:12px;
            margin-top:10px;
            background:#2a2a39;
            border:none;
            border-radius:8px;
            color:white;
            font-size:15px;
        }
        button {
            width:100%;
            background:#8b45ff;
            padding:15px;
            border:none;
            border-radius:10px;
            margin-top:15px;
            color:white;
            font-size:17px;
            font-weight:bold;
        }

        /* Dialog */
        #dialog {
            position:fixed;
            top:0;
            left:0;
            width:100%;
            height:100%;
            background:#000a;
            display:flex;
            justify-content:center;
            align-items:center;
            display:none;
        }
        .dialog-box {
            background:#1a1a27;
            padding:20px;
            border-radius:15px;
            text-align:center;
            width:80%;
            max-width:300px;
            box-shadow:0 0 20px #0009;
        }
        .dialog-box button {
            background:#8b45ff;
        }
    </style>
</head>
<body>

    <div class="top">
        <i class="fa-solid fa-wifi wifi"></i>
        <i class="fa-solid fa-broadcast-tower" style="display:none"></i>
        <i class="fa-solid fa-user profile"></i>
    </div>

    <div class="title">لوحة التحكم</div>

    <div class="card">
        <form method="POST">

            <label>(M3U8) رابط المصدر</label>
            <input name="m3u8" placeholder="https://server.com/live/stream.m3u8" required>

            <label>(Stream Key) مفتاح البث</label>
            <input name="key" placeholder="xxxx-xxxx-xxxx" required>

            <button type="submit">تشغيل نظام البث ⚡</button>
        </form>
    </div>

    {% if success %}
    <div id="dialog">
        <div class="dialog-box">
            <h3>✔ تم بدء البث بنجاح</h3>
            <button onclick="document.getElementById('dialog').style.display='none'">OK</button>
        </div>
    </div>
    <script>document.getElementById('dialog').style.display='flex';</script>
    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            return redirect(url_for("index"))
        else:
            error = "Incorrect password"
    return render_template_string(LOGIN_HTML, error=error)


@app.route("/stream", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        subprocess.Popen([
            "ffmpeg","-re",
            "-i", m3u8,
            "-c:v","copy",
            "-c:a","copy",
            "-f","flv",
            fb_url
        ])

        return render_template_string(HTML, success=True)

    return render_template_string(HTML)
    
app.run(host="0.0.0.0", port=6080) 
