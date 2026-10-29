# 물잔소리 💧

물 마신 걸 기록하면 유리잔에 물이 차오르고, 잊을 때쯤 잠금화면으로 잔소리해 주는 물 마시기 앱이에요.

- 앱 ID: `com.nia.mooljansori`
- 현재 버전: **1.1.0** (versionCode 4)
- 웹 버전: https://mooljansori.netlify.app

## 주요 기능

- 내 컵(머그, 텀블러 등)을 등록해서 버튼 한 번으로 기록
- 커피·차 같은 음료는 수분 인정률만큼, 술은 마신 만큼 빼서 계산
- 콤부차, 믹스커피 등 내 음료 직접 추가
- 정해 둔 간격과 시간대에 잠금화면 알림
- 최근 7일 그래프, 달력으로 지난 기록 보기
- 소라색 글래스 디자인, 다크 모드
- 하단 배너 광고 (Google AdMob)

## 폴더 구성

| 폴더·파일 | 내용 |
|---|---|
| `src/water.html` | **화면 원본.** 화면을 고칠 때는 이 파일 하나만 고쳐요 |
| `android/` | Android Studio 프로젝트 |
| `www/` | 앱에 들어가는 화면 (src에서 자동으로 만들어요) |
| `www/native.js` | 앱 전용 기능: 알림, 진동, 기기 저장, 광고 |
| `web/` | Netlify에 올리는 웹 사이트 (개인정보처리방침, app-ads.txt 포함) |
| `store/` | 플레이스토어 자료: 스크린샷, 그래픽 이미지, 등록 안내서 |
| `assets/` | 아이콘·스플래시 원본 |
| `tools/` | 화면 원본으로 앱·웹 화면을 만드는 스크립트 |
| `node_modules/@capacitor*` | Android Studio가 바로 열 수 있게 넣어 둔 안드로이드 부품 |

## 스토어용 파일(.aab) 만들기

1. 이 저장소를 내려받아요. (GitHub 화면의 **Code → Download ZIP** 후 압축 풀기)
2. Android Studio에서 **File → Open** → **`android`** 폴더 선택
3. 아래쪽 진행 막대가 멈출 때까지 기다리기
4. **Build → Generate Signed App Bundle or APK… → Android App Bundle**
5. 열쇠는 **Choose existing…**으로 `mooljansori-key`를 고르고 비밀번호 입력
6. **release → Create** → `android/app/release/app-release.aab`

> ⚠️ 앱 서명 열쇠(`mooljansori-key`)는 이 저장소에 **절대 올리지 마세요.** `.gitignore`로 막아 두었어요. 열쇠는 구글 드라이브 등 따로 안전한 곳에 보관하세요.

## 업데이트할 때

1. `src/water.html`을 고쳐요. (알림·광고 같은 앱 전용 기능은 `www/native.js`)
2. 화면 다시 만들기
   ```
   python3 tools/build_www.py
   python3 tools/build_web.py
   npx cap sync android
   ```
3. `android/app/build.gradle`의 `versionCode`를 1 올리고 `versionName`을 바꿔요.
4. 위 "스토어용 파일 만들기"대로 새 .aab를 만들어 Play Console에 올려요.

## 버전 기록

| 버전 | versionCode | 내용 |
|---|---|---|
| 1.1.0 | 4 | 하단 배너 광고 (AdMob) |
| 1.0.2 | 3 | 달력으로 지난 기록 보기 |
| 1.0.1 | 2 | 하루 목표 직접 입력, 지운 기록 되돌리기 |
| 1.0.0 | 1 | 첫 출시 |
