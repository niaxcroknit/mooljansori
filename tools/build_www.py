#!/usr/bin/env python3
"""src/water.html(화면 원본)으로 안드로이드 앱 화면 www/index.html을 만들어요.
화면을 고친 뒤:  python3 tools/build_www.py  →  npx cap sync android"""
import re, sys

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src' / 'water.html'
OUT = ROOT / 'www' / 'index.html'
s = open(SRC, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    if n != count:
        sys.exit(f'패턴을 {count}번 찾아야 하는데 {n}번 찾았어요: {a[:70]!r}')
    s = s.replace(a, b)

# 1) 인터넷 글꼴 → 앱에 내장한 글꼴
s = re.sub(r'<link rel="preconnect"[^>]*>\n', '', s)
s, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', '<link rel="stylesheet" href="fonts/fonts.css">', s)
assert n == 1, 'google fonts link'

# 2) 상태바·내비게이션바 영역 (안드로이드 edge-to-edge)
rep("bottom:calc(20px + env(safe-area-inset-bottom,0px))", "bottom:calc(20px + var(--ad-h,0px) + var(--safe-area-inset-bottom, env(safe-area-inset-bottom,0px)))")

# 3) 앱 전용 스타일: 웹 전용 요소 숨기기 + 반투명 물컵(HUD)
rep("@media (prefers-reduced-motion: reduce){*{transition:none!important}", """/* ---- 앱 전용 ---- */
.native #notif-btn,.native .web-only,.native #banner{display:none!important}
.app-only{display:none}
.native .app-only{display:revert}
.native button.app-only{display:block}
.native .grid2 > label.f:first-child{grid-column:1/-1}
/* 하단 배너 광고 자리: 광고 높이(--ad-h)만큼 아래를 비워 둬요 */
.native body{padding-bottom:var(--ad-h,0px)}
.native .history{padding-bottom:calc(var(--ad-h,0px) + var(--safe-area-inset-bottom, env(safe-area-inset-bottom,0px)))}
.hud{position:fixed;inset:0;z-index:80;display:grid;place-items:center;pointer-events:none}
.hud-card{width:172px;height:172px;border-radius:36px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;
  background:var(--g-bg-hi);-webkit-backdrop-filter:blur(26px) saturate(170%);backdrop-filter:blur(26px) saturate(170%);
  border:1px solid var(--g-edge);box-shadow:inset 0 1px 0 var(--g-hi),0 24px 60px -20px var(--g-shadow);
  opacity:0;transform:scale(.86);transition:opacity .32s ease,transform .32s cubic-bezier(.3,1.4,.5,1)}
.hud.show .hud-card{opacity:1;transform:scale(1)}
.hud-card svg{height:96px;width:auto;overflow:visible}
.hud-card b{font-family:var(--f-display);font-weight:400;font-size:18px;color:var(--ink)}
@media (prefers-reduced-motion: reduce){*{transition:none!important}""")

# 4) 알림 설명 문구 (앱은 꺼져 있어도 울려요)
rep('<div><div>알림 켜기</div><div class="note">마지막으로 마신 시각부터 간격을 셉니다.</div></div>',
    '<div><div>알림 켜기</div><div class="note web-only">마지막으로 마신 시각부터 간격을 셉니다.</div><div class="note app-only">시작부터 끝 시각까지 간격마다 울려요.</div></div>')
rep('<p class="note" style="margin:0">알림은 이 페이지가 열려 있을 때 울려요. 휴대폰에서는 탭을 열어 두세요.</p>',
    '<p class="note web-only" style="margin:0">알림은 이 페이지가 열려 있을 때 울려요. 휴대폰에서는 탭을 열어 두세요.</p>\n'
    '      <button id="test-notif" class="app-only" type="button">5초 뒤 알림 보내 보기</button>\n'
    '      <p class="note app-only" style="margin:0">앱을 꺼 두거나 폰이 잠겨 있어도 정해진 시각에 울려요.</p>\n'
    '      <button id="ad-privacy" class="app-only" type="button" hidden>광고 개인정보 설정</button>')
rep('<label class="f">알림에서 기록할 컵', '<label class="f web-only">알림에서 기록할 컵')

# 5) 반투명 물컵(HUD) 자리
rep('<div class="toast" id="toast" role="status"></div>', '''<div class="toast" id="toast" role="status"></div>
<div class="hud" id="hud" hidden aria-live="assertive">
  <div class="hud-card">
    <svg viewBox="0 0 72 116" aria-hidden="true">
      <defs>
        <clipPath id="hud-cav"><path d="M5.8 7 H66.2 L60.9 97 Q60.7 100 57.8 100 H14.2 Q11.3 100 11.1 97 Z"/></clipPath>
        <linearGradient id="hud-w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--water)"/><stop offset="1" style="stop-color:var(--water-deep)"/></linearGradient>
      </defs>
      <path d="M3 5 H69 L63 107 Q62.6 112 57.6 112 H14.4 Q9.4 112 9 107 Z" style="fill:var(--g-bg);stroke:color-mix(in srgb,var(--accent) 35%,var(--g-edge))" stroke-width="1.4"/>
      <g clip-path="url(#hud-cav)"><rect x="0" y="42" width="72" height="80" fill="url(#hud-w)"/>
        <path d="M0 42 Q9 44 18 42 T36 42 T54 42 T72 42" fill="none" style="stroke:var(--g-hi)" stroke-width=".8"/></g>
      <path d="M11.4 101.5 H60.6 L62.4 106 Q62.2 110.2 57.6 110.2 H14.4 Q9.8 110.2 9.6 106 Z" style="fill:var(--g-hi)" opacity=".4"/>
      <path d="M8.6 13 L13 92" style="stroke:var(--g-hi)" stroke-width="3.2" stroke-linecap="round" opacity=".8"/>
      <path d="M3.6 5 H68.4" style="stroke:var(--g-hi)" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
    <b id="hud-text">물 좀 마셔!</b>
  </div>
</div>''')

# 6) 스크립트 연결
rep("<script>\n(function(){", """<script src="capacitor.js"></script>
<script src="native.js"></script>
<script>
(function(){
  const NATIVE = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());
  if(NATIVE) document.documentElement.classList.add('native');""")
# 저장할 때 기기 저장소에도
rep("function lsSave(){ try{ localStorage.setItem(LS, JSON.stringify({settings:state.settings, days:state.days})); }catch(e){} }",
    "function lsSave(){ const json = JSON.stringify({settings:state.settings, days:state.days}); try{ localStorage.setItem(LS, json); }catch(e){} if(window.__nativeSave) window.__nativeSave(json); }")
# 상태 문구
rep("if(!window.claude || !window.claude.use){ $('status').textContent = '이 브라우저에만 저장돼요'; return; }",
    "if(!window.claude || !window.claude.use){ $('status').textContent = NATIVE ? '기록은 이 폰에만 저장돼요' : '이 브라우저에만 저장돼요'; if(NATIVE) syncReminders(false); return; }")
# 진동
rep("    splash(originEl, ml);\n", "    splash(originEl, ml);\n    if(window.__haptic) window.__haptic();\n")
# 설정이 바뀌면 알림 다시 예약
rep("function setSetting(patch){ Object.assign(state.settings, patch); saveSettings(); render(); }",
    """function setSetting(patch){ Object.assign(state.settings, patch); saveSettings(); render();
    if(NATIVE && ['remOn','interval','start','end','sound'].some(k => k in patch)) syncReminders(!!patch.remOn); }
  let syncTimer = null;
  function syncReminders(ask){
    if(!NATIVE || !window.__reschedule) return;
    clearTimeout(syncTimer);
    syncTimer = setTimeout(async () => {
      const r = await window.__reschedule(state.settings, {ask});
      if(r === 'denied' && state.settings.remOn){
        if(ask) toast('알림이 꺼져 있어. 폰 설정 → 앱 → 물잔소리 → 알림을 켜 줘');
        Object.assign(state.settings, {remOn:false}); saveSettings(); render();
      }
    }, ask ? 0 : 400);
  }
  if(NATIVE){
    document.addEventListener('visibilitychange', () => { if(!document.hidden && state.settings.remOn) syncReminders(false); });
    $('test-notif').addEventListener('click', async () => {
      const ok = window.__testNotification && await window.__testNotification(state.settings);
      toast(ok ? '5초 뒤에 울려. 지금 화면을 꺼 봐' : '알림이 꺼져 있어. 폰 설정에서 켜 줘');
    });
    const syncAdPrivacy = () => { $('ad-privacy').hidden = !window.__adPrivacyRequired; };
    document.addEventListener('mjs-ad-privacy', syncAdPrivacy); syncAdPrivacy();
    $('ad-privacy').addEventListener('click', () => window.__adPrivacy && window.__adPrivacy());
    let hudTimer = null;
    window.__showHud = (msg) => {
      const h = $('hud'); $('hud-text').textContent = msg || '물 좀 마셔!';
      h.hidden = false; requestAnimationFrame(() => h.classList.add('show'));
      clearTimeout(hudTimer);
      hudTimer = setTimeout(() => { h.classList.remove('show'); setTimeout(() => { h.hidden = true; }, 380); }, 2900);
    };
  }""")
# 다음 알림: 앱은 정해진 시각마다
rep("  function updateNext(){\n    const due = nextDue();",
    "  function updateNext(){\n    const due = NATIVE ? (window.__nextSlot ? window.__nextSlot(state.settings) : null) : nextDue();")
# 화면 안 배너 알림은 웹에서만 (앱은 진짜 알림이 울려요)
rep("    if(due && Date.now() >= due && $('banner').hidden) fire();", "    if(!NATIVE && due && Date.now() >= due && $('banner').hidden) fire();")
# 브라우저 알림 버튼은 웹에서만
rep("    if('Notification' in window && Notification.permission === 'default'){", "    if(!NATIVE && 'Notification' in window && Notification.permission === 'default'){")
# 저장소를 먼저 불러온 뒤 시작
rep("  connect();\n})();", "  (window.__nativeReady || Promise.resolve()).then(connect);\n})();")

HEAD = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<style>
:root{color-scheme:light;
  padding-top:var(--safe-area-inset-top, env(safe-area-inset-top,0px));
  padding-bottom:var(--safe-area-inset-bottom, env(safe-area-inset-bottom,0px));
  padding-left:var(--safe-area-inset-left, env(safe-area-inset-left,0px));
  padding-right:var(--safe-area-inset-right, env(safe-area-inset-right,0px))}
body{margin:0;font:14px system-ui,sans-serif;-webkit-tap-highlight-color:transparent;overscroll-behavior-y:none}
img{max-width:100%}[hidden]{display:none!important}
</style></head><body>
'''
open(OUT, 'w', encoding='utf-8').write(HEAD + s + '\n</body></html>\n')
print('ok', OUT, len(s))
