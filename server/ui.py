UI_HTML = r"""
<!-- UI_HTML 교체용 (그대로 붙여넣기) -->
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Survey AutoRunner</title>
  <style>
    :root{
  /* 기본 = 다크 */
      --bg:#0b1020;
      --panel:#0f172a;
      --card:#111b33;
      --muted:#93a4c7;
      --text:#e9eefc;
      --line:#243258;
      --pri:#4f7cff;
      --pri2:#2dd4bf;
      --warn:#f59e0b;
      --danger:#ef4444;
      --ok:#22c55e;
      --shadow: 0 10px 30px rgba(0,0,0,.35);
      --radius: 14px;

      --bg-grad-1: rgba(79,124,255,.25);
      --bg-grad-2: rgba(45,212,191,.18);
      --bg-grad-3: rgba(245,158,11,.12);
    }
    /* 라이트 테마 */
    html[data-theme="light"]{
      --bg:#f7f9ff;
      --panel:#ffffff;
      --card:#ffffff;
      --muted:#55627a;
      --text:#0b1220;
      --line:#dbe3f4;
      --pri:#2f63ff;
      --pri2:#0ea5a4;
      --warn:#b45309;
      --danger:#dc2626;
      --ok:#16a34a;
      --shadow: 0 10px 30px rgba(12, 18, 32, .10);

      --bg-grad-1: rgba(47,99,255,.14);
      --bg-grad-2: rgba(14,165,164,.10);
      --bg-grad-3: rgba(180,83,9,.08);
    }
    *{ box-sizing:border-box; }
    /* body 배경도 변수로 */
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Apple Color Emoji, Noto Color Emoji, Arial, sans-serif;
      color:var(--text);
      background:
        radial-gradient(1200px 700px at 10% 10%, var(--bg-grad-1), transparent 60%),
        radial-gradient(1000px 600px at 90% 10%, var(--bg-grad-2), transparent 55%),
        radial-gradient(1100px 700px at 40% 95%, var(--bg-grad-3), transparent 60%),
        var(--bg);
    }
    a{ color:inherit; }
    .wrap{ max-width: 1100px; margin: 26px auto; padding: 0 16px 24px; }
    .topbar{
      display:flex; align-items:center; justify-content:space-between;
      gap:12px; margin-bottom:16px;
    }
    .brand{
      display:flex; align-items:center; gap:12px;
    }
    .logo{
      width:42px; height:42px; border-radius:12px;
      background: linear-gradient(135deg, rgba(79,124,255,.9), rgba(45,212,191,.85));
      box-shadow: var(--shadow);
    }
    h1{ margin:0; font-size:18px; letter-spacing:.2px; }
    .sub{ color:var(--muted); font-size:12px; margin-top:4px; }
    /* switch layout 안정화 */
    .pillrow{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      align-items:center;
    }    
    .pill{
      display:flex;
      align-items:center;
      gap:10px;
      padding:10px 12px;
      border:1px solid var(--line);
      background: var(--card);
      border-radius: 999px;
    }
    .grid{
      display:grid;
      grid-template-columns: 1.25fr .9fr;
      gap:16px;
      align-items:start;
    }
    @media (max-width: 980px){
      .grid{ grid-template-columns: 1fr; }
    }

    .card{
      border:1px solid rgba(255,255,255,.08);
      background: rgba(17,27,51,.66);
      backdrop-filter: blur(10px);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    .card-h{
      padding: 14px 16px;
      border-bottom:1px solid rgba(255,255,255,.08);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
    }
    .card-h .title{
      font-size: 13px;
      color: #dbe6ff;
      display:flex; align-items:center; gap:8px;
    }
    .badge{
      font-size:11px;
      padding: 5px 8px;
      border-radius: 999px;
      border:1px solid rgba(255,255,255,.10);
      color: var(--muted);
      background: rgba(15,23,42,.6);
      white-space: nowrap;
    }
    .card-b{ padding: 14px 16px 16px; }

    label{
      display:block;
      margin-top: 12px;
      font-size: 12px;
      color:#cbd7ff;
    }
    .hint{
      margin-top:6px;
      font-size: 11px;
      color: var(--muted);
      line-height:1.35;
    }
    input[type="text"], input[type="number"], textarea, select{
      width:100%;
      margin-top: 7px;
      padding: 10px 11px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,.10);
      background: rgba(15,23,42,.55);
      color: var(--text);
      outline: none;
    }
    textarea{
      min-height: 200px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 12px;
      line-height:1.4;
    }
    input::placeholder, textarea::placeholder{ color: rgba(147,164,199,.7); }

    .row{ display:flex; gap:12px; flex-wrap:wrap; align-items:center; }
    .col{ flex:1; min-width: 200px; }
    .row.compact label{ margin-top:0; }
    .row.compact{ margin-top: 10px; }

    .toggle{
      display:flex; gap:8px; align-items:center;
      padding: 8px 10px;
      border-radius: 12px;
      border:1px solid rgba(255,255,255,.10);
      background: rgba(15,23,42,.45);
      cursor:pointer;
      user-select:none;
      font-size: 12px;
      color:#dbe6ff;
    }
    .toggle input{ width:auto; margin:0; }

    .btns{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      margin-top:14px;
    }

    button{
      padding:10px 14px;
      border-radius:12px;
      border:1px solid transparent;
      background:#2563eb;          /* default = primary */
      color:#ffffff;
      cursor:pointer;
      font-size:13px;
      font-weight:700;
      letter-spacing:.2px;
      transition: background-color .12s ease, opacity .12s ease;
    }

    button:hover{ opacity:.92; }
    button:disabled{ opacity:.5; cursor:not-allowed; }

    /* === semantic colors (flat) === */

    button.primary{
      background:#2563eb;          /* blue-600 */
    }

    button.info{
      background:#0891b2;          /* cyan-600 */
    }

    button.warn{
      background:#f59e0b;          /* amber-500 */
      color:#111827;               /* 노랑 위 가독성 보강 */
    }

    button.danger{
      background:#dc2626;          /* red-600 */
    }

    /* secondary: 중립/보조 (색 없는 버튼) */
    button.secondary{
      background:transparent;
      color:var(--text);
      border-color:var(--line);
    }
    button.secondary:hover{
      background:rgba(0,0,0,.04);
    }

    /* 다크 테마 보정 */
    html[data-theme="dark"] button.secondary:hover{
      background:rgba(255,255,255,.06);
    }

    .summary{
      display:grid;
      grid-template-columns: repeat(2, minmax(0,1fr));
      gap:12px;
      margin-top: 12px;
    }
    .kpi{
      padding: 12px;
      border-radius: 14px;
      border:1px solid rgba(255,255,255,.08);
      background: rgba(15,23,42,.45);
    }
    .kpi .k{ font-size: 11px; color: var(--muted); }
    .kpi .v{ font-size: 16px; margin-top:6px; color:#e9eefc; font-weight:700; }
    .progress{
      margin-top: 10px;
      height: 10px;
      border-radius: 999px;
      background: rgba(255,255,255,.08);
      overflow:hidden;
      border:1px solid rgba(255,255,255,.06);
    }
    .bar{ height:100%; width:0%; background: linear-gradient(90deg, rgba(45,212,191,.95), rgba(79,124,255,.95)); }

    pre{
      margin:0;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .statusbox{
      font-size: 12px;
      color:#dbe6ff;
      padding: 12px;
      border-radius: 14px;
      border:1px solid rgba(255,255,255,.08);
      background: rgba(15,23,42,.45);
      line-height:1.45;
      white-space: pre-wrap;
    }

    .status_ok { border-color: rgba(34,197,94,.35); }
    .status_warn { border-color: rgba(245,158,11,.35); }
    .status_err { border-color: rgba(239,68,68,.35); }

    .logs{
      height: 460px;
      overflow:auto;
      background: rgba(5,9,20,.75);
      border:1px solid rgba(255,255,255,.08);
      border-radius: var(--radius);
      padding: 12px;
      color:#e5e7eb;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 12px;
      line-height:1.35;
    }

    .muted{ color: var(--muted); }
    .split{
      display:flex; align-items:center; justify-content:space-between; gap:10px;
      margin-top: 10px;
    }
    .right{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; justify-content:flex-end; }

    /* =========================
      Form controls (theme-safe)
      ========================= */
    input[type="text"],
    input[type="number"],
    textarea,
    select {
      background: var(--panel);
      color: var(--text);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 10px;
      outline: none;
    }

    input[type="text"]::placeholder,
    input[type="number"]::placeholder,
    textarea::placeholder {
      color: color-mix(in srgb, var(--muted) 80%, transparent);
    }

    /* 라이트 모드에서 특히 textarea/input이 어둡게 나오는 문제 방지 */
    html[data-theme="light"] input[type="text"],
    html[data-theme="light"] input[type="number"],
    html[data-theme="light"] textarea,
    html[data-theme="light"] select {
      background: #ffffff;
      color: #0b1220;
      border-color: var(--line);
    }

    /* textarea 기본 높이 */
    textarea {
      min-height: 220px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }

    /* =========================
      Switch UI
      ========================= */
    .switch{
      display:flex;
      align-items:center;
      gap:12px;
    }

    .switch .meta{
      display:flex;
      flex-direction:column;
      line-height:1.1;
    }
    .switch .meta .title{
      font-size:12px;
      color: var(--muted);
    }
    .switch .meta .value{
      font-size:13px;
      font-weight:700;
      color: var(--text);
    }

    /* toggle */
    .switchWrap{
      position:relative;
      display:inline-flex;
      align-items:center;
    }

    .switchWrap input{
      position:absolute;
      opacity:0;
      pointer-events:none;
    }

    /* =========================
      Switch UI (BRIGHT VERSION)
      ========================= */

    .switch .toggle{
      position:relative;
      width:54px;
      height:30px;
      border-radius:999px;

      /* OFF 상태 */
      background: #E5EAF3;
      border:1px solid #CBD5E1;

      cursor:pointer;
      transition: background .25s ease, border-color .25s ease;
    }

    /* knob */
    .switch .toggle::after{
      content:"";
      position:absolute;
      top:50%;
      left:4px;
      width:22px;
      height:22px;
      border-radius:999px;
      transform: translateY(-50%);
      background:#FFFFFF;
      box-shadow: 0 3px 8px rgba(0,0,0,.25);
      transition: left .22s ease;
    }

    /* ON (다크 모드) */
    #theme_toggle:checked + .toggle{
      background: #2DD4BF;
      border-color: #2DD4BF;
    }

    #theme_toggle:checked + .toggle::after{
      left:28px;
    }

    /* =========================
      Light mode fixes (override)
      ========================= */
    html[data-theme="light"] .card{
      background: rgba(255,255,255,.78);
      border: 1px solid rgba(12, 18, 32, .10);
      backdrop-filter: blur(10px);
    }

    html[data-theme="light"] .card-h{
      border-bottom: 1px solid rgba(12, 18, 32, .08);
    }

    html[data-theme="light"] .card-h .title{
      color: var(--text);
    }

    html[data-theme="light"] label{
      color: color-mix(in srgb, var(--text) 80%, var(--muted));
    }

    html[data-theme="light"] .badge{
      background: rgba(247,249,255,.9);
      border-color: rgba(12, 18, 32, .10);
      color: var(--muted);
    }

    html[data-theme="light"] .kpi,
    html[data-theme="light"] .statusbox{
      background: rgba(247,249,255,.9);
      border-color: rgba(12, 18, 32, .10);
      color: var(--text);
    }

    html[data-theme="light"] .kpi .v{
      color: var(--text);
    }

    html[data-theme="light"] .progress{
      background: rgba(12, 18, 32, .06);
      border-color: rgba(12, 18, 32, .08);
    }

    /* logs: 라이트에서는 너무 어두우면 가독성 떨어져서 살짝 밝힘 */
    html[data-theme="light"] .logs{
      background: rgba(247,249,255,.95);
      border-color: rgba(12, 18, 32, .10);
      color: #0b1220;
    }

    .collapseBox{
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid var(--line);
    }

    .collapseBox[hidden]{ display:none !important; }

    /* =========================
      Inline warnings / invalid UI
      ========================= */
    .warnline{
      margin-top: 8px;
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid rgba(245,158,11,.35);
      background: rgba(245,158,11,.10);
      color: color-mix(in srgb, var(--text) 85%, var(--warn));
      font-size: 12px;
      line-height: 1.35;
    }

    .is-invalid{
      border-color: rgba(239,68,68,.70) !important;
      box-shadow: 0 0 0 3px rgba(239,68,68,.18) !important;
    }

    /* textarea가 invalid일 때 배경도 살짝 */
    textarea.is-invalid{
      background: color-mix(in srgb, var(--panel) 88%, rgba(239,68,68,.10)) !important;
    }

    /* =========================
       Banner / Toast
       ========================= */
    .banner{
      position: sticky;
      top: 0;
      z-index: 50;
      margin: 0 auto 14px;
      max-width: 1100px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel);
      box-shadow: var(--shadow);
      padding: 12px 14px;
      display:flex;
      align-items:flex-start;
      gap:12px;
    }
    .banner__icon{
      width:28px; height:28px;
      border-radius: 10px;
      display:flex; align-items:center; justify-content:center;
      flex: 0 0 auto;
      border: 1px solid var(--line);
      background: rgba(245,158,11,.12);
    }
    .banner__body{ flex:1; min-width:0; }
    .banner__title{
      font-size: 12px;
      font-weight: 800;
      letter-spacing:.2px;
      margin-bottom: 2px;
    }
    .banner__msg{
      font-size: 12px;
      color: var(--muted);
      white-space: pre-wrap;
      line-height: 1.35;
    }
    .banner__close{
      flex: 0 0 auto;
      border: 1px solid var(--line);
      background: transparent;
      color: var(--muted);
      padding: 6px 10px;
      border-radius: 10px;
      cursor: pointer;
      font-weight: 700;
    }

    /* banner variants */
    .banner.is-warn{
      border-color: rgba(245,158,11,.40);
      background: color-mix(in srgb, var(--panel) 92%, rgba(245,158,11,.10));
    }
    .banner.is-warn .banner__icon{
      border-color: rgba(245,158,11,.45);
      background: rgba(245,158,11,.14);
    }
    .banner.is-err{
      border-color: rgba(239,68,68,.45);
      background: color-mix(in srgb, var(--panel) 92%, rgba(239,68,68,.10));
    }
    .banner.is-err .banner__icon{
      border-color: rgba(239,68,68,.55);
      background: rgba(239,68,68,.14);
    }
    .banner.is-ok{
      border-color: rgba(34,197,94,.35);
      background: color-mix(in srgb, var(--panel) 92%, rgba(34,197,94,.10));
    }
    .banner.is-ok .banner__icon{
      border-color: rgba(34,197,94,.45);
      background: rgba(34,197,94,.14);
    }

    /* Toast */
    .toast{
      position: fixed;
      right: 16px;
      bottom: 16px;
      z-index: 80;
      width: min(420px, calc(100vw - 32px));
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel);
      box-shadow: var(--shadow);
      padding: 12px 14px;
      display:flex;
      align-items:flex-start;
      gap:12px;
      transform: translateY(10px);
      opacity: 0;
      pointer-events: none;
      transition: opacity .18s ease, transform .18s ease;
    }
    .toast.show{
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
    .toast__icon{
      width:28px; height:28px;
      border-radius: 10px;
      display:flex; align-items:center; justify-content:center;
      flex: 0 0 auto;
      border: 1px solid var(--line);
      background: rgba(245,158,11,.12);
    }
    .toast__body{ flex:1; min-width:0; }
    .toast__title{
      font-size: 12px;
      font-weight: 800;
      margin-bottom: 2px;
    }
    .toast__msg{
      font-size: 12px;
      color: var(--muted);
      white-space: pre-wrap;
      line-height: 1.35;
    }

    .toast.is-warn{ border-color: rgba(245,158,11,.40); }
    .toast.is-warn .toast__icon{ border-color: rgba(245,158,11,.45); background: rgba(245,158,11,.14); }

    .toast.is-err{ border-color: rgba(239,68,68,.45); }
    .toast.is-err .toast__icon{ border-color: rgba(239,68,68,.55); background: rgba(239,68,68,.14); }

    .toast.is-ok{ border-color: rgba(34,197,94,.35); }
    .toast.is-ok .toast__icon{ border-color: rgba(34,197,94,.45); background: rgba(34,197,94,.14); }

    /* =========================
       Tooltip (hover help)
       ========================= */
    .tip{
      position: relative;
      display: inline-block;
      cursor: help;
      border-bottom: 1px dotted color-mix(in srgb, var(--muted) 70%, transparent);
      padding-bottom: 1px;
    }

    .tip::after{
      content: attr(data-tip);
      position: absolute;
      left: 0;
      top: calc(100% + 10px);
      width: max-content;
      max-width: min(380px, 70vw);

      background: rgba(15,23,42,.96);
      color: #e5e7eb;
      border: 1px solid rgba(255,255,255,.10);
      border-radius: 12px;
      padding: 10px 12px;
      box-shadow: 0 12px 28px rgba(0,0,0,.35);

      font-size: 12px;
      line-height: 1.35;
      white-space: pre-wrap;

      opacity: 0;
      transform: translateY(-2px);
      pointer-events: none;
      transition: opacity .12s ease, transform .12s ease;
      z-index: 1000;
    }

    .tip:hover::after{
      opacity: 1;
      transform: translateY(0);
    }

    /* 라이트 모드에서 툴팁 가독성 보정 */
    html[data-theme="light"] .tip::after{
      background: rgba(255,255,255,.98);
      color: #0b1220;
      border-color: rgba(12,18,32,.14);
      box-shadow: 0 12px 28px rgba(12,18,32,.14);
    }

  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div class="brand">
        <div class="logo"></div>
        <div>
          <h1>Survey AutoRunner</h1>
          <div class="sub">ASP 로직 기반 케이스(분기) 추출 + Playwright 자동 응답 실행</div>
        </div>
      </div>
      <div class="pillrow">
        <!--
        <div class="pill">접속: <span class="muted">http://내부IP:8013</span></div>
        <div class="pill">로그: <span class="muted">관리자=run_all.log / 사용자=IP별 run.log</span></div>
        -->
        <div class="pill">
          <div class="switch">
            <div class="meta">
              <div class="title">테마</div>
              <div class="value" id="theme_value">자동</div>
            </div>

            <label class="switchWrap" title="다크/라이트 전환">
              <input id="theme_toggle" type="checkbox" />
              <span class="toggle" aria-hidden="true"></span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <div class="grid">
      <!-- Left: Controls -->
      <div class="card">
        <div class="card-h">
          <div class="title">⚙️ 실행 설정</div>
          <div class="badge" id="badge_mode">모드: -</div>
        </div>
        <div class="card-b">
          <label>테스트 URL (설문 시작 주소)</label>
          <input id="test_url" type="text" placeholder="예: https://.../index.asp?ResType=TEST"/>
          <div class="hint">브라우저에서 실제로 설문이 시작되는 URL을 붙여 넣으세요.</div>

          <div class="row">
            <div class="col">
              <label>반복 실행 횟수 (Random 모드)</label>
              <input id="repeat" type="number" min="1" max="500" value="1"/>
              <div class="hint">Coverage 모드에서는 “남은 케이스 수”에 따라 자동 계산될 수 있습니다.</div>
            </div>
            <div class="col" style="display:none;">
              <label>출력 폴더 (로그/스냅샷 저장)</label>
              <input id="out_dir" type="text" value="run_logs_pw"/>
              <div class="hint">IP별로 clients/&lt;ip&gt;/... 하위에 저장됩니다.</div>
            </div>
          </div>

          <div class="row">
            <div class="col">
              <label>동시 실행 수</label>
              <input id="concurrency" type="number" min="1" max="10" value="5"/>
              <div class="hint">최소 1개, 최대 10개까지 입력 가능합니다. 기본값은 5입니다.</div>
            </div>
            <div class="col" style="display:none;">
              <label>실행 타임아웃 (초)</label>
              <input id="execution_timeout_sec" type="number" min="1" value="3600"/>
              <div class="hint">응답 1건 기준 최대 실행 시간입니다. 기본값은 600초입니다.</div>
            </div>
          </div>

          <label>실행 모드</label>
          <div class="row compact">
            <label class="toggle"><input type="radio" name="mode" id="mode_random" checked/> 랜덤 자동응답 (Random)</label>
            <label class="toggle"><input type="radio" name="mode" id="mode_coverage"/> 로직 기반 케이스 실행 (Coverage)</label>
          </div>
          <div class="hint">
            - <span class="tip" data-tip="Random 모드: 화면의 DOM(입력 요소)을 직접 읽어
무작위로 선택/입력 후 다음으로 진행합니다.">Random</span>:
              화면 DOM을 보고 무작위로 선택/입력 후 다음으로 진행<br/>
            - <span class="tip" data-tip="Coverage 모드: ASP 로직(If/Else 분기)에서 가능한 케이스를 추출해
각 케이스를 강제로 적용하며 반복 실행합니다.">Coverage</span>:
              ASP 로직에서 케이스를 추출해
              <span class="tip" data-tip="case_overrides: 특정 입력값을 '강제로' 지정하는 규칙 묶음입니다.
Coverage 모드에서 케이스별로 어떤 값이 선택/입력되어야 하는지 정의합니다."><b>case_overrides</b></span>로
              강제값을 주며 반복 실행
          </div>
          <label>
            <span class="tip" data-tip="설문 Classic ASP 로직(If/ElseIf/End If)을 붙여넣는 영역입니다.
Coverage 모드에서는 케이스(분기 조합) 추출에 필수이고,
Random 모드에서도 특정 화면으로 빠지는 것을 피하는 가드로 활용할 수 있어요.">ASP Logic</span>
            (Coverage용 / Random에서도
            <span class="tip" data-tip="SCREEN 회피: 특정 차단/에러/종료 화면(SCREEN)으로 빠지는 분기를
미리 피하도록 강제하는 규칙을 의미합니다.">SCREEN 회피</span>
            용도로 사용 가능)
          </label>
          <textarea id="asp_logic"></textarea>
          <div id="asp_logic_warn" class="warnline" hidden>
            ⚠️ Coverage 모드에서는 ASP Logic이 필수입니다. ASP 로직을 붙여 넣어 주세요.
          </div>

          <div id="asp_logic_format_warn" class="warnline" hidden>
            ⛔ Asp Logic 형식이 올바르지 않습니다. If/ElseIf/End If 구조, 괄호/따옴표를 확인하고 다시 붙여 넣어 주세요.
          </div>

          <div id="asp_logic_ok" class="warnline" hidden
              style="
                border-color: rgba(34,197,94,.45);
                background: rgba(34,197,94,.12);
                color: color-mix(in srgb, var(--text) 85%, var(--ok));
              ">
            ✅ ASP Logic 확인 결과, 실행 가능한 케이스가 발견되었습니다.
          </div>

          <div class="hint">Coverage 모드에서는 분기 케이스를 추출해 실행합니다.</div>

          <!-- ✅ Coverage options wrapper -->
          <div id="coverage_opts" class="collapseBox" hidden>
            <!-- Tie-break -->
            <label>
              <span class="tip" data-tip="Coverage 모드에서 여러 케이스가 남아있을 때,
어떤 순서로 케이스를 선택할지 정하는 방식입니다.">타이브레이크</span> 방식
            </label>
            <div class="row compact">
              <label class="toggle">
                <input type="radio" name="tie_break" id="tie_stable" checked/>
                <span class="tip" data-tip="항상 같은 순서로 케이스를 실행합니다.
재현/디버깅에 유리합니다.">안정(Stable)</span>
              </label>
              <label class="toggle">
                <input type="radio" name="tie_break" id="tie_random"/>
                <span class="tip" data-tip="남은 케이스 중 무작위로 골라 실행합니다.
커버리지를 넓게 찍는 데 유리합니다.">무작위(Random)</span>
              </label>
            </div>

            <label>
              <span class="tip" data-tip="ASP 로직에서 추출할 케이스의 최대 개수입니다.
너무 크게 잡으면 계획/실행이 오래 걸릴 수 있어요.">최대 케이스 수</span> (Coverage)
            </label>
            <input id="max_cases" type="number" min="1" max="200" value="50"/>

            <label>
              <span class="tip" data-tip="Coverage 실행 동작을 제어하는 옵션들입니다.">Coverage 옵션</span>
            </label>
            <div class="row compact">
              <label class="toggle">
                <input id="auto_until_done" type="checkbox" checked/>
                <span class="tip" data-tip="남은 케이스를 가능한 끝까지 자동으로 실행합니다.
(단, 아래 '최대 총 실행 횟수'로 안전 제한)">자동으로 케이스 끝까지 실행</span>
              </label>
              <label class="toggle">
                <input id="persist_state" type="checkbox" checked/>
                <span class="tip" data-tip="실행 완료(done) / 실패(bad)한 케이스 상태를 파일로 저장합니다.
서버 재시작 후에도 이어서 실행할 수 있어요.">상태 저장(재시작 이어서)</span>
              </label>
              <label class="toggle">
                <input id="include_default_paths" type="checkbox" checked/>
                <span class="tip" data-tip="If 조건이 '거짓'일 때 타는 경로도 케이스로 포함합니다.
분기 누락을 줄이지만 케이스 수가 늘어날 수 있어요.">기본 경로(조건 거짓) 케이스 생성</span>
              </label>
              <label class="toggle">
                <input id="include_screen_cases" type="checkbox"/>
                <span class="tip" data-tip="NEXTPAGE=SCREEN 으로 가는 분기도 케이스로 포함합니다.
기본적으로는 제외되며, 체크하면 SCREEN 종료 케이스도 coverage에 포함됩니다.">SCREEN 케이스 포함</span>
              </label>
            </div>

            <div class="row">
              <div class="col">
                <label>
                  <span class="tip" data-tip="자동 실행이 너무 많이 돌지 않도록 거는 상한선입니다.
케이스가 많아도 이 값 이상은 실행하지 않습니다.">최대 총 실행 횟수(안전 제한)</span>
                </label>
                <input id="max_total_runs" type="number" min="1" max="5000" value="200"/>
              </div>
            </div>
          </div>

          <label>입력/선택 옵션</label>
          <div class="row compact">
            <label class="toggle"><input id="headless" type="checkbox"/> 창 숨김</label>
            <label class="toggle"><input id="select_all" type="checkbox" checked/> 체크박스 전체 선택</label>
            <label class="toggle"><input id="rank_select_all" type="checkbox" checked/> 순위 전체 선택</label>
          </div>

          <div class="row">
            <div class="col">
              <div class="hint">체크박스 최소/최대는 문항 hidden(MIQxCNT/MQxCNT) 기준으로 자동 적용됩니다.</div>
            </div>
          </div>


          <label style="display:none; margin-bottom:6px;">
            스탑 페이지(예: SQ3, SQ3.asp):
            <input id="stop_at_page" type="text" style="width:220px; margin-left:8px;">
          </label>

            <!--
            <label style="display:block; margin-bottom:6px;">
              Hold max seconds (optional, blank = infinite):
              <input id="stop_hold_max_seconds" type="number" min="1" step="1" placeholder="" style="width:120px; margin-left:8px;">
            </label>
            -->

          <div class="row">
            <div class="col">
              <label>워딩 검증용 문서 (HWPX, DOCX)</label>
              <input type="file" id="ref_doc" accept=".hwpx,.docx" style="margin-top: 6px;"/>
              <div class="hint">첨부 시 더미 응답 중 페이지 텍스트와 비교하여 검증합니다.</div>
            </div>
          </div>
          
          <div class="btns">
            <button id="btn_plan" class="info">계획 확인(몇 번 실행?)</button>
            <button id="btn_run" class="primary">실행(Run)</button>
            <button id="btn_stop" class="danger">중지(Stop)</button>
            <button id="btn_reset" class="warn">상태 초기화(Reset)</button>
            <button id="btn_latest_failure" class="secondary">최근 실패 HTML 보기</button>
            <button id="btn_wording_report" class="secondary">워딩 리포트 보기</button>
          </div>

          <div class="hint">
            ⚠️ Reset은 coverage 상태(done/bad)를 초기화합니다. (IP + 로직 해시 기준)
          </div>
        </div>
      </div>

      <!-- Right: Status -->
      <div class="card">
        <div class="card-h">
          <div class="title">📊 상태 / 진행</div>
          <div class="badge" id="badge_run">상태: -</div>
        </div>
        <div class="card-b">
          <div class="summary">
            <div class="kpi">
              <div class="k">모드</div>
              <div class="v" id="k_mode">-</div>
            </div>
            <div class="kpi">
              <div class="k">진행</div>
              <div class="v" id="k_progress">-</div>
              <div class="progress"><div class="bar" id="k_bar"></div></div>
            </div>
            <div class="kpi">
              <div class="k">예정 실행 횟수</div>
              <div class="v" id="k_planned">-</div>
            </div>
            <div class="kpi">
              <div class="k">남은 케이스(Coverage)</div>
              <div class="v" id="k_remaining">-</div>
            </div>
          </div>

          <div class="split">
            <div class="muted">상세 상태(JSON)</div>
            <div class="right">
              <label class="toggle"><input id="auto_scroll" type="checkbox" checked/> 로그 자동스크롤</label>
            </div>
          </div>

          <div class="statusbox" id="status_summary">-</div>
          <div style="height:10px;"></div>

          <div class="statusbox" id="status">-</div>
          <div style="height:12px;"></div>

          <div class="split">
            <div class="muted">계획 확인 결과(Plan)</div>
            <div class="right">
              <button id="btn_clear_plan" class="secondary" type="button">Plan 지우기</button>
            </div>
          </div>

          <div class="statusbox" id="plan_box">(plan not run)</div>
        </div>
      </div>
    </div>

    <!-- Logs -->
    <div style="height:16px;"></div>
    <div class="card">
      <div class="card-h">
        <div class="title">🧾 로그</div>
        <div class="badge">최근 300줄</div>
      </div>
      <div class="card-b">
        <pre id="logs" class="logs"></pre>
      </div>
    </div>
  </div>

  <!-- ✅ Global Banner -->
  <div id="banner" class="banner" hidden>
    <div class="banner__icon" id="banner_icon">⚠️</div>
    <div class="banner__body">
      <div class="banner__title" id="banner_title">알림</div>
      <div class="banner__msg" id="banner_msg">-</div>
    </div>
    <button id="banner_close" class="banner__close" type="button" aria-label="close">✕</button>
  </div>

  <!-- ✅ Toast -->
  <div id="toast" class="toast" hidden>
    <div class="toast__icon" id="toast_icon">⚠️</div>
    <div class="toast__body">
      <div class="toast__title" id="toast_title">알림</div>
      <div class="toast__msg" id="toast_msg">-</div>
    </div>
  </div>

<script>
function $(id){ return document.getElementById(id); }

let toastTimer = null;

function clearBanner(){
  const b = $("banner");
  if(!b) return;
  b.hidden = true;
  b.classList.remove("is-warn","is-err","is-ok");
}

function showBanner(kind, title, msg){
  const b = $("banner");
  if(!b) return;

  b.hidden = false;
  b.classList.remove("is-warn","is-err","is-ok");
  b.classList.add(kind === "err" ? "is-err" : (kind === "ok" ? "is-ok" : "is-warn"));

  $("banner_title").textContent = title || "알림";
  $("banner_msg").textContent = msg || "-";

  const icon = (kind === "err") ? "⛔" : (kind === "ok" ? "✅" : "⚠️");
  $("banner_icon").textContent = icon;
}

function clearToast(){
  const t = $("toast");
  if(!t) return;
  t.hidden = true;
  t.classList.remove("show","is-warn","is-err","is-ok");
  if(toastTimer){ clearTimeout(toastTimer); toastTimer = null; }
}

function showToast(kind, title, msg, ms){
  const t = $("toast");
  if(!t) return;

  // reset
  t.hidden = false;
  t.classList.remove("is-warn","is-err","is-ok");
  t.classList.add(kind === "err" ? "is-err" : (kind === "ok" ? "is-ok" : "is-warn"));

  $("toast_title").textContent = title || "알림";
  $("toast_msg").textContent = msg || "-";
  $("toast_icon").textContent = (kind === "err") ? "⛔" : (kind === "ok" ? "✅" : "⚠️");

  // animate in
  requestAnimationFrame(()=> t.classList.add("show"));

  // auto dismiss
  if(toastTimer){ clearTimeout(toastTimer); toastTimer = null; }
  toastTimer = setTimeout(()=>{
    t.classList.remove("show");
    setTimeout(()=>{ t.hidden = true; }, 200);
  }, (typeof ms === "number" ? ms : 5000));
}

function serverOfflineMessage(){
  return "서버에 연결할 수 없습니다. 서버가 종료되었거나 아직 실행되지 않았을 수 있습니다. BAT 파일을 먼저 실행한 뒤 다시 시도해 주세요.";
}

function friendlyErrorText(err){
  try{
    const raw = (err && err.message) ? String(err.message) : String(err || "");
    try{
      const j = JSON.parse(raw);
      if(typeof j?.detail === "string" && j.detail.trim()){
        return j.detail.trim();
      }
    }catch(_){}
    return raw || "요청 처리 중 오류가 발생했습니다.";
  }catch(_){
    return "요청 처리 중 오류가 발생했습니다.";
  }
}

async function safeFetch(url, options){
  try{
    const r = await fetch(url, options);
    if(!r.ok){
      throw new Error(await r.text());
    }
    return r;
  }catch(e){
    const msg = String((e && e.message) || e || "");
    if(e instanceof TypeError || msg.includes("Failed to fetch")){
      throw new Error(JSON.stringify({
        detail: serverOfflineMessage(),
        offline: true
      }));
    }
    throw e;
  }
}

async function apiGetText(url){
  const r = await safeFetch(url);
  return await r.text();
}
async function apiGetJson(url){
  const r = await safeFetch(url);
  return await r.json();
}
async function apiPostJson(url, body){
  const r = await safeFetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(body)
  });
  return await r.json();
}

function payload(){
  const isCoverage = $("mode_coverage").checked;

  // ✅ breakpoint 입력값: payload() 안에서 읽어서 return에 포함
  const stopAtPage = ($("stop_at_page")?.value || "").trim();
  // stop_hold_max_seconds는 UI에서 제거됨 → 항상 null

  return {
    mode: isCoverage ? "coverage" : "random",
    tie_break: isCoverage ? ($("tie_random").checked ? "random" : "stable") : "stable",

    asp_logic: ($("asp_logic").value || ""),
    max_cases: isCoverage ? parseInt($("max_cases").value||"20",10) : 0,

    include_default_paths: isCoverage ? $("include_default_paths").checked : false,
    include_screen_cases: isCoverage ? $("include_screen_cases").checked : false,
    auto_until_done: isCoverage ? $("auto_until_done").checked : false,
    persist_state: isCoverage ? $("persist_state").checked : false,
    max_total_runs: isCoverage ? parseInt($("max_total_runs").value||"200",10) : 0,

    test_url: $("test_url").value.trim(),
    repeat: parseInt($("repeat").value||"1",10),
    headless: $("headless").checked,
    out_dir: $("out_dir").value.trim() || "run_logs_pw",
    concurrency: parseInt($("concurrency").value||"5",10),
    execution_timeout_sec: parseInt($("execution_timeout_sec").value||"3600",10),
    checkbox_select_all: $("select_all").checked,
    rank_select_all: $("rank_select_all").checked,

    // ✅ ADD
    stop_at_page: stopAtPage || null,
    stop_hold_max_seconds: null,
    ref_doc_path: window._uploadedDocPath || null
  };
}

function validateBeforePlanOrRun(){
  const isCoverage = $("mode_coverage").checked;

  const testUrl = ($("test_url").value || "").trim();
  const aspLogic = ($("asp_logic").value || "").trim();

  // 1) URL은 항상 필요
  if(!testUrl){
    alert("테스트 URL이 비어 있습니다.");
    $("test_url").focus();
    return false;
  }

  // 2) ✅ Coverage면 ASP Logic 필수
  if(isCoverage && !aspLogic){
    alert("Coverage 모드에서는 ASP Logic이 비어 있을 수 없습니다.\n\nASP 로직을 붙여 넣고 다시 실행해 주세요.");
    $("asp_logic").focus();
    return false;
  }

  return true;
}
function setAspLogicInvalidUI(on){
  const ta = $("asp_logic");
  const warn = $("asp_logic_warn");
  if(!ta || !warn) return;

  if(on){
    ta.classList.add("is-invalid");
    warn.hidden = false;
  }else{
    ta.classList.remove("is-invalid");
    warn.hidden = true;
  }
}

function setAspLogicFormatInvalidUI(on){
  const ta = $("asp_logic");
  const warn = $("asp_logic_format_warn");
  if(!ta || !warn) return;

  if(on){
    ta.classList.add("is-invalid");
    warn.hidden = false;
  }else{
    warn.hidden = true;
    // ⚠️ 빈칸 invalid은 setAspLogicInvalidUI가 담당하므로 여기서 무조건 remove하지 않음
    // (둘 다 켜져 있을 수 있음)
  }
}

function setAspLogicOkUI(on, count){
  const ok = $("asp_logic_ok");
  const ta = $("asp_logic");
  if(!ok || !ta) return;

  if(on){
    ok.hidden = false;
    ok.textContent =
      `✅ ASP Logic 확인 결과, 실행 가능한 케이스 ${count}개가 발견되었습니다.`;
    // 정상일 땐 빨간 테두리 제거
    ta.classList.remove("is-invalid");
  }else{
    ok.hidden = true;
  }
}

function updateRunPlanEnabled(){
  const isCoverage = $("mode_coverage").checked;

  const testUrl = ($("test_url").value || "").trim();
  const aspLogic = ($("asp_logic").value || "").trim();

  // 기본: URL 없으면 어차피 의미 없으니 Run/Plan 막기
  const urlOk = !!testUrl;

  // Coverage일 때만 asp_logic 필수
  const aspOk = (!isCoverage) ? true : !!aspLogic;

  // UI 표시
  setAspLogicInvalidUI(isCoverage && !aspOk);

  // 빈칸이 해결되면 형식 경고도 같이 내려줌(사용자가 다시 입력했을 때)
  if(isCoverage && aspOk){
    setAspLogicFormatInvalidUI(false);
    // 입력이 바뀌면 이전 OK 결과는 무효
    setAspLogicOkUI(false);
  }

  // 버튼 상태
  const canGo = urlOk && aspOk;

  const btnPlan = $("btn_plan");
  const btnRun = $("btn_run");
  if(btnPlan) btnPlan.disabled = !canGo;
  if(btnRun) btnRun.disabled = !canGo;

  // ✅ 사용자가 입력을 바로잡으면 배너는 자동으로 내려줌(다시 Run/Plan에서 재검증)
  if(canGo) clearBanner();
  if(canGo) clearUxSummary();
}

// localStorage: 입력값 저장/복구
const LS_KEY = "autorunner_ui_v1";

// =========================
// Theme (default: dark, with Auto(OS) option)
// =========================
const THEME_KEY = "autorunner_theme_v2";
const THEME_MODE_KEY = "autorunner_theme_mode_v2"; // "auto" | "manual"

let mql = null;

function osPrefTheme(){
  try{
    if(!mql) mql = window.matchMedia("(prefers-color-scheme: dark)");
    return mql.matches ? "dark" : "light";
  }catch(e){
    return "dark";
  }
}

function setThemeValueLabel(theme){
  const el = $("theme_value");
  if(el) el.textContent = (theme === "dark") ? "다크" : "라이트";
}

function applyTheme(theme){
  document.documentElement.setAttribute("data-theme", theme);
  setThemeValueLabel(theme);

  const t = $("theme_toggle");
  if(t) t.checked = (theme === "dark");
}

function setModeUI(mode){
  const modeSel = $("theme_mode");
  const t = $("theme_toggle");
  const toggleSpan = document.querySelector(".switch .toggle");

  if(modeSel) modeSel.value = mode;

  const manual = (mode === "manual");

  // 수동이 아니면 토글 비활성화 + 흐리게
  if(t){
    t.disabled = !manual;
  }
  if(toggleSpan){
    toggleSpan.style.opacity = manual ? "1" : ".45";
    toggleSpan.style.cursor = manual ? "pointer" : "not-allowed";
  }
}

function loadTheme(){
  const savedMode = localStorage.getItem(THEME_MODE_KEY) || "manual";
  const mode = (savedMode === "auto") ? "auto" : "manual";
  setModeUI(mode);

  if(mode === "auto"){
    const theme = osPrefTheme();
    applyTheme(theme);
  }else{
    // ✅ 기본은 다크. 저장값이 있으면 저장값 사용
    const savedTheme = localStorage.getItem(THEME_KEY);
    applyTheme(savedTheme === "light" ? "light" : "dark");
  }
}

function saveTheme(theme){
  try{ localStorage.setItem(THEME_KEY, theme); }catch(e){}
}
function saveMode(mode){
  try{ localStorage.setItem(THEME_MODE_KEY, mode); }catch(e){}
}

function startWatchOSTheme(){
  try{
    if(!mql) mql = window.matchMedia("(prefers-color-scheme: dark)");
    // Safari 구버전 대응
    const handler = () => {
      const mode = localStorage.getItem(THEME_MODE_KEY) || "manual";
      if(mode === "auto"){
        applyTheme(osPrefTheme());
      }
    };
    if(mql.addEventListener) mql.addEventListener("change", handler);
    else if(mql.addListener) mql.addListener(handler);
  }catch(e){}
}

function saveForm(){
  try{ localStorage.setItem(LS_KEY, JSON.stringify(payload())); }catch(e){}
}
function loadForm(){
  try{
    const raw = localStorage.getItem(LS_KEY);
    if(!raw) return;
    const p = JSON.parse(raw);

    if(p.mode === "coverage"){ $("mode_coverage").checked = true; } else { $("mode_random").checked = true; }
    if(p.tie_break === "random"){ $("tie_random").checked = true; } else { $("tie_stable").checked = true; }

    $("asp_logic").value = p.asp_logic || "";
    $("max_cases").value = p.max_cases ?? 50;

    $("include_default_paths").checked = !!p.include_default_paths;
    $("include_screen_cases").checked = !!p.include_screen_cases;
    $("auto_until_done").checked = !!p.auto_until_done;
    $("persist_state").checked = !!p.persist_state;
    $("max_total_runs").value = p.max_total_runs ?? 200;

    $("test_url").value = p.test_url || "";
    $("repeat").value = p.repeat ?? 1;
    $("headless").checked = !!p.headless;
    $("out_dir").value = p.out_dir || "run_logs_pw";
    $("concurrency").value = p.concurrency ?? 5;
    $("execution_timeout_sec").value = p.execution_timeout_sec ?? 3600;

    $("select_all").checked = !!p.checkbox_select_all;
    if($("rank_select_all")) $("rank_select_all").checked = !!p.rank_select_all;
    if($("stop_at_page")) $("stop_at_page").value = p.stop_at_page || "";
  }catch(e){}
}

function setBadges(st){
  const mode = st?.mode || (payload().mode);
  $("badge_mode").textContent = "모드: " + mode.toUpperCase();
  $("badge_run").textContent = "상태: " + (st?.running ? "실행 중" : "대기");
}

function setKpis(st){
  const mode = st?.mode ?? "-";
  const planned = st?.planned_total ?? "-";
  const cur = st?.current_run ?? 0;
  const remain = st?.remaining_cases ?? "-";

  $("k_mode").textContent = mode;
  $("k_planned").textContent = planned;
  $("k_remaining").textContent = remain;

  let pct = 0;
  if(typeof planned === "number" && planned > 0){
    pct = Math.min(100, Math.round((cur / planned) * 100));
  }
  $("k_progress").textContent = `${cur} / ${planned} (${pct}%)`;
  $("k_bar").style.width = pct + "%";
}

function setStatusSummary(st){
  const el = $("status_summary");
  if(!el) return;

  const running = !!st?.running;
  const mode = (st?.mode || "-").toUpperCase();
  const cur = (typeof st?.current_run === "number") ? st.current_run : 0;
  const planned = (typeof st?.planned_total === "number") ? st.planned_total : 0;

  const err = st?.error || "";
  const ok = st?.ok;

  // 기본 문구
  let line1 = `상태: ${running ? "실행 중" : "대기"}  |  모드: ${mode}  |  진행: ${cur}/${planned}`;
  let line2 = "";

  // 상태 분류
  el.classList.remove("status_ok","status_warn","status_err");

  if(running){
    el.classList.add("status_warn");
    line2 = "실행 중입니다.";
  }else{
    // 실행 중이 아닐 때
    if(err){
      if(err === "창닫음"){
        el.classList.add("status_warn");
        line2 = "중단 사유: 창닫음 (사용자가 설문 창을 닫음)";
      }else{
        el.classList.add("status_err");
        line2 = `오류: ${err}`;
      }
    }else if(ok === true){
      el.classList.add("status_ok");
      line2 = "완료: 정상 종료";
    }else if(ok === false){
      el.classList.add("status_err");
      line2 = "완료: 실패 종료";
    }else{
      // ok가 None이고 err도 없으면 그냥 대기
      el.classList.add("status_ok");
      line2 = "대기 중";
    }
  }

  el.textContent = `${line1}\n${line2}`;

  // ✅ UX summary persist: 의미있는 오류/경고만 저장
  // - "대기 중" / 정상 완료 같은 기본 상태는 저장하지 않음
  const shouldPersist =
    (!running) && !!err && (err !== "창닫음"); // 필요하면 조건 더 조정 가능

  if(shouldPersist){
    saveUxSummary({
      // 서버 status랑 섞이지 않게 "ux" 플래그
      _ux: true,
      ts: Date.now(),
      // 표시용 최소 필드
      running: false,
      mode: (st?.mode || payload().mode),
      planned_total: (typeof st?.planned_total === "number" ? st.planned_total : 0),
      current_run: (typeof st?.current_run === "number" ? st.current_run : 0),
      remaining_cases: (typeof st?.remaining_cases === "number" ? st.remaining_cases : 0),
      ok: st?.ok,
      error: err
    });
  }
}

const PLAN_LS_KEY = "autorunner_last_plan_v1";
const UX_LS_KEY = "autorunner_last_ux_v1";

function formatPlanText(plan){
  if(!plan || typeof plan !== "object") return "-";
  const lines = [];
  lines.push(`mode: ${plan.mode ?? "-"}`);
  lines.push(`planned_total: ${plan.planned_total ?? "-"}`);
  lines.push(`extracted_cases: ${plan.extracted_cases ?? "-"}`);
  lines.push(`remaining_cases: ${plan.remaining_cases ?? "-"}`);
  lines.push(`done_cases: ${plan.done_cases ?? "-"}`);
  lines.push(`bad_cases: ${plan.bad_cases ?? "-"}`);
  lines.push(`state_path: ${plan.state_path ?? "-"}`);
  // guards는 길 수 있어서 JSON 한 줄로
  if(plan.guards && Object.keys(plan.guards).length){
    lines.push(`guards: ${JSON.stringify(plan.guards)}`);
  }else{
    lines.push(`guards: {}`);
  }
  return lines.join("\n");
}

function saveUxSummary(obj){
  try{ localStorage.setItem(UX_LS_KEY, JSON.stringify(obj)); }catch(e){}
}

function loadUxSummary(){
  try{
    const raw = localStorage.getItem(UX_LS_KEY);
    if(!raw) return null;
    const j = JSON.parse(raw);
    if(!j || typeof j !== "object") return null;
    return j;
  }catch(e){
    return null;
  }
}

function clearUxSummary(){
  try{ localStorage.removeItem(UX_LS_KEY); }catch(e){}
}

function setPlanBox(plan){
  const el = $("plan_box");
  if(!el) return;
  el.textContent = formatPlanText(plan);

  // 저장 (새로고침해도 유지)
  try{ localStorage.setItem(PLAN_LS_KEY, JSON.stringify(plan)); }catch(e){}
}

function loadPlanBox(){
  const el = $("plan_box");
  if(!el) return;
  try{
    const raw = localStorage.getItem(PLAN_LS_KEY);
    if(!raw){ el.textContent = "-"; return; }
    const plan = JSON.parse(raw);
    el.textContent = formatPlanText(plan);
  }catch(e){
    el.textContent = "-";
  }
}

function clearPlanBox(){
  const el = $("plan_box");
  if(el) el.textContent = "-";
  try{ localStorage.removeItem(PLAN_LS_KEY); }catch(e){}
}

async function refresh(){
  saveForm();
  try{
    const st = await apiGetJson("/api/status");

    // ✅ 서버가 "의미 없는 idle"을 주는 경우(=사용자 안내를 유지해야 할 때)
    // - running=false
    // - error 없음
    // - ok 값도 없거나 null/undefined
    const isServerNeutralIdle =
      !st?.running && !st?.error && (!st?.ok || st?.planned_total === 0);

    if(isServerNeutralIdle){
      const ux = loadUxSummary();
      if(ux && ux._ux && ux.error){
        // status_summary에는 ux를 적용 (status JSON은 서버값 그대로 보여도 됨)
        setBadges({mode: ux.mode, running:false});
        setKpis({
          mode: ux.mode,
          planned_total: ux.planned_total ?? 0,
          current_run: ux.current_run ?? 0,
          remaining_cases: ux.remaining_cases ?? "-"
        });
        setStatusSummary(ux);
      }else{
        setBadges(st);
        setKpis(st);
        setStatusSummary(st);
      }
    }else{
      // 서버가 실제 에러/실행중/완료 상태면 서버 우선
      setBadges(st);
      setKpis(st);
      setStatusSummary(st);

      // ✅ 서버가 실제 상태를 갖고 있으면, UX 저장값은 필요 시 정리
      // (원하면: 완료(ok=true)면 클리어)
      if(st?.ok === true && !st?.running){
        clearUxSummary();
      }
    }

    $("status").textContent = JSON.stringify(st, null, 2);
  }catch(e){
    $("status").textContent = friendlyErrorText(e);
  }

  try{
    const outDir = $("out_dir").value.trim() || "run_logs_pw";
    const logs = await apiGetText("/api/logs?out_dir="+encodeURIComponent(outDir));
    $("logs").textContent = logs;

    if($("auto_scroll").checked){
      $("logs").scrollTop = $("logs").scrollHeight;
    }
  }catch(e){
    $("logs").textContent = friendlyErrorText(e);
  }
}

async function precheckCoverageOrWarn(){
  const isCoverage = $("mode_coverage").checked;
  if(!isCoverage) return true;

  const p = payload();

  // 사전 점검 시작 안내(토스트)
  showToast("warn", "Coverage 사전 점검", "케이스 추출(Plan)로 실행 가능 여부를 확인 중입니다…", 2500);

  let res;
  try{
    res = await apiPostJson("/api/plan", p);
  }catch(e){
    // plan에서 ASP Logic 형식 오류 등 -> 배너/토스트로 안내
    let detail = "";
    try{
      const j = JSON.parse(e.message);
      detail = (typeof j?.detail === "string") ? j.detail : "";
    }catch(_){}

    const msg = detail && detail.includes("ASP Logic")
      ? detail
      : "Coverage 사전 점검(Plan) 중 오류가 발생했습니다.";

    // ASP Logic 형식 오류면 textarea 빨간 강조 + 안내문구 표시
    const isAspFormatErr = (detail && detail.includes("ASP Logic"));
    if(isAspFormatErr){
      setAspLogicFormatInvalidUI(true);
      // 빈칸 경고는 별개이므로(빈칸이면 validateBeforePlanOrRun에서 이미 막힘)
      // 여기서는 형식 경고만 켬
      setAspLogicOkUI(false);
    }

    showBanner("err", "Coverage 실행 불가", msg);
    showToast("err", "실행 불가", msg, 6000);

    // 상태 요약에도 반영
    setStatusSummary({
      running:false, mode:"coverage", planned_total:0, current_run:0, remaining_cases:0,
      ok:false, error: msg
    });

    return false;
  }

  const plan = res?.plan || {};
  setPlanBox(plan);

  const extracted = Number(plan.extracted_cases ?? 0);
  const remaining = Number(plan.remaining_cases ?? 0);
  const planned = Number(plan.planned_total ?? 0);

  // ✅ 실행 가능
  if(extracted > 0 && remaining > 0 && planned > 0){
    clearBanner();

    // ❌ 오류 UI는 모두 내림
    setAspLogicFormatInvalidUI(false);
    setAspLogicInvalidUI(false);

    // ✅ 정상 케이스 발견 UI 표시
    setAspLogicOkUI(true, remaining);

    showToast(
      "ok",
      "ASP Logic 확인 완료",
      `실행 가능한 케이스 ${remaining}개가 발견되었습니다.`,
      2200
    );
    return true;
  }

  // ❌ 케이스 0개 차단
  const msg =
`Coverage 모드에서 실행 가능한 케이스가 없습니다.

- ASP Logic에서 If/ElseIf 분기 조건을 추출하지 못했습니다.
- ASP Logic 형식(If/End If, 괄호/따옴표)을 확인해 주세요.`;

  showBanner("warn", "Coverage 실행 불가", msg);
  // ✅ 케이스 0개도 "로직 형식/구조 문제" 가능성이 높아서 입력 박스 강조
  setAspLogicFormatInvalidUI(true);
  setAspLogicOkUI(false);
  showToast("warn", "실행 불가", "실행 가능한 케이스가 없습니다. ASP Logic을 확인해 주세요.", 6000);

  setStatusSummary({
    running:false, mode:"coverage", planned_total:0, current_run:0, remaining_cases:0,
    ok:false, error: "실행 가능한 케이스가 없습니다."
  });

  return false;
}

$("btn_plan").addEventListener("click", async ()=>{
  if(!validateBeforePlanOrRun()) return;
  // ✅ ADD: Coverage면 서버 plan으로 먼저 케이스 존재 여부 확인 후, 없으면 차단
  if(!(await precheckCoverageOrWarn())) return;
  try{
    const res = await apiPostJson("/api/plan", payload());
    // plan 결과를 KPI처럼 보여주기 위해 status를 status endpoint처럼 가공
    const plan = res?.plan || {};
    setPlanBox(plan);
    setBadges({mode: plan.mode, running:false});
    // ✅ ADD: Coverage 케이스 0개면 즉시 안내
    if((plan.mode === "coverage") && (Number(plan.planned_total ?? 0) <= 0 || Number(plan.remaining_cases ?? 0) <= 0)){
      alert("Coverage 모드에서 실행 가능한 케이스가 없습니다.\n\nASP Logic에서 분기 조건(If/ElseIf)을 추출하지 못했습니다.");
    }
    setKpis({
      mode: plan.mode,
      planned_total: plan.planned_total,
      current_run: 0,
      remaining_cases: plan.remaining_cases ?? "-"
    });
  }catch(e){
    // 1) validation 에러(test_url) 처리
    try{
      const j = JSON.parse(e.message);
      if(j.detail?.[0]?.loc?.includes("test_url")){
        alert("테스트 URL이 비어 있습니다.");
        return;
      }
    }catch{}

    // 2) ASP Logic 관련 오류
    try{
      const j = JSON.parse(e.message);
      if(typeof j.detail === "string" && j.detail.includes("ASP Logic")){
        alert(j.detail);
        return;
      }
    }catch(_){}

    // 3) ✅ 그 외(409 Already running 포함): 서버 detail을 그대로 보여주기
    try{
      const j = JSON.parse(e.message);
      if(typeof j.detail === "string" && j.detail.trim()){
        alert(j.detail);
        return;
      }
    }catch(_){}

    alert("요청 처리 중 오류가 발생했습니다.");
  }
});

$("btn_run").addEventListener("click", async ()=>{
  if(!validateBeforePlanOrRun()) return;

  // ✅ ADD: Coverage면 서버 plan으로 먼저 케이스 존재 여부 확인 후, 없으면 차단
  if(!(await precheckCoverageOrWarn())) return;

  // ✅ Upload Document if exists
  const fileInput = $("ref_doc");
  if (fileInput && fileInput.files.length > 0) {
    showToast("warn", "파일 업로드 중", "문서를 업로드하고 있습니다...", 2000);
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    try {
      const uploadRes = await fetch("/api/upload_doc", {
        method: "POST",
        body: formData
      });
      const uploadJson = await uploadRes.json();
      if (uploadJson.ok) {
        window._uploadedDocPath = uploadJson.path;
      } else {
        alert("문서 업로드 실패: " + uploadJson.detail);
        return;
      }
    } catch (e) {
      alert("문서 업로드 중 오류 발생");
      return;
    }
  } else {
    window._uploadedDocPath = null;
  }

  try{
    const res = await apiPostJson("/api/run", payload());
    $("status").textContent = JSON.stringify(res, null, 2);
    await refresh();
  }catch(e){
    // 1) validation 에러(test_url) 처리
    try{
      const j = JSON.parse(e.message);
      if(j.detail?.[0]?.loc?.includes("test_url")){
        alert("테스트 URL이 비어 있습니다.");
        return;
      }
    }catch{}

    // 2) ASP Logic 관련 오류
    try{
      const j = JSON.parse(e.message);
      if(typeof j.detail === "string" && j.detail.includes("ASP Logic")){
        alert(j.detail);
        return;
      }
    }catch(_){}

    // 3) ✅ 그 외(409 Already running 포함): 서버 detail을 그대로 보여주기
    try{
      const j = JSON.parse(e.message);
      if(typeof j.detail === "string" && j.detail.trim()){
        alert(j.detail);
        return;
      }
    }catch(_){}

    alert("요청 처리 중 오류가 발생했습니다.");
  }
});

$("btn_stop").addEventListener("click", async ()=>{
  try{
    await apiPostJson("/api/stop", {});
    await refresh();
  }catch(e){
    alert(friendlyErrorText(e));
  }
});

$("btn_reset").addEventListener("click", async ()=>{
  try{
    const res = await apiPostJson("/api/reset_state", payload());
    $("status").textContent = JSON.stringify(res, null, 2);
    await refresh();
  }catch(e){
    alert(friendlyErrorText(e));
  }
});

if($("btn_clear_plan")){
  $("btn_clear_plan").addEventListener("click", ()=>{
    clearPlanBox();
  });
}

if($("btn_latest_failure")){
  $("btn_latest_failure").addEventListener("click", async ()=>{
    try{
      const info = await apiGetJson("/api/latest_failure");
      if(!info || !info.found){
        alert("최근 실패 HTML snapshot이 없습니다.");
        return;
      }
      window.open("/api/latest_failure_view", "_blank");
    }catch(e){
      alert("최근 실패 HTML snapshot을 여는 중 오류가 발생했습니다.");
    }
  });
}

if($("btn_wording_report")){
  $("btn_wording_report").addEventListener("click", async ()=>{
    try {
      const outDir = $("out_dir").value.trim() || "run_logs_pw";
      window.open("/api/wording_report?out_dir=" + encodeURIComponent(outDir), "_blank");
    } catch(e) {
      alert("리포트를 여는 중 오류가 발생했습니다.");
    }
  });
}

// 입력 바뀔 때 자동 저장
["test_url","repeat","out_dir","concurrency","execution_timeout_sec","asp_logic","max_cases","max_total_runs",
 "mode_random","mode_coverage","tie_stable","tie_random",
 "auto_until_done","persist_state","include_default_paths","include_screen_cases","headless","select_all","rank_select_all","stop_at_page"
].forEach(id=>{
  const el = $(id);
  if(!el) return;
  el.addEventListener("change", saveForm);
  el.addEventListener("keyup", saveForm);
});

// 실시간 UX 검증(버튼 enable/disable + 경고 표시)
["test_url","asp_logic","mode_random","mode_coverage"].forEach(id=>{
  const el = $(id);
  if(!el) return;
  el.addEventListener("change", updateRunPlanEnabled);
  el.addEventListener("keyup", updateRunPlanEnabled);
});

// coverage 옵션 영역 토글과 함께 UX도 동기화
function applyModeUI(){
  const isCoverage = document.getElementById("mode_coverage").checked;
  const box = document.getElementById("coverage_opts");
  box.hidden = !isCoverage;
  updateRunPlanEnabled();
}

// init theme
loadTheme();
startWatchOSTheme();

// mode change (auto/manual)
if($("theme_mode")){
  $("theme_mode").addEventListener("change", ()=>{
    const mode = $("theme_mode").value === "auto" ? "auto" : "manual";
    saveMode(mode);
    setModeUI(mode);

    if(mode === "auto"){
      applyTheme(osPrefTheme());
    }else{
      // 수동으로 돌아오면 저장값(없으면 다크)
      const savedTheme = localStorage.getItem(THEME_KEY);
      applyTheme(savedTheme === "light" ? "light" : "dark");
    }
  });
}

// manual toggle (dark/light)
if($("theme_toggle")){
  $("theme_toggle").addEventListener("change", ()=>{
    // auto면 무시
    const mode = localStorage.getItem(THEME_MODE_KEY) || "manual";
    if(mode === "auto"){
      applyTheme(osPrefTheme());
      return;
    }
    const theme = $("theme_toggle").checked ? "dark" : "light";
    applyTheme(theme);
    saveTheme(theme);
  });
}
setBadges({mode: payload().mode, running:false});
setKpis({mode: payload().mode, planned_total: 0, current_run: 0, remaining_cases: "-"});

let refreshTimer = setInterval(refresh, 1500);
loadPlanBox();
refresh();

if($("banner_close")){
  $("banner_close").addEventListener("click", ()=> clearBanner());
}

document.getElementById("mode_random").addEventListener("change", applyModeUI);
document.getElementById("mode_coverage").addEventListener("change", applyModeUI);

// ✅ 페이지 로드시 1회 적용
applyModeUI();
updateRunPlanEnabled();
</script>
</body>
</html>
"""
