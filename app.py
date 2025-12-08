import subprocess
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

PASSWORD = "556874"
PANEL_NAME = "StreamX"

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>دخول - {{ panel }}</title>
  <style>
    :root{
      --bg:#0f0f13;
      --card:#141318;
      --muted:#9aa0aa;
      --accent1:#b26bff;
      --accent2:#8a3dff;
      --input:#1e1e26;
      --glass: rgba(255,255,255,0.03);
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      background:linear-gradient(180deg,#08080a 0%, #0f0f13 100%);
      color:#fff;
      font-family: "Segoe UI", Tahoma, Arial, sans-serif;
      display:flex;
      align-items:center;
      justify-content:center;
      min-height:100vh;
      padding:20px;
    }
    .card{
      width:100%;
      max-width:420px;
      background:var(--card);
      border-radius:16px;
      padding:28px;
      box-shadow:0 6px 30px rgba(0,0,0,0.6);
      border:1px solid rgba(255,255,255,0.03);
    }
    .logo{
      display:flex;
      gap:10px;
      align-items:center;
      margin-bottom:12px;
    }
    .badge{
      background:linear-gradient(90deg,var(--accent1),var(--accent2));
      width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:bold;color:#fff;font-size:18px;
      box-shadow:0 6px 20px rgba(138,61,255,0.18);
    }
    h1{font-size:20px;margin:0}
    p.sub{color:var(--muted);margin:6px 0 18px;font-size:13px}

    form{display:flex;flex-direction:column;gap:12px}
    input[type="password"]{
      padding:12px;border-radius:10px;border:none;background:var(--input);color:#fff;font-size:15px;
    }
    button.btn{
      padding:12px;border-radius:10px;border:none;background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#fff;font-weight:600;font-size:16px;
      cursor:pointer;
      box-shadow:0 8px 26px rgba(138,61,255,0.12);
    }
    .footer-note{font-size:12px;color:var(--muted);text-align:center;margin-top:10px}

    @media(max-width:420px){
      .card{padding:18px}
    }
  </style>
</head>
<body>
  <div class="card" role="main">
    <div class="logo">
      <div class="badge">{{ panel[0] }}</div>
      <div>
        <h1>{{ panel }}</h1>
        <p class="sub">أدخل كلمة المرور للدخول إلى لوحة التحكم</p>
      </div>
    </div>
    <form method="POST" aria-label="login-form">
      <input name="password" type="password" placeholder="كلمة المرور" required>
      <button class="btn" type="submit">دخول</button>
      {% if error %}
        <p style="color:#ff6b6b;margin:6px 0 0;font-size:13px">{{ error }}</p>
      {% endif %}
    </form>
    <p class="footer-note">نسخة واجهة موبايل — Dark UI</p>
  </div>
</body>
</html>
"""

CONTROL_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>لوحة التحكم - {{ panel }}</title>
  <style>
    :root{
      --bg:#0f0f13;
      --card:#121218;
      --muted:#9aa0aa;
      --accent1:#b26bff;
      --accent2:#8a3dff;
      --glass: rgba(255,255,255,0.03);
      --input:#1e1e26;
    }
    *{box-sizing:border-box}
    body{
      margin:0;background:linear-gradient(#09090b,#0f0f13);color:#fff;font-family:Arial, sans-serif;padding:14px;
    }
    .top{
      display:flex;align-items:center;justify-content:space-between;gap:12px;
    }
    .panel-title{display:flex;gap:12px;align-items:center}
    .logo{
      background:linear-gradient(90deg,var(--accent1),var(--accent2));
      width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:bold;color:#fff;font-size:18px;
      box-shadow:0 8px 26px rgba(138,61,255,0.12);
    }
    h2{margin:0;font-size:18px}
    .status{
      display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted);
    }
    .status .dot{width:10px;height:10px;border-radius:50%;background:#4CAF50;box-shadow:0 2px 6px rgba(76,175,80,0.2)}

    /* card */
    .card{margin-top:16px;background:var(--card);border-radius:16px;padding:16px;border:1px solid rgba(255,255,255,0.03)}
    .cpu-row{display:flex;align-items:center;gap:14px;justify-content:space-between}
    .cpu-left{flex:1}
    .cpu-percent{font-size:20px;color:var(--accent1);font-weight:700}
    .spark{height:120px;background:linear-gradient(180deg,#7d3cff22,transparent);border-radius:12px;padding:12px;position:relative;overflow:hidden}
    /* animated line (fake sparkline) */
    .spark svg{width:100%;height:100%;}
    .label-muted{color:var(--muted);font-size:13px;margin-top:8px}

    /* inputs */
    .field{margin-top:14px}
    label{display:block;color:var(--muted);font-size:13px;margin-bottom:8px}
    input[type="text"], input[type="password"]{
      width:100%;padding:12px;border-radius:12px;border:none;background:var(--input);color:#fff;font-size:15px;
    }

    /* action */
    .action{margin-top:18px;display:flex;gap:12px;flex-direction:column}
    .btn-live{
      padding:14px;border-radius:14px;border:none;background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#fff;font-weight:700;font-size:16px;
      display:flex;align-items:center;justify-content:center;gap:10px;cursor:pointer;
    }
    .btn-ghost{padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);background:transparent;color:var(--muted);font-size:14px}

    /* footer small */
    .small{font-size:12px;color:var(--muted);margin-top:12px}

    /* Modal */
    .modal{display:none;position:fixed;z-index:2000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.6);align-items:center;justify-content:center}
    .modal.show{display:flex}
    .modal-box{background:#101016;padding:18px;border-radius:12px;max-width:320px;width:90%;text-align:center;border:1px solid rgba(255,255,255,0.03)}
    .modal-box p{margin:0 0 12px;color:#fff}
    .modal-btn{padding:10px 18px;border-radius:10px;border:none;background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#fff;font-weight:700;cursor:pointer}

    /* small icons row */
    .icons{display:flex;gap:12px;margin-top:12px}
    .icon{
      background:var(--glass);padding:10px;border-radius:10px;display:flex;align-items:center;gap:8px;color:var(--muted);font-size:13px;
    }

    @media (max-width:480px){
      .cpu-percent{font-size:18px}
      .spark{height:100px}
    }
  </style>
</head>
<body>

  <div class="top">
    <div class="panel-title">
      <div class="logo">{{ panel[0] }}</div>
      <div>
        <h2>{{ panel }}</h2>
        <div class="status"><span class="dot"></span><span>النظام متصل</span></div>
      </div>
    </div>
    <div style="text-align:left">
      <button onclick="logout()" class="btn-ghost">تسجيل خروج</button>
    </div>
  </div>

  <div class="card" role="region" aria-label="cpu-card">
    <div class="cpu-row">
      <div class="cpu-left">
        <div class="cpu-percent" id="cpuPercent">66%</div>
        <div class="label-muted">وحدة المعالجة المركزية (CPU)</div>
      </div>
      <div style="width:55%">
        <div class="spark" aria-hidden="true">
          <!-- inline SVG sparkline: we'll animate path via JS -->
          <svg id="sparkSvg" viewBox="0 0 300 80" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <path id="sparkPath" d="" fill="none" stroke="#c084ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>
          </svg>
        </div>
      </div>
    </div>
    <div class="icons" aria-hidden="true">
      <div class="icon">📶 شبكة</div>
      <div class="icon">⚙️ إعدادات</div>
      <div class="icon">🔑 مفتاح</div>
    </div>

    <form method="POST" id="streamForm" style="margin-top:12px;">
      <div class="field">
        <label>رابط المصدر (M3U8)</label>
        <input name="m3u8" type="text" placeholder="https://server.com/live/stream.m3u8" required>
      </div>
      <div class="field">
        <label>مفتاح البث (Stream Key)</label>
        <input name="key" type="password" placeholder="FB-xxxxxxxxxxxxxxxx" required>
      </div>

      <div class="action">
        <button type="submit" class="btn-live">⚡ تشغيل نظام البث</button>
        <button type="button" class="btn-ghost" onclick="copyPreview()">معاينة الرابط</button>
      </div>
    </form>

    <div class="small">تصميم موبايل — الألوان بنفسجية وداكنة</div>
  </div>

  <!-- Modal -->
  <div id="successModal" class="modal" role="dialog" aria-modal="true" aria-hidden="true">
    <div class="modal-box">
      <p id="modalText">تم تشغيل البث بنجاح!</p>
      <button class="modal-btn" onclick="closeModal()">موافق</button>
    </div>
  </div>

<script>
  // Logout helper (redirect to root)
  function logout(){
    window.location.href = "/";
  }

  // Modal functions
  function showModal(text){
    const modal = document.getElementById("successModal");
    document.getElementById("modalText").innerText = text || "تم تشغيل البث بنجاح!";
    modal.classList.add("show");
    modal.setAttribute("aria-hidden","false");
    // اختفاء تلقائي بعد 3.5 ثانية
    setTimeout(()=>{ closeModal(); }, 3500);
  }
  function closeModal(){
    const modal = document.getElementById("successModal");
    modal.classList.remove("show");
    modal.setAttribute("aria-hidden","true");
  }

  // Fake CPU sparkline generator (client-side)
  const svg = document.getElementById("sparkSvg");
  const path = document.getElementById("sparkPath");
  const cpuPercentEl = document.getElementById("cpuPercent");

  // generate moving data points and render path
  const points = [];
  const POINTS = 30;
  // init points
  for(let i=0;i<POINTS;i++){
    points.push( Math.round(30 + Math.random()*40) ); // start around 30-70
  }

  function drawSpark(){
    const w = 300;
    const h = 80;
    const step = w / (POINTS-1);
    let d = "";
    for(let i=0;i<POINTS;i++){
      const x = (i*step);
      const val = points[i];
      // map val (0-100) to y (padding)
      const y = h - (val/100)* (h - 12) - 6;
      d += (i===0 ? `M ${x} ${y}` : ` L ${x} ${y}`);
    }
    path.setAttribute("d", d);
    // update percent text to latest point
    const latest = points[points.length-1];
    cpuPercentEl.innerText = latest + "%";
  }

  // animate: every 800ms shift and push new random value (simulate CPU)
  setInterval(()=>{
    // push new value influenced by previous to be smoother
    const prev = points[points.length-1];
    let change = (Math.random()*14 - 7); // -7..+7
    let next = Math.max(6, Math.min(95, Math.round(prev + change)));
    points.shift();
    points.push(next);
    drawSpark();
  }, 800);

  // On form submit: open modal (we also let backend start ffmpeg)
  document.getElementById("streamForm").addEventListener("submit", function(e){
    // show modal immediately (optimistic)
    showModal("جارٍ تشغيل البث...");
    // allow form to submit normally to backend
  });

  // copyPreview: just show a small modal (demo)
  function copyPreview(){
    showModal("ميزة المعاينة مؤقتة (Demo)");
  }

  // If server returned success flag, show modal
  {% if success %}
    // use setTimeout so DOM ready
    setTimeout(()=>{ showModal("تم تشغيل البث بنجاح!"); }, 200);
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
            error = "كلمة المرور خاطئة"
    return render_template_string(LOGIN_HTML, error=error, panel=PANEL_NAME)

@app.route("/stream", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        m3u8 = request.form.get("m3u8", "").strip()
        key = request.form.get("key", "").strip()

        # validate minimal
        if not m3u8 or not key:
            return render_template_string(CONTROL_HTML, success=False, panel=PANEL_NAME)

        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        # Start ffmpeg as background process (non-blocking)
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
            # if ffmpeg fails to start, show modal with error
            return render_template_string(CONTROL_HTML, success=False, panel=PANEL_NAME)

        # render page with success modal
        return render_template_string(CONTROL_HTML, success=True, panel=PANEL_NAME)

    return render_template_string(CONTROL_HTML, success=False, panel=PANEL_NAME)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6080)
