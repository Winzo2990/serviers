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

    <p class="footer">Mobile-friendly • Light/Dark mode</p>
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
    body.light .card{background:var(--card-light);border-color:rgba(7,18,37,0.04);box-shadow:0 10px 30px rgba(7
