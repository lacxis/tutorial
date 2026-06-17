/* ================================================================
   ACED Attendance — Enhancements v1.0
   Visual · Layout · Interactions · Who's In · Celebrations
   ================================================================ */
(function () {
  'use strict';

  /* ── Wait for ACED to be fully initialised ─────────────────── */
  function whenReady(cb) {
    if (window.ACED && window.ACED.nav && window.ACED.toast && window.STATE && window.DB) {
      cb();
    } else {
      setTimeout(function () { whenReady(cb); }, 80);
    }
  }

  /* ================================================================
     1. COUNT-UP ANIMATION
     ================================================================ */
  function countUp(el, target, duration) {
    if (!el) return;
    duration = duration || 750;
    var start = 0;
    var startTime = performance.now();
    var isPercent = String(target).includes('%');
    var numTarget = parseInt(target) || 0;

    function update(currentTime) {
      var elapsed = currentTime - startTime;
      var progress = Math.min(elapsed / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.round(start + (numTarget - start) * eased);
      el.textContent = isPercent ? current + '%' : current;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  }

  function triggerStatCountup() {
    document.querySelectorAll('.stat-value').forEach(function (el) {
      var raw = el.textContent.trim();
      if (/^\d+$/.test(raw)) countUp(el, parseInt(raw));
    });
    document.querySelectorAll('.metric-value').forEach(function (el) {
      var raw = el.textContent.trim();
      if (/^\d+%$/.test(raw)) {
        var num = parseInt(raw);
        countUp(el, num);
        setTimeout(function () {
          var t = el.textContent.replace('%', '');
          el.textContent = t + '%';
        }, 800);
      }
    });
    document.querySelectorAll('.rsc-value').forEach(function (el) {
      var raw = el.textContent.trim();
      if (/^\d+$/.test(raw)) countUp(el, parseInt(raw));
    });
  }

  /* ================================================================
     2. STAGGERED CARD ANIMATION
     ================================================================ */
  function animateCards(selector, delay) {
    delay = delay || 70;
    var cards = document.querySelectorAll(selector);
    cards.forEach(function (card, i) {
      card.classList.remove('enh-animate');
      void card.offsetWidth; // reflow
      card.style.animationDelay = (i * delay) + 'ms';
      card.classList.add('enh-animate');
    });
  }

  /* ================================================================
     3. MOBILE FLOATING ACTION BUTTON
     ================================================================ */
  function injectMobileFAB() {
    if (document.getElementById('enh-mobile-fab')) return;

    var fab = document.createElement('button');
    fab.id = 'enh-mobile-fab';
    fab.className = 'enh-mobile-fab enh-fab-clockin';
    fab.setAttribute('aria-label', 'Clock In / Out');
    fab.innerHTML =
      '<div class="enh-fab-ring"></div>' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>' +
      '</svg>' +
      '<span id="enh-fab-label">Clock In</span>';

    fab.addEventListener('click', function () {
      if (!window.ACED || !window.ACED.attendance) return;
      ACED.nav.go('attendance');
      setTimeout(function () {
        var clockBtn = document.getElementById('clock-btn');
        if (clockBtn) clockBtn.click();
      }, 350);
    });

    var app = document.getElementById('app');
    if (app) app.appendChild(fab);
  }

  function updateFABState() {
    var fab = document.getElementById('enh-mobile-fab');
    var label = document.getElementById('enh-fab-label');
    if (!fab || !window.STATE || !STATE.currentUser) return;

    var todayStr = new Date().toISOString().split('T')[0];
    var rec = DB.attendance.find(function (r) {
      return r.userId === STATE.currentUser.id && r.date === todayStr;
    });

    if (!rec || !rec.clockIn) {
      fab.className = 'enh-mobile-fab enh-fab-clockin';
      if (label) label.textContent = 'Clock In';
    } else if (rec.clockIn && !rec.clockOut) {
      fab.className = 'enh-mobile-fab enh-fab-clockout';
      if (label) label.textContent = 'Clock Out';
    } else {
      fab.className = 'enh-mobile-fab enh-fab-done';
      if (label) label.textContent = 'Done ✓';
    }
  }

  /* ================================================================
     4. ARC RING ON CLOCK WIDGET
     ================================================================ */
  function upgradeClockWidget() {
    if (document.getElementById('enh-arc-ring')) return;
    var clockDisplay = document.querySelector('.clock-display');
    if (!clockDisplay) return;

    clockDisplay.style.position = 'relative';
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('id', 'enh-arc-ring');
    svg.setAttribute('class', 'enh-arc-svg');
    svg.setAttribute('viewBox', '0 0 120 120');

    var track = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    track.setAttribute('class', 'enh-arc-track');
    track.setAttribute('cx', '60'); track.setAttribute('cy', '60'); track.setAttribute('r', '52');

    var fill = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    fill.setAttribute('id', 'enh-arc-fill');
    fill.setAttribute('class', 'enh-arc-fill');
    fill.setAttribute('cx', '60'); fill.setAttribute('cy', '60'); fill.setAttribute('r', '52');
    fill.setAttribute('stroke-dasharray', '326.7');
    fill.setAttribute('stroke-dashoffset', '326.7');

    svg.appendChild(track);
    svg.appendChild(fill);
    clockDisplay.appendChild(svg);
    updateArcRing();
  }

  function updateArcRing() {
    var fill = document.getElementById('enh-arc-fill');
    if (!fill || !window.DB || !DB.settings) return;

    var now = new Date();
    var parts = DB.settings.workStart.split(':').map(Number);
    var startH = parts[0], startM = parts[1];
    var eParts = DB.settings.workEnd.split(':').map(Number);
    var endH = eParts[0], endM = eParts[1];
    var lateParts = (DB.settings.lateThreshold || '08:20').split(':').map(Number);

    var dayStart = startH * 60 + startM;
    var dayEnd   = endH * 60 + endM;
    var lateMins = lateParts[0] * 60 + lateParts[1];
    var nowMins  = now.getHours() * 60 + now.getMinutes();

    var progress = Math.min(Math.max((nowMins - dayStart) / (dayEnd - dayStart), 0), 1);
    fill.style.strokeDashoffset = String(326.7 * (1 - progress));

    if (nowMins < lateMins)      fill.style.stroke = 'var(--green)';
    else if (nowMins < dayEnd)   fill.style.stroke = 'var(--amber)';
    else                         fill.style.stroke = 'var(--orange)';
  }

  /* ================================================================
     5. SMOOTH PAGE TRANSITIONS + NAV HOOK
     ================================================================ */
  function wrapNavGo() {
    if (ACED.nav._enhWrapped) return;
    var original = ACED.nav.go.bind(ACED.nav);
    ACED.nav.go = function (section) {
      var current = document.querySelector('.section.active');
      if (current) {
        current.style.transition = 'opacity 0.15s ease, transform 0.15s ease';
        current.style.opacity = '0';
        current.style.transform = 'translateY(6px)';
      }
      setTimeout(function () {
        original(section);
        var next = document.querySelector('.section.active');
        if (next) {
          next.style.opacity = '0';
          next.style.transform = 'translateY(10px)';
          next.style.transition = 'none';
          requestAnimationFrame(function () {
            requestAnimationFrame(function () {
              next.style.transition = 'opacity 0.28s ease, transform 0.28s ease';
              next.style.opacity = '1';
              next.style.transform = 'translateY(0)';
            });
          });
        }
        /* Section-specific side effects */
        if (section === 'whoisin') {
          renderWhoisin();
        }
        if (section === 'dashboard') {
          setTimeout(triggerStatCountup, 250);
          setTimeout(function () { animateCards('.stat-card', 80); }, 50);
        }
        if (section === 'attendance') {
          updateFABState();
          setTimeout(upgradeClockWidget, 100);
        }
        updateFABState();
      }, 140);
    };
    ACED.nav._enhWrapped = true;
  }

  /* ================================================================
     6. WHO'S IN BOARD
     ================================================================ */
  function injectWhoisinSection() {
    if (document.querySelector('[data-section="whoisin"]')) return;

    /* Sidebar nav item */
    var attNav = document.querySelector('[data-section="attendance"]');
    if (attNav) {
      var navItem = document.createElement('a');
      navItem.className = 'nav-item';
      navItem.setAttribute('data-section', 'whoisin');
      navItem.innerHTML =
        '<i data-lucide="users-round"></i><span>Who\'s In</span><div class="nav-indicator"></div>';
      navItem.addEventListener('click', function () { ACED.nav.go('whoisin'); });
      attNav.parentNode.insertBefore(navItem, attNav.nextSibling);
    }

    /* Mobile bottom nav item */
    var mobileNav = document.querySelector('.mnav-items');
    if (mobileNav) {
      var mobileItem = document.createElement('button');
      mobileItem.className = 'mnav-item';
      mobileItem.setAttribute('data-section', 'whoisin');
      mobileItem.innerHTML = '<i data-lucide="users-round"></i><span>Who\'s In</span>';
      mobileItem.addEventListener('click', function () { ACED.nav.go('whoisin'); });
      if (mobileNav.children.length >= 2) {
        mobileNav.insertBefore(mobileItem, mobileNav.children[2]);
      } else {
        mobileNav.appendChild(mobileItem);
      }
    }

    /* Section HTML */
    var section = document.createElement('section');
    section.id = 'section-whoisin';
    section.className = 'section';
    section.innerHTML =
      '<div class="enh-whoisin-header">' +
        '<div>' +
          '<h2 style="font-family:\'Syne\',sans-serif;font-size:1.1rem;font-weight:800">Team Status Board</h2>' +
          '<p id="whoisin-subtitle" style="font-size:.8rem;color:var(--text-secondary);margin-top:.15rem">Loading…</p>' +
        '</div>' +
        '<div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap">' +
          '<input type="text" class="search-input" id="whoisin-search" placeholder="Search…" style="min-width:160px">' +
          '<select id="whoisin-dept" class="search-input" style="min-width:140px">' +
            '<option value="all">All Departments</option>' +
          '</select>' +
          '<select id="whoisin-status-filter" class="search-input" style="min-width:140px">' +
            '<option value="all">All Status</option>' +
            '<option value="Present">Present</option>' +
            '<option value="Late">Late</option>' +
            '<option value="Absent">Absent</option>' +
            '<option value="On Leave">On Leave</option>' +
          '</select>' +
        '</div>' +
      '</div>' +
      '<div class="enh-whoisin-stats" id="whoisin-stats"></div>' +
      '<div class="enh-whoisin-grid" id="whoisin-grid"></div>';

    var contentArea = document.getElementById('content-area');
    if (contentArea) contentArea.appendChild(section);

    /* Live filter listeners */
    section.querySelector('#whoisin-search').addEventListener('input', renderWhoisin);
    section.querySelector('#whoisin-dept').addEventListener('change', renderWhoisin);
    section.querySelector('#whoisin-status-filter').addEventListener('change', renderWhoisin);

    if (window.lucide) lucide.createIcons();
  }

  function renderWhoisin() {
    var grid     = document.getElementById('whoisin-grid');
    var statsEl  = document.getElementById('whoisin-stats');
    var subtitle = document.getElementById('whoisin-subtitle');
    if (!grid) return;

    var todayStr = new Date().toISOString().split('T')[0];
    var allUsers = DB.users.filter(function (u) { return u.status !== 'inactive'; });
    var users    = window.ROLE ? ROLE.filterUsers(allUsers) : allUsers;

    /* Populate department filter (once) */
    var deptSel = document.getElementById('whoisin-dept');
    if (deptSel && deptSel.options.length === 1) {
      var depts = Array.from(new Set(users.map(function (u) { return u.department; }))).sort();
      depts.forEach(function (d) {
        var opt = document.createElement('option');
        opt.value = d; opt.textContent = d;
        deptSel.appendChild(opt);
      });
    }

    /* Build status map */
    var statusMap = {};
    users.forEach(function (u) {
      var rec = DB.attendance.find(function (r) {
        return r.userId === u.id && r.date === todayStr;
      });
      var onLeave = DB.leaves.find(function (l) {
        return l.userId === u.id && l.status === 'Approved' &&
               todayStr >= l.startDate && todayStr <= l.endDate;
      });

      if (onLeave) {
        statusMap[u.id] = { status: 'On Leave', clockIn: null, clockOut: null, duration: null, leaveType: onLeave.type };
      } else if (rec && rec.clockIn) {
        var dur = rec.clockOut ? window.calcDur ? calcDur(rec.clockIn, rec.clockOut) : '—' : 'Active';
        statusMap[u.id] = { status: rec.status, clockIn: rec.clockIn, clockOut: rec.clockOut, duration: dur };
      } else {
        statusMap[u.id] = { status: 'Absent', clockIn: null, clockOut: null, duration: null };
      }
    });

    /* Summary counts */
    var counts = { Present: 0, Late: 0, Absent: 0, 'On Leave': 0 };
    Object.keys(statusMap).forEach(function (id) {
      var s = statusMap[id].status;
      if (counts[s] !== undefined) counts[s]++;
    });

    if (subtitle) {
      var now = new Date();
      var t = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
      subtitle.textContent = 'Live as of ' + t + ' · ' + users.length + ' active employees';
    }

    if (statsEl) {
      statsEl.innerHTML =
        '<div class="enh-whos-stat enh-whos-present"><span class="enh-whos-num">' + counts.Present + '</span><span>Present</span></div>' +
        '<div class="enh-whos-stat enh-whos-late"><span class="enh-whos-num">' + counts.Late + '</span><span>Late</span></div>' +
        '<div class="enh-whos-stat enh-whos-absent"><span class="enh-whos-num">' + counts.Absent + '</span><span>Absent</span></div>' +
        '<div class="enh-whos-stat enh-whos-leave"><span class="enh-whos-num">' + counts['On Leave'] + '</span><span>On Leave</span></div>';
    }

    /* Filter + sort */
    var search  = (document.getElementById('whoisin-search')?.value || '').toLowerCase();
    var deptF   = document.getElementById('whoisin-dept')?.value || 'all';
    var statusF = document.getElementById('whoisin-status-filter')?.value || 'all';

    var filtered = users.filter(function (u) {
      var s = statusMap[u.id];
      var name = (u.firstName + ' ' + u.lastName).toLowerCase();
      if (search && !name.includes(search) && !(u.department||'').toLowerCase().includes(search)) return false;
      if (deptF !== 'all' && u.department !== deptF) return false;
      if (statusF !== 'all' && s.status !== statusF) return false;
      return true;
    });

    var order = { Present: 0, Late: 1, 'On Leave': 2, Absent: 3 };
    filtered.sort(function (a, b) {
      return (order[statusMap[a.id].status] || 3) - (order[statusMap[b.id].status] || 3);
    });

    if (!filtered.length) {
      grid.innerHTML = '<div class="empty-state" style="grid-column:1/-1"><p>No employees match your filter.</p></div>';
      return;
    }

    var COLORS = ['#F97316','#0D1B3E','#22C55E','#8B5CF6','#3B82F6','#F59E0B','#EF4444','#14B8A6'];
    function avatarCol(name) { return COLORS[name.charCodeAt(0) % COLORS.length]; }
    function ini(u) { return ((u.firstName||'?')[0] + (u.lastName||'?')[0]).toUpperCase(); }
    function fmt12(t) {
      if (!t || t === '—') return t || '—';
      try { var p = t.split(':').map(Number); var ampm = p[0]>=12?'PM':'AM'; var h = p[0]%12||12; return h+':'+(String(p[1]).padStart(2,'0'))+' '+ampm; } catch(e){return t;}
    }

    grid.innerHTML = filtered.map(function (u, idx) {
      var s = statusMap[u.id];
      var color = avatarCol(u.firstName);
      var sc = s.status.toLowerCase().replace(' ', '-');
      var inVal = s.clockIn ? fmt12(s.clockIn) : (s.status === 'On Leave' ? (s.leaveType || 'Leave') : '—');
      var outVal = s.clockOut ? fmt12(s.clockOut) : (s.clockIn && !s.clockOut ? 'Active' : '—');
      var isActive = s.clockIn && !s.clockOut;

      return '<div class="enh-whos-card enh-whos-' + sc + '" style="animation-delay:' + (idx * 45) + 'ms">' +
        '<div class="enh-whos-card-top">' +
          '<div class="enh-whos-avatar" style="background:' + color + '">' +
            ini(u) +
            '<div class="enh-whos-status-dot enh-dot-' + sc + '"></div>' +
          '</div>' +
          '<div class="enh-whos-info">' +
            '<div class="enh-whos-name">' + u.firstName + ' ' + u.lastName + '</div>' +
            '<div class="enh-whos-dept">' + (u.position||'') + ' · ' + (u.department||'') + '</div>' +
          '</div>' +
          '<span class="badge ' + sc + '">' + s.status + '</span>' +
        '</div>' +
        '<div class="enh-whos-times">' +
          '<div class="enh-whos-time-item"><span class="enh-whos-time-label">In</span>' +
            '<span class="enh-whos-time-val' + (isActive ? ' enh-active-time' : '') + '">' + inVal + '</span></div>' +
          '<div class="enh-whos-time-divider"></div>' +
          '<div class="enh-whos-time-item"><span class="enh-whos-time-label">Out</span>' +
            '<span class="enh-whos-time-val">' + outVal + '</span></div>' +
          '<div class="enh-whos-time-divider"></div>' +
          '<div class="enh-whos-time-item"><span class="enh-whos-time-label">Hours</span>' +
            '<span class="enh-whos-time-val">' + (s.duration || '—') + '</span></div>' +
        '</div>' +
      '</div>';
    }).join('');
  }

  /* ================================================================
     7. BIRTHDAY & WORK ANNIVERSARY ALERTS
     ================================================================ */
  function checkCelebrations() {
    if (!window.STATE || !STATE.currentUser) return;

    var now    = new Date();
    var mm     = String(now.getMonth() + 1).padStart(2, '0');
    var dd     = String(now.getDate()).padStart(2, '0');
    var todayMMDD = mm + '-' + dd;

    var users = DB.users.filter(function (u) { return u.status === 'active'; });

    users.forEach(function (u) {
      /* Birthday */
      if (u.birthday && u.birthday.length >= 10) {
        var bMMDD = u.birthday.substring(5); // 'YYYY-MM-DD' → 'MM-DD'
        if (bMMDD === todayMMDD) {
          showCelebration('birthday', u, null);
        }
      }

      /* Work anniversary */
      if (u.joinDate && u.joinDate.length >= 10) {
        var jMMDD = u.joinDate.substring(5);
        if (jMMDD === todayMMDD) {
          var years = now.getFullYear() - parseInt(u.joinDate.substring(0, 4));
          if (years > 0) showCelebration('anniversary', u, years);
        }
      }
    });
  }

  function showCelebration(type, user, years) {
    var isMe = window.STATE && user.id === STATE.currentUser?.id;
    var emoji, title, msg;

    if (type === 'birthday') {
      emoji = '🎂';
      title = isMe ? 'Happy Birthday!' : 'Happy Birthday, ' + user.firstName + '!';
      msg   = isMe
        ? 'Wishing you a wonderful day! 🎉'
        : 'Today is ' + user.firstName + ' ' + user.lastName + '\'s birthday. Send them your wishes!';
    } else {
      emoji = '🏆';
      title = isMe
        ? years + '-Year Work Anniversary!'
        : user.firstName + ' ' + user.lastName + '\'s ' + years + '-Year Anniversary!';
      msg   = isMe
        ? 'You\'ve been with ACED for ' + years + ' year' + (years > 1 ? 's' : '') + '. Thank you! 🎊'
        : user.firstName + ' ' + user.lastName + ' celebrates ' + years + ' year' + (years > 1 ? 's' : '') + ' with ACED today!';
    }

    /* Celebration toast (stays for 9 seconds) */
    var container = document.getElementById('toast-container');
    if (container) {
      var t = document.createElement('div');
      t.className = 'toast enh-celebration-toast';
      t.innerHTML =
        '<div class="enh-celebration-emoji">' + emoji + '</div>' +
        '<div class="toast-body">' +
          '<div class="toast-title">' + title + '</div>' +
          '<div class="toast-msg">' + msg + '</div>' +
        '</div>' +
        '<div class="toast-close" style="cursor:pointer;color:var(--text-muted)" onclick="this.parentElement.remove()">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
        '</div>';
      container.appendChild(t);
      setTimeout(function () { t.classList.add('removing'); setTimeout(function () { t.remove(); }, 300); }, 9000);
    }

    /* Dashboard banner */
    injectCelebrationBanner(emoji, title, msg);
  }

  function injectCelebrationBanner(emoji, title, msg) {
    var dashboard = document.getElementById('section-dashboard');
    if (!dashboard) return;

    var existing = document.getElementById('enh-celebration-banner');
    if (existing) {
      var list = existing.querySelector('.enh-celebration-list');
      if (list) {
        var item = document.createElement('div');
        item.className = 'enh-celebration-item';
        item.innerHTML = '<span class="enh-cel-emoji">' + emoji + '</span><div><strong>' + title + '</strong><p>' + msg + '</p></div>';
        list.appendChild(item);
      }
      return;
    }

    var banner = document.createElement('div');
    banner.id = 'enh-celebration-banner';
    banner.className = 'enh-celebration-banner';
    banner.innerHTML =
      '<div class="enh-celebration-header">' +
        '<span style="font-size:1rem">🎉</span>' +
        '<strong>Today\'s Celebrations</strong>' +
        '<button class="enh-cel-dismiss" onclick="document.getElementById(\'enh-celebration-banner\').remove()">&#10005;</button>' +
      '</div>' +
      '<div class="enh-celebration-list">' +
        '<div class="enh-celebration-item">' +
          '<span class="enh-cel-emoji">' + emoji + '</span>' +
          '<div><strong>' + title + '</strong><p>' + msg + '</p></div>' +
        '</div>' +
      '</div>';

    dashboard.insertBefore(banner, dashboard.firstElementChild);
  }

  /* ================================================================
     8. INJECT BIRTHDAY FIELD INTO EMPLOYEE MODAL
     ================================================================ */
  function injectBirthdayField() {
    var formGrid = document.querySelector('#employee-modal .form-grid');
    if (!formGrid || document.getElementById('emp-birthday')) return;

    var group = document.createElement('div');
    group.className = 'form-group';
    group.innerHTML =
      '<label>Date of Birth <span style="font-size:.7rem;color:var(--text-muted)">(birthday alerts)</span></label>' +
      '<input type="date" id="emp-birthday">';
    formGrid.appendChild(group);

    /* Hook into employee save to persist birthday */
    if (window.ACED && ACED.employees && ACED.employees.save) {
      var origSave = ACED.employees.save.bind(ACED.employees);
      ACED.employees.save = function () {
        var bday = document.getElementById('emp-birthday');
        if (bday && bday.value) {
          /* Store birthday on the user record before saving */
          var empId = document.getElementById('emp-modal-id')?.value;
          if (empId) {
            var u = DB.users.find(function (u) { return u.id === empId; });
            if (u) u.birthday = bday.value;
          }
        }
        origSave();
      };
    }

    /* Pre-fill birthday when editing */
    if (window.ACED && ACED.employees && ACED.employees.openEdit) {
      var origEdit = ACED.employees.openEdit.bind(ACED.employees);
      ACED.employees.openEdit = function (id) {
        origEdit(id);
        setTimeout(function () {
          var u = DB.users.find(function (u) { return u.id === id; });
          var bday = document.getElementById('emp-birthday');
          if (u && bday) bday.value = u.birthday || '';
        }, 50);
      };
    }
  }

  /* ================================================================
     9. ENHANCED TOAST WITH UNDO
     ================================================================ */
  function toastWithUndo(message, undoFn, duration) {
    duration = duration || 5000;
    var container = document.getElementById('toast-container');
    if (!container) return;

    var id = 'undo-' + Date.now();
    var toast = document.createElement('div');
    toast.id = id;
    toast.className = 'toast success enh-undo-toast';

    toast.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2" style="width:17px;height:17px;flex-shrink:0">' +
        '<polyline points="20 6 9 17 4 12"/>' +
      '</svg>' +
      '<div class="toast-body">' +
        '<div class="toast-title">' + message + '</div>' +
        '<div class="enh-undo-progress"><div class="enh-undo-bar" style="animation-duration:' + duration + 'ms"></div></div>' +
      '</div>' +
      '<button class="enh-undo-btn" id="' + id + '-undo">Undo</button>' +
      '<div class="toast-close" style="cursor:pointer;color:var(--text-muted)" onclick="document.getElementById(\'' + id + '\')?.remove()">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
      '</div>';

    container.appendChild(toast);

    var timer = setTimeout(function () {
      var el = document.getElementById(id);
      if (el) { el.classList.add('removing'); setTimeout(function () { el.remove(); }, 300); }
    }, duration);

    var undoBtn = document.getElementById(id + '-undo');
    if (undoBtn && undoFn) {
      undoBtn.addEventListener('click', function () {
        clearTimeout(timer);
        undoFn();
        var el = document.getElementById(id);
        if (el) { el.classList.add('removing'); setTimeout(function () { el.remove(); }, 300); }
      });
    }

    return id;
  }

  /* ================================================================
     10. BUTTON MICRO-ANIMATIONS
     ================================================================ */
  function attachButtonAnimations() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.btn-primary,.btn-secondary,.btn-sm-approve,.btn-sm-reject,.btn-login');
      if (!btn) return;
      btn.style.transform = 'scale(0.95)';
      setTimeout(function () { btn.style.transform = ''; }, 120);
    });
  }

  /* ================================================================
     11. SEED DEMO CELEBRATION DATA
     ================================================================ */
  function seedDemoCelebrations() {
    /* Set today as birthday for James Okafor and anniversary for Priya Naidoo
       so the feature is visible immediately in demo mode */
    if (!window.DB || !DB.users) return;
    var now = new Date();
    var mm  = String(now.getMonth() + 1).padStart(2, '0');
    var dd  = String(now.getDate()).padStart(2, '0');

    /* Birthday: James */
    var james = DB.users.find(function (u) { return u.id === 'u2'; });
    if (james && !james.birthday) james.birthday = '1990-' + mm + '-' + dd;

    /* Anniversary: Priya — 3 years ago today */
    var priya = DB.users.find(function (u) { return u.id === 'u3'; });
    if (priya) priya.joinDate = (now.getFullYear() - 3) + '-' + mm + '-' + dd;
  }

  /* ================================================================
     PUBLIC API
     ================================================================ */
  window.ACED_ENH = {
    renderWhoisin    : renderWhoisin,
    updateFABState   : updateFABState,
    toastWithUndo    : toastWithUndo,
    showCelebration  : showCelebration,
    checkCelebrations: checkCelebrations,
    triggerCountup   : triggerStatCountup
  };

  /* ================================================================
     BOOT
     ================================================================ */
  whenReady(function () {
    /* Seed demo data */
    seedDemoCelebrations();

    /* Inject persistent UI elements */
    injectMobileFAB();
    injectWhoisinSection();
    injectBirthdayField();
    attachButtonAnimations();

    /* Wrap ACED.nav.go for smooth transitions */
    wrapNavGo();

    /* Hook into auth.onLogin */
    if (ACED.auth && ACED.auth.onLogin) {
      var origLogin = ACED.auth.onLogin.bind(ACED.auth);
      ACED.auth.onLogin = async function (u) {
        await origLogin(u);
        setTimeout(function () {
          /* Celebrate birthdays / anniversaries */
          checkCelebrations();
          /* Animate initial dashboard */
          triggerStatCountup();
          animateCards('.stat-card', 80);
          animateCards('.metric-pill', 60);
          /* Clock widget arc */
          upgradeClockWidget();
          updateArcRing();
          updateFABState();
        }, 600);
      };
    }

    /* Periodic updates */
    setInterval(updateArcRing, 60000);
    setInterval(function () {
      if (window.STATE && STATE.currentSection === 'whoisin') renderWhoisin();
      updateFABState();
    }, 120000);

    console.info('%c[ACED Enhancements] Loaded ✓', 'color:#F97316;font-weight:bold;font-size:12px');
  });

})();
