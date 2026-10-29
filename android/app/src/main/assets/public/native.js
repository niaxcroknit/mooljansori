/* 물잔소리 — 안드로이드 앱 연결
 * 웹 화면(index.html)은 그대로 두고, 앱에서만 필요한 것을 여기서 붙여요.
 *  - 기록 저장: 기기 저장소(Preferences)에 한 번 더 저장해서 지워지지 않게
 *  - 진동: 컵을 누를 때 톡
 *  - 알림: 폰이 잠겨 있어도 울리는 예약 알림 (앞으로 최대 2주치를 미리 예약)
 *  - 앱을 켜 둔 채 알림이 오면 화면 가운데 반투명 물컵(HUD)
 *  - 하단 배너 광고 (AdMob)
 */
(function () {
  var C = window.Capacitor;
  if (!C || !C.isNativePlatform || !C.isNativePlatform()) return;
  var reg = window.capacitorExports.registerPlugin;
  var LN = reg('LocalNotifications');
  var HP = reg('Haptics');
  var PF = reg('Preferences');

  var KEY = 'hanmogeum-v1'; // index.html이 쓰는 저장 이름과 같아야 해요
  var IDS_KEY = 'mjs-scheduled-ids';

  // 1) 저장: 앱 시작 때 기기 저장소 → 화면 저장소로 옮긴 뒤 화면을 그려요
  window.__nativeReady = PF.get({ key: KEY })
    .then(function (r) {
      if (r && r.value) { try { localStorage.setItem(KEY, r.value); } catch (e) {} }
    })
    .catch(function () {});
  var saveTimer = null;
  window.__nativeSave = function (json) {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { PF.set({ key: KEY, value: json }).catch(function () {}); }, 300);
  };

  // 2) 진동
  window.__haptic = function () { HP.impact({ style: 'LIGHT' }).catch(function () {}); };

  // 3) 알림
  var NAGS = [
    '물 마실 시간이야. 딱 한 컵만.',
    '목 마르기 전에 마시는 거야.',
    '커피 말고 물. 알지?',
    '지금 한 컵 마시면 저녁이 편해.',
    '물잔 비었다. 채우러 가자.',
    '잔소리 듣기 싫으면 미리 마시기.'
  ];
  function toMin(v) {
    if (typeof v === 'number') return v;
    var p = String(v || '').split(':');
    return Number(p[0]) * 60 + Number(p[1] || 0);
  }
  function slotsOf(s) {
    var st = toMin(s.start || '08:00'), en = toMin(s.end || '22:00'), iv = Number(s.interval) || 60, out = [];
    if (en <= st) return out;
    for (var m = st; m <= en; m += iv) out.push(m);
    return out;
  }
  // 다음 알림 시각 (화면의 "다음 알림" 칸)
  window.__nextSlot = function (s) {
    if (!s || !s.remOn) return null;
    var slots = slotsOf(s); if (!slots.length) return null;
    var now = new Date();
    for (var d = 0; d < 2; d++) {
      for (var i = 0; i < slots.length; i++) {
        var t = new Date(now.getFullYear(), now.getMonth(), now.getDate() + d, Math.floor(slots[i] / 60), slots[i] % 60, 0, 0);
        if (t.getTime() > now.getTime()) return t.getTime();
      }
    }
    return null;
  };

  var channelsReady = null;
  function ensureChannels() {
    if (!channelsReady) {
      channelsReady = Promise.all([
        LN.createChannel({ id: 'reminders', name: '물 마시기 알림', description: '정해 둔 시각에 울리는 물 마시기 알림', importance: 4, vibration: true, visibility: 1 }),
        LN.createChannel({ id: 'reminders-quiet', name: '물 마시기 알림 (무음)', description: '소리 없이 오는 물 마시기 알림', importance: 2, vibration: false, visibility: 1 })
      ]).catch(function () {});
    }
    return channelsReady;
  }

  function permission() {
    return LN.checkPermissions().then(function (p) {
      if (p.display === 'granted') return true;
      if (p.display === 'denied') return false;
      return LN.requestPermissions().then(function (r) { return r.display === 'granted'; });
    }).catch(function () { return false; });
  }

  function cancelOld() {
    var ids = [];
    try { ids = JSON.parse(localStorage.getItem(IDS_KEY) || '[]'); } catch (e) {}
    return LN.getPending().then(function (r) {
      (r.notifications || []).forEach(function (n) { if (ids.indexOf(n.id) < 0) ids.push(n.id); });
    }).catch(function () {}).then(function () {
      if (!ids.length) return;
      return LN.cancel({ notifications: ids.map(function (id) { return { id: id }; }) }).catch(function () {});
    }).then(function () { try { localStorage.setItem(IDS_KEY, '[]'); } catch (e) {} });
  }

  var running = Promise.resolve();
  // 알림 예약을 설정에 맞게 다시 만들어요. 'off' | 'on' | 'denied' 를 돌려줘요.
  window.__reschedule = function (s, opts) {
    opts = opts || {};
    running = running.then(function () {
      return cancelOld().then(function () {
        if (!s || !s.remOn) return 'off';
        return (opts.ask === false ? LN.checkPermissions().then(function (p) { return p.display === 'granted'; }) : permission())
          .then(function (ok) {
            if (!ok) return 'denied';
            return ensureChannels().then(function () {
              var slots = slotsOf(s);
              if (!slots.length) return 'on';
              var days = Math.max(1, Math.min(14, Math.floor(200 / slots.length)));
              var now = Date.now(), base = new Date(), list = [], n = 0;
              for (var d = 0; d < days; d++) {
                for (var i = 0; i < slots.length; i++) {
                  var t = new Date(base.getFullYear(), base.getMonth(), base.getDate() + d, Math.floor(slots[i] / 60), slots[i] % 60, 0, 0);
                  if (t.getTime() <= now + 30000) continue;
                  list.push({
                    id: 1000 + d * 100 + i,
                    title: '물 좀 마셔!',
                    body: NAGS[n++ % NAGS.length],
                    channelId: s.sound === false ? 'reminders-quiet' : 'reminders',
                    smallIcon: 'ic_stat_glass',
                    largeIcon: 'ic_notif_glass',
                    iconColor: '#3F78DC',
                    schedule: { at: t, allowWhileIdle: true },
                    isExactNotification: false
                  });
                }
              }
              if (!list.length) return 'on';
              return LN.schedule({ notifications: list }).then(function () {
                try { localStorage.setItem(IDS_KEY, JSON.stringify(list.map(function (x) { return x.id; }))); } catch (e) {}
                return 'on';
              });
            });
          });
      }).catch(function () { return 'error'; });
    });
    return running;
  };

  // 설정 화면의 "5초 뒤 알림 보내 보기"
  window.__testNotification = function (s) {
    return permission().then(function (ok) {
      if (!ok) return false;
      return ensureChannels().then(function () {
        return LN.schedule({ notifications: [{
          id: 999,
          title: '물 좀 마셔!',
          body: NAGS[Math.floor(Math.random() * NAGS.length)],
          channelId: s && s.sound === false ? 'reminders-quiet' : 'reminders',
          smallIcon: 'ic_stat_glass',
          largeIcon: 'ic_notif_glass',
          iconColor: '#3F78DC',
          schedule: { at: new Date(Date.now() + 5000), allowWhileIdle: true },
          isExactNotification: false
        }] }).then(function () { return true; });
      });
    }).catch(function () { return false; });
  };

  // 4) 하단 배너 광고 (AdMob)
  //   앱 ID는 AndroidManifest.xml, 광고 단위 ID는 여기에 있어요.
  var AD_UNIT = 'ca-app-pub-2486517051650098/3025809421';
  var AM = reg('AdMob');
  function setAdH(h) { document.documentElement.style.setProperty('--ad-h', (Number(h) || 0) + 'px'); }
  setAdH(0);
  AM.addListener('bannerAdSizeChanged', function (sz) { setAdH(sz && sz.height); });
  AM.addListener('bannerAdFailedToLoad', function () { setAdH(0); });
  window.__adPrivacyRequired = false;
  window.__adPrivacy = function () { return AM.showPrivacyOptionsForm().catch(function () {}); };
  (async function () {
    await AM.initialize({ maxAdContentRating: 'Teen' });
    // 유럽 등 동의가 필요한 지역에서만 동의 창이 떠요
    var info = await AM.requestConsentInfo();
    if (info.isConsentFormAvailable && info.status === 'REQUIRED') info = await AM.showConsentForm();
    window.__adPrivacyRequired = info.privacyOptionsRequirementStatus === 'REQUIRED';
    document.dispatchEvent(new Event('mjs-ad-privacy'));
    if (info.canRequestAds) {
      await AM.showBanner({ adId: AD_UNIT, adSize: 'ADAPTIVE_BANNER', position: 'BOTTOM_CENTER', margin: 0 });
    }
  })().catch(function () { setAdH(0); });

  // 앱을 켜 둔 상태에서 알림이 오면 반투명 물컵을 띄워요
  LN.addListener('localNotificationReceived', function (n) {
    if (window.__showHud) window.__showHud((n && n.title) || '물 좀 마셔!');
  });
})();
