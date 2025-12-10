import subprocess
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

PASSWORD = "556874"
PANEL_NAME = "streamX"

LOGIN_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Login - {{ panel }}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    :root{
      --bg-dark:#0f0f17;
      --card-dark:#1a1a27;
      --input-dark:#2a2a39;
      --accent:#8b45ff;
      --text:#ffffff;

      --bg-light:#f5f7fb;
      --card-light:#ffffff;
      --input-light:#f0f2f6;
      --text-dark:#071225;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family:Arial, Helvetica, sans-serif;
      height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      background:var(--bg-dark);
      color:var(--text);
      transition:background .25s, color .25s;
    }
    .card{
      width:100%;
      max-width:380px;
      background:var(--card-dark);
      border-radius:14px;
      padding:26px;
      box-shadow:0 8px 30px rgba(0,0,0,0.5);
      border:1px solid rgba(255,255,255,0.03);
    }
    .logo {
      display:flex;
      gap:12px;
      align-items:center;
      margin-bottom:10px;
    }
    .badge{
      width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;
      background:linear-gradient(90deg,var(--accent), #6b2bff);
      color:white;font-weight:700;font-size:18px;
      box-shadow:0 8px 30px rgba(138,61,255,0.12);
    }
    h1{margin:0;font-size:20px}
    p.sub{margin:6px 0 18px;color:rgba(255,255,255,0.8);font-size:13px}
    form{display:flex;flex-direction:column;gap:12px}
    input[type="password"]{
      padding:12px;border-radius:10px;border:none;background:var(--input-dark);color:var(--text);font-size:15px;
    }
    button.btn{
      padding:12px;border-radius:10px;border:none;background:linear-gradient(90deg,var(--accent),#6b2bff);color:white;font-weight:700;font-size:15px;cursor:pointer;
    }
    .footer{font-size:12px;color:rgba(255,255,255,0.6);text-align:center;margin-top:12px}

    /* Light theme overrides (applied by JS) */
    body.light { background: var(--bg-light); color: var(--text-dark); }
    body.light .card { background: var(--card-light); border-color: rgba(7,18,37,0.04); box-shadow: 0 8px 30px rgba(7,18,37,0.06); }
    body.light .sub { color: #5a6b7a; }
    body.light input[type="password"]{ background: var(--input-light); color: var(--text-dark); }
    body.light .footer { color: #5a6b7a; }

    @media(max-width:420px){
      .card{padding:18px}
    }
  </style>
</head>
<body>
  <div class="card" role="main">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div class="logo">
        <div class="badge">{{ panel[0]|upper }}</div>
        <div>
          <h1>{{ panel }}</h1>
          <p class="sub">Enter password to access control panel</p>
        </div>
      </div>
      <div>
        <button id="themeToggle" title="Toggle light/dark" style="background:transparent;border:none;color:inherit;font-size:18px;cursor:pointer">
          <i id="themeIcon" class="fa-solid fa-moon"></i>
        </button>
      </div>
    </div>

    <form method="POST" aria-label="login-form">
      <input name="password" type="password" placeholder="Password" required aria-label="password">
      <button class="btn" type="submit">Login</button>
      {% if error %}
        <p style="color:#ff6b6b;margin:6px 0 0;font-size:13px">{{ error }}</p>
      {% endif %}
    </form>

    <p class="footer">StreamX• V3</p>
  </div>

<script>
  // Theme toggle & persistence
  const toggle = document.getElementById('themeToggle');
  const icon = document.getElementById('themeIcon');
  const setTheme = (mode) => {
    if(mode === 'light'){ document.body.classList.add('light'); icon.className='fa-solid fa-sun'; }
    else { document.body.classList.remove('light'); icon.className='fa-solid fa-moon'; }
    localStorage.setItem('theme', mode);
  }
  const saved = localStorage.getItem('theme') || 'dark';
  setTheme(saved);
  toggle.addEventListener('click', ()=> setTheme(document.body.classList.contains('light') ? 'dark' : 'light'));
</script>
</body>
</html>
"""

CONTROL_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ panel }} - Control Panel</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    :root{
      --bg-dark:#0f0f17; --card-dark:#121218; --muted:#9aa0aa;
      --accent1:#b26bff; --accent2:#8a3dff;
      --input-dark:#1e1e26; --glass: rgba(255,255,255,0.03);
      --bg-light:#f5f7fb; --card-light:#ffffff; --text-dark:#071225; --input-light:#f1f3f7;
    }
    *{box-sizing:border-box}
    body{margin:0;font-family:Arial,Helvetica,sans-serif;padding:14px;background:var(--bg-dark);color:#fff;transition:background .25s,color .25s}
    .top{display:flex;justify-content:space-between;align-items:center}
    .brand{display:flex;gap:12px;align-items:center}
    .badge{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;
           background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#fff;font-weight:700;font-size:18px;
           box-shadow:0 8px 30px rgba(138,61,255,0.12)}
    h2{margin:0;font-size:18px}
    .status{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted)}
    .dot{width:10px;height:10px;border-radius:50%;background:#4CAF50;box-shadow:0 2px 6px rgba(76,175,80,0.2)}

    .card{margin-top:16px;background:var(--card-dark);border-radius:16px;padding:16px;border:1px solid rgba(255,255,255,0.03);box-shadow:0 10px 30px rgba(0,0,0,0.45)}
    .cpu-row{display:flex;gap:14px;align-items:center;justify-content:space-between}
    .cpu-left{flex:1}
    .cpu-percent{font-size:22px;color:var(--accent1);font-weight:700}
    .spark{height:120px;border-radius:12px;padding:8px;position:relative;overflow:hidden;background:linear-gradient(180deg,#7d3cff10,transparent)}

    /* sparkline uses SVG */
    svg{width:100%;height:100%}

    label{display:block;color:var(--muted);font-size:13px;margin-top:14px}
    input[type="text"], input[type="password"]{width:100%;padding:12px;border-radius:12px;border:none;background:var(--input-dark);color:#fff;font-size:15px;margin-top:8px}
    .actions{margin-top:18px;display:flex;flex-direction:column;gap:10px}
    .btn-live{padding:14px;border-radius:14px;border:none;background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#fff;font-weight:700;font-size:16px;cursor:pointer}
    .logout{background:transparent;border:1px solid rgba(255,255,255,0.04);color:var(--muted);padding:10px;border-radius:10px;cursor:pointer}

    .small{font-size:12px;color:var(--muted);margin-top:12px}

    /* Modal */
    .modal{display:none;position:fixed;z-index:2000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.6);align-items:center;justify-content:center}
    .modal.show{display:flex}
    .modal-box{background:var(--card-dark);padding:18px;border-radius:12px;max-width:340px;width:90%;text-align:center;border:1px solid rgba(255,255,255,0.03)}
    .modal-btn{padding:10px 18px;border-radius:10px;border:none;background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#fff;font-weight:700;cursor:pointer}

    /* icons row */
    .icons{display:flex;gap:12px;margin-top:12px}
    .icon{background:var(--glass);padding:10px;border-radius:10px;display:flex;align-items:center;gap:8px;color:var(--muted);font-size:13px}

    /* Light mode overrides */
    body.light{background:var(--bg-light);color:var(--text-dark)}
    body.light .card{background:var(--card-light);border-color:rgba(7,18,37,0.04);box-shadow:0 10px 30px rgba(7,18,37,0.06)}
    body.light input[type="text"], body.light input[type="password"]{background:var(--input-light);color:var(--text-dark)}
    body.light .small, body.light .status{color:#6b7280}
    body.light .icon{color:#6b7280;background:rgba(7,18,37,0.03)}
    @media(max-width:480px){ .cpu-percent{font-size:18px} .spark{height:100px} }
  </style>
</head>
<body>

  <div class="top">
    <div class="brand">
      <div class="badge">{{ panel[0]|upper }}</div>
      <div>
        <h2>{{ panel }}</h2>
        <div class="status"><span class="dot"></span><span id="srvStatus">Server Online</span></div>
      </div>
    </div>

    <div style="display:flex;gap:8px;align-items:center">
      <button id="themeToggle" title="Toggle theme" style="background:transparent;border:none;color:inherit;font-size:18px;cursor:pointer">
        <i id="themeIcon" class="fa-solid fa-moon"></i>
      </button>
      <button class="logout" onclick="logout()">Logout</button>
    </div>
  </div>

  <div class="card" role="region" aria-label="cpu-card">
    <div class="cpu-row">
      <div class="cpu-left">
        <div class="cpu-percent" id="cpuPercent">66%</div>
        <div class="small">CPU Usage</div>
      </div>
      <div style="width:55%">
        <div class="spark" aria-hidden="true">
          <svg id="sparkSvg" viewBox="0 0 300 80" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <path id="sparkPath" d="" fill="none" stroke="#c084ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    </div>

    <div class="icons" aria-hidden="true">
      <div class="icon"><i class="fa-solid fa-wifi"></i> Network</div>
      <div class="icon"><i class="fa-solid fa-signal"></i> Bitrate</div>
      <div class="icon"><i class="fa-solid fa-gear"></i> Settings</div>
    </div>

    <form method="POST" id="streamForm" style="margin-top:12px;">
      <label>Source URL (M3U8)</label>
      <input name="m3u8" type="text" placeholder="https://server.com/live/stream.m3u8" required>

      <label>Stream Key</label>
      <input name="key" type="password" placeholder="FB-xxxxxxxxxxxxxxxx" required>

      <div class="actions">
        <button type="submit" class="btn-live">Start Stream</button>
      </div>
    </form>

    <div class="small">StreamX• My server has been contacted. </div>
  </div>

  <!-- Modal -->
  <div id="successModal" class="modal" role="dialog" aria-modal="true" aria-hidden="true">
    <div class="modal-box">
      <p id="modalText">Stream started successfully!</p>
      <button class="modal-btn" onclick="closeModal()">OK</button>
    </div>
  </div>

<script>
  // Theme toggle & persistence
  const toggle = document.getElementById('themeToggle');
  const icon = document.getElementById('themeIcon');
  const setTheme = (mode) => {
    if(mode === 'light'){ document.body.classList.add('light'); icon.className='fa-solid fa-sun'; }
    else { document.body.classList.remove('light'); icon.className='fa-solid fa-moon'; }
    localStorage.setItem('theme', mode);
  }
  const saved = localStorage.getItem('theme') || 'dark';
  setTheme(saved);
  toggle.addEventListener('click', ()=> setTheme(document.body.classList.contains('light') ? 'dark' : 'light'));

  // Logout helper
  function logout(){ window.location.href = "/"; }

  // Modal functions
  function showModal(text){
    const modal = document.getElementById("successModal");
    document.getElementById("modalText").innerText = text || "Stream started successfully!";
    modal.classList.add("show");
    modal.setAttribute("aria-hidden","false");
    setTimeout(()=>{ closeModal(); }, 3500); // auto-close
  }
  function closeModal(){
    const modal = document.getElementById("successModal");
    modal.classList.remove("show");
    modal.setAttribute("aria-hidden","true");
  }

  // CPU sparkline logic (client-side realistic animation)
  const points = [];
  const POINTS = 30;
  for(let i=0;i<POINTS;i++){ points.push(Math.round(20 + Math.random()*60)); } // 20-80 start

  const path = document.getElementById('sparkPath');
  const cpuEl = document.getElementById('cpuPercent');

  function drawSpark(){
    const w = 300, h = 80;
    const step = w / (POINTS - 1);
    let d = '';
    for(let i=0;i<POINTS;i++){
      const x = (i * step);
      const val = points[i];
      const y = h - (val / 100) * (h - 12) - 6;
      d += (i===0 ? `M ${x} ${y}` : ` L ${x} ${y}`);
    }
    path.setAttribute('d', d);
    const latest = points[points.length - 1];
    cpuEl.innerText = latest + '%';
  }

  // Smooth random generator each second
  setInterval(()=>{
    const prev = points[points.length - 1];
    const change = (Math.random() * 12 - 6); // -6..+6
    let next = Math.round(prev + change);
    next = Math.max(5, Math.min(95, next));
    points.shift(); points.push(next);
    drawSpark();
  }, 1000);

  // On form submit: show optimistic modal while backend handles ffmpeg
  document.getElementById('streamForm').addEventListener('submit', function(e){
    // show starting modal immediately
    showModal('Starting stream...');
    // allow form to submit normally (POST)
  });

  // If server returned success flag (template var), show final success
  {% if success %}
    setTimeout(()=>{ showModal("Stream started successfully!"); }, 200);
  {% endif %}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == PASSWORD:
            return redirect(url_for("index"))
        else:
            error = "Incorrect password"
    return render_template_string(LOGIN_HTML, error=error, panel=PANEL_NAME)

@app.route("/stream", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        m3u8 = request.form.get("m3u8", "").strip()
        key = request.form.get("key", "").strip()
        if not m3u8 or not key:
            return render_template_string(CONTROL_HTML, success=False, panel=PANEL_NAME)

        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"
        try:
            subprocess.Popen([
                "ffmpeg",
                "-re",
                "-i", m3u8,
                "-c:v", "copy",
                "-c:a", "copy",
                "-f", "flv",
                fb_url
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            # could not start ffmpeg: show panel without success modal
            return render_template_string(CONTROL_HTML, success=False, panel=PANEL_NAME)

        return render_template_string(CONTROL_HTML, success=True, panel=PANEL_NAME)

    return render_template_string(CONTROL_HTML, success=False, panel=PANEL_NAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6080)
