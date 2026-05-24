#!/usr/bin/env python3
"""
ACED Attendance UI/UX Revamp — injection script
Reads source HTML, injects CSS / HTML / JS, writes output.
"""

SRC  = '/root/.claude/uploads/2d581491-1b9c-44b7-8b40-abfd5acbe7d4/6187e289-index.html'
DEST = '/home/user/tutorial/aced-revamp/acedattendance-revamped.html'

with open(SRC, 'r', encoding='utf-8') as f:
    h = f.read()

# ── A. CSS injection ── inject before first </style>
CSS_INJECT = r"""
/* === ACED REVAMP v2 === */

/* Glassmorphism topbar */
.topbar{background:rgba(255,255,255,0.85)!important;backdrop-filter:blur(16px) saturate(1.8)!important;-webkit-backdrop-filter:blur(16px) saturate(1.8)!important;border-bottom:1px solid rgba(226,232,240,0.5)!important}
[data-theme="dark"] .topbar{background:rgba(17,24,39,0.85)!important;border-bottom:1px solid rgba(31,45,66,0.5)!important}

/* Glassmorphism sidebar */
.sidebar{background:rgba(7,13,26,0.9)!important;backdrop-filter:blur(20px) saturate(1.4)!important;-webkit-backdrop-filter:blur(20px) saturate(1.4)!important;border-right:1px solid rgba(255,255,255,0.06)!important;box-shadow:4px 0 32px rgba(0,0,0,0.2)!important}

/* Gradient stat cards */
.stat-card{transition:box-shadow .25s ease,transform .25s ease!important;border:none!important;overflow:hidden}
.stat-card::after{height:4px!important;border-radius:0 0 var(--radius) var(--radius)!important;opacity:.9}
.stat-card[style*="--accent:var(--green)"]{background:linear-gradient(135deg,#fff 60%,rgba(34,197,94,.06) 100%)}
.stat-card[style*="--accent:var(--amber)"]{background:linear-gradient(135deg,#fff 60%,rgba(245,158,11,.06) 100%)}
.stat-card[style*="--accent:var(--red)"]{background:linear-gradient(135deg,#fff 60%,rgba(239,68,68,.06) 100%)}
.stat-card[style*="--accent:var(--purple)"]{background:linear-gradient(135deg,#fff 60%,rgba(139,92,246,.06) 100%)}
[data-theme="dark"] .stat-card[style*="--accent:var(--green)"]{background:linear-gradient(135deg,var(--surface) 60%,rgba(34,197,94,.09) 100%)!important}
[data-theme="dark"] .stat-card[style*="--accent:var(--amber)"]{background:linear-gradient(135deg,var(--surface) 60%,rgba(245,158,11,.09) 100%)!important}
[data-theme="dark"] .stat-card[style*="--accent:var(--red)"]{background:linear-gradient(135deg,var(--surface) 60%,rgba(239,68,68,.09) 100%)!important}
[data-theme="dark"] .stat-card[style*="--accent:var(--purple)"]{background:linear-gradient(135deg,var(--surface) 60%,rgba(139,92,246,.09) 100%)!important}
.stat-card:hover{box-shadow:0 10px 36px rgba(13,27,62,.14),0 2px 8px rgba(13,27,62,.07)!important;transform:translateY(-3px)!important}

/* Card stagger animation */
@keyframes enhCardIn{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.enh-stagger{animation:enhCardIn .38s cubic-bezier(.16,1,.3,1) both}

/* Section transition */
@keyframes enhSectionIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.section.active{animation:enhSectionIn .28s cubic-bezier(.16,1,.3,1) both}

/* Sticky table headers */
.data-table thead th{position:sticky;top:0;z-index:10;box-shadow:0 1px 0 var(--border)}

/* Breathable spacing */
.content-area{padding:1.5rem!important}
.stats-grid{gap:1rem!important;margin-bottom:1rem!important}
.chart-card,.recent-card{padding:1.25rem!important}
.charts-row,.bottom-row{gap:1rem!important}
@media(max-width:768px){.content-area{padding:.875rem!important}}

/* Metric pill hover */
.metric-pill{transition:all .2s ease!important}
.metric-pill:hover{transform:translateY(-2px);border-color:var(--orange)!important;box-shadow:var(--shadow)!important}

/* Nav item animation */
.nav-item{transition:all .18s cubic-bezier(.16,1,.3,1)!important}
.nav-item:hover:not(.active){transform:translateX(3px)}

/* Recent item hover */
.recent-item{transition:all .18s ease!important}
.recent-item:hover{transform:translateX(3px);border-color:var(--orange)!important}

/* Button micro press */
.btn-primary:active,.btn-secondary:active,.btn-login:active{transform:scale(.96)!important}

/* Enhanced login card */
.login-card{box-shadow:0 32px 80px rgba(7,13,26,.32),0 8px 24px rgba(7,13,26,.16)!important}
.login-bg-pattern{background-image:radial-gradient(circle at 20% 20%,rgba(249,115,22,.18) 0%,transparent 45%),radial-gradient(circle at 80% 80%,rgba(30,50,100,.6) 0%,transparent 45%),radial-gradient(circle at 50% 50%,rgba(139,92,246,.07) 0%,transparent 60%),repeating-linear-gradient(45deg,transparent,transparent 40px,rgba(255,255,255,.02) 40px,rgba(255,255,255,.02) 80px)!important}

/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:10px}
::-webkit-scrollbar-thumb:hover{background:var(--orange)}

/* Mobile FAB */
.enh-fab{display:none;position:fixed;bottom:calc(68px + env(safe-area-inset-bottom,0px));right:1rem;z-index:95;width:58px;height:58px;border-radius:50%;border:none;cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-family:'Syne',sans-serif;font-size:.58rem;font-weight:700;color:#fff;transition:all .25s cubic-bezier(.16,1,.3,1);overflow:hidden}
.enh-fab svg{width:22px;height:22px;flex-shrink:0}
.enh-fab span{font-size:.55rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.enh-fab:active{transform:scale(.92)!important}
.enh-fab-ring{position:absolute;inset:-6px;border-radius:50%;border:2px solid rgba(255,255,255,.35);animation:pulsering 2.5s infinite}
.enh-fab-in{background:linear-gradient(145deg,var(--green),#16a34a);box-shadow:0 6px 24px rgba(34,197,94,.5)}
.enh-fab-out{background:linear-gradient(145deg,var(--red),#dc2626);box-shadow:0 6px 24px rgba(239,68,68,.5)}
.enh-fab-done{background:linear-gradient(145deg,#475569,#334155);box-shadow:0 4px 16px rgba(0,0,0,.2)}
.enh-fab-done .enh-fab-ring{display:none}
@media(max-width:768px){.enh-fab{display:flex}}

/* Celebration banner */
.enh-cel-banner{background:linear-gradient(135deg,rgba(124,58,237,.07),rgba(249,115,22,.07),rgba(236,72,153,.07));border:1.5px solid rgba(249,115,22,.3);border-radius:var(--radius);padding:1rem 1.1rem;margin-bottom:1rem;position:relative;overflow:hidden}
.enh-cel-header{display:flex;align-items:center;gap:.5rem;margin-bottom:.6rem;font-family:'Syne',sans-serif;font-weight:700;font-size:.9rem;color:var(--text-primary)}
.enh-cel-dismiss{margin-left:auto;background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:.9rem;padding:.1rem .3rem;border-radius:4px;transition:all .15s}
.enh-cel-dismiss:hover{background:var(--red-bg);color:var(--red)}
.enh-cel-list{display:flex;flex-direction:column;gap:.5rem}
.enh-cel-item{display:flex;align-items:flex-start;gap:.6rem;padding:.55rem .75rem;background:rgba(255,255,255,.6);border-radius:var(--radius-sm);border:1px solid rgba(249,115,22,.12)}
[data-theme="dark"] .enh-cel-item{background:rgba(255,255,255,.04)}
.enh-cel-emoji{font-size:1.4rem;flex-shrink:0}
.enh-cel-item strong{display:block;font-size:.85rem;font-weight:700;color:var(--text-primary)}
.enh-cel-item p{font-size:.78rem;color:var(--text-secondary);margin-top:.1rem}
/* Celebration toast */
.enh-cel-toast{border-left:4px solid var(--amber)!important}
.enh-cel-toast-emoji{font-size:1.4rem;flex-shrink:0}

/* Who's In Board */
.enh-wi-header{display:flex;align-items:flex-start;justify-content:space-between;gap:.875rem;margin-bottom:1rem;flex-wrap:wrap}
.enh-wi-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1rem}
.enh-wi-stat{background:var(--surface);border-radius:var(--radius);padding:1rem;text-align:center;border:1px solid var(--border);box-shadow:var(--shadow-sm);display:flex;flex-direction:column;align-items:center;gap:.2rem;font-size:.75rem;font-weight:600;transition:all .2s ease}
.enh-wi-stat:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.enh-wi-num{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;display:block;line-height:1}
.enh-wi-present{border-top:3px solid var(--green);color:var(--green)}.enh-wi-present .enh-wi-num{color:var(--green)}
.enh-wi-late{border-top:3px solid var(--amber);color:var(--amber)}.enh-wi-late .enh-wi-num{color:var(--amber)}
.enh-wi-absent{border-top:3px solid var(--red);color:var(--red)}.enh-wi-absent .enh-wi-num{color:var(--red)}
.enh-wi-leave{border-top:3px solid var(--purple);color:var(--purple)}.enh-wi-leave .enh-wi-num{color:var(--purple)}
.enh-wi-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:.875rem}
.enh-wi-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;box-shadow:var(--shadow-sm);transition:all .22s ease;animation:enhCardIn .35s cubic-bezier(.16,1,.3,1) both;display:flex;flex-direction:column;gap:.7rem}
.enh-wi-card:hover{box-shadow:var(--shadow);transform:translateY(-2px)}
.enh-wi-card.s-present{border-left:3px solid var(--green)}
.enh-wi-card.s-late{border-left:3px solid var(--amber)}
.enh-wi-card.s-absent{border-left:3px solid var(--red);opacity:.8}
.enh-wi-card.s-on-leave{border-left:3px solid var(--purple)}
.enh-wi-top{display:flex;align-items:center;gap:.65rem}
.enh-wi-av{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:.9rem;color:#fff;flex-shrink:0;position:relative;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.enh-wi-dot{position:absolute;bottom:-2px;right:-2px;width:11px;height:11px;border-radius:50%;border:2px solid var(--surface)}
.enh-dot-present{background:var(--green);box-shadow:0 0 0 2px rgba(34,197,94,.3)}
.enh-dot-late{background:var(--amber)}
.enh-dot-absent{background:var(--red)}
.enh-dot-on-leave{background:var(--purple)}
.enh-wi-info{flex:1;min-width:0}
.enh-wi-name{font-family:'Syne',sans-serif;font-size:.875rem;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.enh-wi-dept{font-size:.7rem;color:var(--text-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:.05rem}
.enh-wi-times{display:flex;align-items:center;background:var(--surface-2);border:1px solid var(--border-light);border-radius:var(--radius-sm);overflow:hidden}
.enh-wi-t{flex:1;display:flex;flex-direction:column;align-items:center;padding:.42rem .3rem;gap:.05rem}
.enh-wi-tdiv{width:1px;height:32px;background:var(--border);flex-shrink:0}
.enh-wi-tlbl{font-size:.58rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em}
.enh-wi-tval{font-family:'Syne',sans-serif;font-size:.78rem;font-weight:700;color:var(--text-primary)}
.enh-wi-tval.active-now{color:var(--green)}
.enh-wi-tval.active-now::after{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--green);margin-left:3px;vertical-align:middle;animation:pulseDot 2s infinite}
@media(max-width:768px){.enh-wi-stats{grid-template-columns:repeat(2,1fr)}.enh-wi-grid{grid-template-columns:1fr}.enh-wi-header{flex-direction:column}.enh-wi-header>div:last-child{width:100%}.enh-wi-header .search-input{width:100%;min-width:0}}
</style>"""

# Replace the FIRST </style> only
first_style_close = h.index('</style>')
h = h[:first_style_close] + CSS_INJECT + h[first_style_close + len('</style>'):]

# ── B. Who's In section HTML ── inject before `    </main>`
WHOISIN_SECTION = """      <!-- WHO'S IN BOARD -->
      <section id="section-whoisin" class="section">
        <div class="enh-wi-header">
          <div>
            <h2 style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800">Team Status Board</h2>
            <p id="wi-subtitle" style="font-size:.8rem;color:var(--text-secondary);margin-top:.15rem">Loading…</p>
          </div>
          <div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap">
            <input type="text" class="search-input" id="wi-search" placeholder="Search…" style="min-width:160px" oninput="enhWIRender()">
            <select id="wi-dept" class="search-input" style="min-width:140px" onchange="enhWIRender()"><option value="all">All Departments</option></select>
            <select id="wi-status" class="search-input" style="min-width:140px" onchange="enhWIRender()">
              <option value="all">All Status</option>
              <option value="Present">Present</option>
              <option value="Late">Late</option>
              <option value="Absent">Absent</option>
              <option value="On Leave">On Leave</option>
            </select>
          </div>
        </div>
        <div class="enh-wi-stats" id="wi-stats"></div>
        <div class="enh-wi-grid" id="wi-grid"></div>
      </section>
    </main>"""

h = h.replace('    </main>', WHOISIN_SECTION, 1)

# ── C. Who's In sidebar nav item ── inject after attendance nav item's </a>
# The attendance nav item block ends with </a> on a new line after the indicator div
SIDEBAR_ATT_BLOCK = """      <a class="nav-item" data-section="attendance" onclick="ACED.nav.go('attendance')">
        <i data-lucide="clock"></i><span>Attendance</span><div class="nav-indicator"></div>
      </a>"""

SIDEBAR_ATT_WITH_WHOISIN = SIDEBAR_ATT_BLOCK + """
      <a class="nav-item" data-section="whoisin" onclick="ACED.nav.go('whoisin')">
        <i data-lucide="users-round"></i><span>Who's In</span><div class="nav-indicator"></div>
      </a>"""

h = h.replace(SIDEBAR_ATT_BLOCK, SIDEBAR_ATT_WITH_WHOISIN, 1)

# ── D. Who's In mobile nav item ── inject after attendance button in mobile nav
MOBILE_ATT_BTN = """<button class="mnav-item" data-section="attendance" onclick="ACED.nav.go('attendance')"><i data-lucide="clock"></i><span>Attendance</span></button>"""
MOBILE_ATT_WITH_WHOISIN = MOBILE_ATT_BTN + """
      <button class="mnav-item" data-section="whoisin" onclick="ACED.nav.go('whoisin')"><i data-lucide="users-round"></i><span>Who's In</span></button>"""

h = h.replace(MOBILE_ATT_BTN, MOBILE_ATT_WITH_WHOISIN, 1)

# ── E. Birthday field ── inject after join date field
JOIN_DATE_FIELD = '<div class="form-group"><label>Join Date</label><input type="date" id="emp-join-date"></div>'
JOIN_DATE_WITH_BIRTHDAY = JOIN_DATE_FIELD + """
        <div class="form-group"><label>Date of Birth <span style="font-size:.7rem;color:var(--text-muted)">(birthday alerts)</span></label><input type="date" id="emp-birthday"></div>"""

h = h.replace(JOIN_DATE_FIELD, JOIN_DATE_WITH_BIRTHDAY, 1)

# ── F. Mobile FAB ── inject just before `</div>\n\n<!-- MODALS -->`
FAB_ANCHOR = '</div>\n\n<!-- MODALS -->'
FAB_HTML = """<button id="enh-fab" class="enh-fab enh-fab-in" aria-label="Clock In/Out" onclick="ACED.nav.go('attendance');setTimeout(function(){var b=document.getElementById('clock-btn');if(b)b.click();},350)">
  <div class="enh-fab-ring"></div>
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
  <span id="enh-fab-lbl">Clock In</span>
</button>
</div>

<!-- MODALS -->"""

h = h.replace(FAB_ANCHOR, FAB_HTML, 1)

# ── G. Enhancement JS ── inject before </body>
ENHANCEMENT_JS = r"""
<script>
/* ================================================================
   ACED REVAMP v2 — Enhancement Layer
   Uses MutationObserver + event listeners only.
   Does NOT wrap or replace any ACED functions.
   ================================================================ */
(function(){
  'use strict';

  /* ── Helpers ── */
  function fmt12(t){
    if(!t||t==='—') return t||'—';
    try{
      var p=t.split(':').map(Number);
      var ampm=p[0]>=12?'PM':'AM';
      var hh=p[0]%12||12;
      return hh+':'+(String(p[1]).padStart(2,'0'))+' '+ampm;
    }catch(e){return t;}
  }

  function enhDur(ci,co){
    if(!ci||!co) return '—';
    var a=ci.split(':').map(Number),b=co.split(':').map(Number);
    var m=(b[0]*60+b[1])-(a[0]*60+a[1]);
    return m<=0?'—':Math.floor(m/60)+'h '+m%60+'m';
  }

  function todayStr(){
    var d=new Date();
    return d.getFullYear()+'-'+(String(d.getMonth()+1).padStart(2,'0'))+'-'+(String(d.getDate()).padStart(2,'0'));
  }

  function todayMMDD(){
    var s=todayStr();
    return s.slice(5);
  }

  var COLORS=['#F97316','#0D1B3E','#22C55E','#8B5CF6','#3B82F6','#F59E0B','#EF4444','#14B8A6'];

  function colorForUser(uid){
    var idx=0;
    for(var i=0;i<uid.length;i++) idx=(idx+uid.charCodeAt(i))%COLORS.length;
    return COLORS[idx];
  }

  function initials(u){
    return ((u.firstName||'?')[0]+(u.lastName||'?')[0]).toUpperCase();
  }

  /* ── 1. Count-up animation ── */
  function enhCountUp(el,target,duration){
    if(!el) return;
    var start=performance.now();
    var from=0;
    function step(now){
      var progress=Math.min((now-start)/duration,1);
      var ease=1-Math.pow(1-progress,3);
      el.textContent=Math.round(from+(target-from)*ease);
      if(progress<1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function triggerCountUps(){
    document.querySelectorAll('.stat-value,.metric-value,.rsc-value').forEach(function(el){
      var raw=parseInt(el.textContent,10);
      if(!isNaN(raw)&&raw>0) enhCountUp(el,raw,900);
    });
  }

  /* ── 2. Stagger animation ── */
  function enhStagger(selector,delay){
    document.querySelectorAll(selector).forEach(function(el,i){
      el.classList.remove('enh-stagger');
      void el.offsetWidth; // reflow
      el.style.animationDelay=(i*delay)+'ms';
      el.classList.add('enh-stagger');
    });
  }

  /* ── 3. FAB state update ── */
  function enhUpdateFAB(){
    var fab=document.getElementById('enh-fab');
    var lbl=document.getElementById('enh-fab-lbl');
    if(!fab||!lbl) return;
    if(typeof STATE==='undefined'||!STATE.currentUser) return;
    if(typeof DB==='undefined') return;
    var today=todayStr();
    var uid=STATE.currentUser.id;
    var rec=DB.attendance.find(function(r){return r.userId===uid&&r.date===today;});
    fab.className='enh-fab';
    if(!rec||!rec.clockIn){
      fab.classList.add('enh-fab-in');
      lbl.textContent='Clock In';
    } else if(rec.clockIn&&!rec.clockOut){
      fab.classList.add('enh-fab-out');
      lbl.textContent='Clock Out';
    } else {
      fab.classList.add('enh-fab-done');
      lbl.textContent='Done ✓';
    }
  }

  /* ── 4. Who's In render ── */
  var wiDeptPopulated=false;
  var wiAutoTimer=null;

  window.enhWIRender=function(){
    if(typeof DB==='undefined') return;
    var grid=document.getElementById('wi-grid');
    var statsEl=document.getElementById('wi-stats');
    var subtitle=document.getElementById('wi-subtitle');
    if(!grid||!statsEl) return;

    var today=todayStr();
    var searchVal=(document.getElementById('wi-search')||{value:''}).value.toLowerCase();
    var deptVal=(document.getElementById('wi-dept')||{value:'all'}).value;
    var statusVal=(document.getElementById('wi-status')||{value:'all'}).value;

    // Populate dept dropdown once
    if(!wiDeptPopulated){
      var deptSel=document.getElementById('wi-dept');
      if(deptSel){
        var depts={};
        DB.users.forEach(function(u){if(u.department) depts[u.department]=1;});
        Object.keys(depts).sort().forEach(function(d){
          var opt=document.createElement('option');
          opt.value=d; opt.textContent=d;
          deptSel.appendChild(opt);
        });
        wiDeptPopulated=true;
      }
    }

    // Build status map
    var activeUsers=DB.users.filter(function(u){return u.status==='active'||u.status==='on-leave';});

    var statusMap={};
    activeUsers.forEach(function(u){
      var rec=DB.attendance.find(function(r){return r.userId===u.id&&r.date===today;});
      // Check approved leave
      var onLeave=DB.leaves.some(function(l){
        return l.userId===u.id&&l.status==='Approved'&&l.startDate<=today&&l.endDate>=today;
      });
      var status='Absent',clockIn='—',clockOut='—';
      if(onLeave){status='On Leave';}
      else if(rec){
        clockIn=rec.clockIn||'—';
        clockOut=rec.clockOut||'—';
        status=rec.status==='Late'?'Late':'Present';
      }
      statusMap[u.id]={status:status,clockIn:clockIn,clockOut:clockOut};
    });

    // Stats
    var counts={Present:0,Late:0,Absent:0,'On Leave':0};
    activeUsers.forEach(function(u){ var s=statusMap[u.id].status; if(counts[s]!==undefined) counts[s]++; });
    statsEl.innerHTML='<div class="enh-wi-stat enh-wi-present"><span class="enh-wi-num">'+counts.Present+'</span>Present</div>'
      +'<div class="enh-wi-stat enh-wi-late"><span class="enh-wi-num">'+counts.Late+'</span>Late</div>'
      +'<div class="enh-wi-stat enh-wi-absent"><span class="enh-wi-num">'+counts.Absent+'</span>Absent</div>'
      +'<div class="enh-wi-stat enh-wi-leave"><span class="enh-wi-num">'+counts['On Leave']+'</span>On Leave</div>';

    // Sort
    var sortOrder={Present:0,Late:1,'On Leave':2,Absent:3};
    var filtered=activeUsers.slice().sort(function(a,b){
      return sortOrder[statusMap[a.id].status]-sortOrder[statusMap[b.id].status];
    });

    // Filter
    filtered=filtered.filter(function(u){
      if(deptVal!=='all'&&u.department!==deptVal) return false;
      if(statusVal!=='all'&&statusMap[u.id].status!==statusVal) return false;
      if(searchVal){
        var name=(u.firstName+' '+u.lastName).toLowerCase();
        if(name.indexOf(searchVal)<0&&(u.department||'').toLowerCase().indexOf(searchVal)<0&&(u.position||'').toLowerCase().indexOf(searchVal)<0) return false;
      }
      return true;
    });

    // Render cards
    var html='';
    filtered.forEach(function(u,idx){
      var info=statusMap[u.id];
      var sc=info.status.toLowerCase().replace(/\s+/g,'-');
      var color=colorForUser(u.id);
      var dur=enhDur(info.clockIn==='—'?null:info.clockIn,info.clockOut==='—'?null:info.clockOut);
      var activeClass=(info.clockIn!=='—'&&info.clockOut==='—')?'active-now':'';
      var badgeClass=sc;
      html+='<div class="enh-wi-card s-'+sc+'" style="animation-delay:'+(idx*40)+'ms">'
        +'<div class="enh-wi-top">'
        +'<div class="enh-wi-av" style="background:'+color+'">'+initials(u)
        +'<div class="enh-wi-dot enh-dot-'+sc+'"></div></div>'
        +'<div class="enh-wi-info">'
        +'<div class="enh-wi-name">'+(u.firstName+' '+u.lastName)+'</div>'
        +'<div class="enh-wi-dept">'+((u.position||'')+' · '+(u.department||''))+'</div>'
        +'</div>'
        +'<span class="badge '+badgeClass+'">'+info.status+'</span>'
        +'</div>'
        +'<div class="enh-wi-times">'
        +'<div class="enh-wi-t"><span class="enh-wi-tlbl">In</span><span class="enh-wi-tval '+activeClass+'">'+fmt12(info.clockIn)+'</span></div>'
        +'<div class="enh-wi-tdiv"></div>'
        +'<div class="enh-wi-t"><span class="enh-wi-tlbl">Out</span><span class="enh-wi-tval">'+fmt12(info.clockOut)+'</span></div>'
        +'<div class="enh-wi-tdiv"></div>'
        +'<div class="enh-wi-t"><span class="enh-wi-tlbl">Hours</span><span class="enh-wi-tval">'+dur+'</span></div>'
        +'</div>'
        +'</div>';
    });
    grid.innerHTML=html||'<p style="color:var(--text-muted);font-size:.85rem;padding:.5rem">No employees match filters.</p>';

    if(subtitle){
      var now=new Date();
      subtitle.textContent='Last updated: '+now.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})+' · '+activeUsers.length+' active employees';
    }
  };

  /* ── 5. Birthday & anniversary check ── */
  var celebrationsShown=false;

  function enhCheckCelebrations(){
    if(typeof DB==='undefined') return;
    var today=todayStr();
    var todayMD=todayMMDD();
    var thisYear=new Date().getFullYear();
    var items=[];

    DB.users.forEach(function(u){
      if(u.status!=='active') return;
      // Birthday
      if(u.birthday&&u.birthday.slice(5)===todayMD){
        items.push({emoji:'🎂',name:u.firstName+' '+u.lastName,msg:'Happy Birthday! 🎉',type:'birthday'});
        if(typeof ACED!=='undefined'&&ACED.ui&&ACED.ui.toast){
          ACED.ui.toast('🎂 Happy Birthday '+u.firstName+'!','',9000,'enh-cel-toast');
        }
      }
      // Work anniversary
      if(u.joinDate&&u.joinDate.slice(5)===todayMD){
        var years=thisYear-parseInt(u.joinDate.slice(0,4),10);
        if(years>0){
          items.push({emoji:'🌟',name:u.firstName+' '+u.lastName,msg:years+' year'+(years>1?'s':'')+' with the team! 👏',type:'anniversary'});
          if(typeof ACED!=='undefined'&&ACED.ui&&ACED.ui.toast){
            ACED.ui.toast('🌟 '+u.firstName+' — '+years+' year anniversary!','',9000,'enh-cel-toast');
          }
        }
      }
    });

    if(!items.length) return;
    var dash=document.getElementById('section-dashboard');
    if(!dash) return;
    // Remove existing banner
    var existing=dash.querySelector('.enh-cel-banner');
    if(existing) existing.remove();

    var banner=document.createElement('div');
    banner.className='enh-cel-banner';
    var listHTML=items.map(function(item){
      return '<div class="enh-cel-item"><span class="enh-cel-emoji">'+item.emoji+'</span><div><strong>'+item.name+'</strong><p>'+item.msg+'</p></div></div>';
    }).join('');
    banner.innerHTML='<div class="enh-cel-header"><span>🎉 Celebrations Today</span><button class="enh-cel-dismiss" onclick="this.parentElement.parentElement.remove()" title="Dismiss">×</button></div><div class="enh-cel-list">'+listHTML+'</div>';
    dash.insertBefore(banner,dash.firstChild);
  }

  /* ── 6. Employee modal birthday persistence ── */

  // Save birthday when modal save button is clicked (event delegation)
  document.addEventListener('click',function(e){
    // Match save button inside employee-modal
    var modal=document.getElementById('employee-modal');
    if(!modal) return;
    var btn=e.target.closest('button');
    if(!btn) return;
    // Find the save/submit button by checking it's inside the employee modal and has primary class
    if(!modal.contains(btn)) return;
    if(!btn.classList.contains('btn-primary')) return;
    // Save birthday value onto the user object
    setTimeout(function(){
      var bdEl=document.getElementById('emp-birthday');
      var idEl=document.getElementById('emp-modal-id');
      if(!bdEl||!idEl) return;
      var userId=idEl.value;
      var bdVal=bdEl.value;
      if(!userId||!bdVal) return;
      if(typeof DB==='undefined') return;
      var user=DB.users.find(function(u){return u.id===userId;});
      if(user) user.birthday=bdVal;
    },200);
  });

  // Pre-fill birthday when employee modal opens — use MutationObserver
  var empModalEl=document.getElementById('employee-modal');
  if(empModalEl){
    var empModalObs=new MutationObserver(function(mutations){
      mutations.forEach(function(m){
        if(m.type==='attributes'&&m.attributeName==='class'){
          var isVisible=!empModalEl.classList.contains('hidden');
          if(isVisible){
            setTimeout(function(){
              var idEl=document.getElementById('emp-modal-id');
              var bdEl=document.getElementById('emp-birthday');
              if(!idEl||!bdEl) return;
              var userId=idEl.value;
              if(!userId) return;
              if(typeof DB==='undefined') return;
              var user=DB.users.find(function(u){return u.id===userId;});
              if(user&&user.birthday) bdEl.value=user.birthday;
              else bdEl.value='';
            },120);
          }
        }
      });
    });
    empModalObs.observe(empModalEl,{attributes:true,attributeFilter:['class']});
  }

  /* ── 9. Arc ring on clock widget ── */
  var arcTimer=null;

  function enhUpdateArc(){
    var arc=document.getElementById('enh-arc-fill');
    if(!arc) return;
    if(typeof DB==='undefined') return;
    var settings=DB.settings||{};
    var ws=settings.workStart||'08:00';
    var we=settings.workEnd||'17:00';
    var lt=settings.lateThreshold||'08:20';
    var now=new Date();
    var nowMins=now.getHours()*60+now.getMinutes();
    var startMins=parseInt(ws.split(':')[0])*60+parseInt(ws.split(':')[1]);
    var endMins=parseInt(we.split(':')[0])*60+parseInt(we.split(':')[1]);
    var lateMins=parseInt(lt.split(':')[0])*60+parseInt(lt.split(':')[1]);
    var total=endMins-startMins;
    var progress=Math.max(0,Math.min(1,(nowMins-startMins)/total));
    var circumference=326.7;
    arc.style.strokeDashoffset=circumference*(1-progress);
    if(nowMins<=lateMins) arc.style.stroke='var(--green)';
    else if(nowMins<=endMins) arc.style.stroke='var(--amber)';
    else arc.style.stroke='var(--orange)';
  }

  function enhInjectArc(){
    var clockDisplay=document.querySelector('.clock-display');
    if(!clockDisplay||document.getElementById('enh-arc')) return;
    var svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
    svg.id='enh-arc';
    svg.setAttribute('style','position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg);opacity:.15;pointer-events:none');
    svg.setAttribute('viewBox','0 0 120 120');
    svg.innerHTML='<circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" stroke-width="5"/>'
      +'<circle id="enh-arc-fill" cx="60" cy="60" r="52" fill="none" stroke="var(--green)" stroke-width="5" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="326.7" style="transition:stroke-dashoffset 1s linear,stroke .5s ease"/>';
    clockDisplay.appendChild(svg);
    enhUpdateArc();
    if(arcTimer) clearInterval(arcTimer);
    arcTimer=setInterval(enhUpdateArc,60000);
  }

  /* ── 7 & 8. MutationObservers ── */

  function onLoginReady(){
    // Set demo birthday data
    if(typeof DB!=='undefined'&&DB.users&&DB.users[1]){
      DB.users[1].birthday=todayStr();
    }
    setTimeout(function(){
      enhCheckCelebrations();
      enhUpdateFAB();
      enhStagger('.stat-card',80);
      enhStagger('.metric-pill',60);
      triggerCountUps();
    },600);
  }

  // Observer 7: watch login-screen for hidden class
  var loginScreen=document.getElementById('login-screen');
  if(loginScreen){
    var loginObs=new MutationObserver(function(mutations){
      mutations.forEach(function(m){
        if(m.type==='attributes'&&m.attributeName==='class'){
          if(loginScreen.classList.contains('hidden')){
            onLoginReady();
          }
        }
      });
    });
    loginObs.observe(loginScreen,{attributes:true,attributeFilter:['class']});
  }

  // Observer 8: watch for section active class changes
  var contentArea=document.getElementById('content-area');
  if(contentArea){
    var sectionObs=new MutationObserver(function(mutations){
      mutations.forEach(function(m){
        if(m.type==='attributes'&&m.attributeName==='class'&&m.target.classList.contains('section')){
          if(m.target.classList.contains('active')){
            var sid=m.target.id;
            if(sid==='section-dashboard'){
              setTimeout(function(){
                enhStagger('.stat-card',80);
                enhStagger('.metric-pill',60);
                triggerCountUps();
              },200);
            } else if(sid==='section-whoisin'){
              enhWIRender();
            } else if(sid==='section-attendance'){
              enhUpdateFAB();
              setTimeout(function(){enhInjectArc();},150);
            }
          }
        }
      });
    });
    sectionObs.observe(contentArea,{attributes:true,attributeFilter:['class'],subtree:true});
  }

  /* ── 10. Auto-refresh timers ── */
  setInterval(function(){
    if(typeof STATE!=='undefined'&&STATE.currentSection==='whoisin') enhWIRender();
    enhUpdateFAB();
  },90000);

  /* ── Boot ── */
  function domReady(cb){
    var attempts=0;
    function poll(){
      attempts++;
      if(typeof window.ACED!=='undefined'&&typeof window.DB!=='undefined'&&typeof window.STATE!=='undefined'){
        cb();
      } else if(attempts<150){
        setTimeout(poll,100);
      }
    }
    if(document.readyState==='loading'){
      document.addEventListener('DOMContentLoaded',function(){setTimeout(poll,100);});
    } else {
      setTimeout(poll,100);
    }
  }

  domReady(function(){
    // Set up any post-ready initialisation that needs ACED/DB/STATE
    // If user is already logged in (session restore), trigger onLoginReady
    if(typeof STATE!=='undefined'&&STATE.currentUser){
      onLoginReady();
    }
    // Re-observe in case login-screen was already hidden before observer was set up
    var ls=document.getElementById('login-screen');
    if(ls&&ls.classList.contains('hidden')&&typeof STATE!=='undefined'&&STATE.currentUser){
      onLoginReady();
    }
  });

})();
</script>
</body>"""

h = h.replace('</body>', ENHANCEMENT_JS, 1)

# Write output
with open(DEST, 'w', encoding='utf-8') as f:
    f.write(h)

print('Written:', DEST)

# ── Final verification ──
with open(DEST) as f:
    h2 = f.read()

checks = {
  'Firebase config': 'firebaseConfig' in h2,
  'Login form intact': 'id="login-form"' in h2,
  'FIREBASE_ENABLED=true': 'FIREBASE_ENABLED = true' in h2,
  'No external CSS ref': 'aced-enhancements.css' not in h2,
  'No external JS ref': 'aced-enhancements.js' not in h2,
  'Whoisin section': 'section-whoisin' in h2,
  'Birthday field': 'emp-birthday' in h2,
  'Mobile FAB': 'enh-fab' in h2,
  'Arc ring': 'enh-arc' in h2,
  'Celebration banner': 'enh-cel-banner' in h2,
  'ACED.auth.onLogin NOT overwritten': 'ACED.auth.onLogin = ' not in h2.split('async onLogin')[1][:200] if 'async onLogin' in h2 else True,
}
for k,v in checks.items():
    print(f"{'OK' if v else 'FAIL'} {k}")
print('Total size:', round(len(h2)/1024,1), 'KB')
