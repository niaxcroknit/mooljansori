#!/usr/bin/env python3
"""src/water.html(화면 원본)으로 Netlify용 웹 사이트 web/index.html을 만들어요.
사용법:  python3 tools/build_web.py   →  web 폴더를 Netlify Deploys에 끌어다 놓기"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
HEAD = '<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#eef3fb" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0e1526" media="(prefers-color-scheme: dark)"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="물잔소리"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="description" content="물 마신 걸 기록하고 잔소리로 알려 주는 앱"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
body = (ROOT / 'src' / 'water.html').read_text(encoding='utf-8')
(ROOT / 'web' / 'index.html').write_text(HEAD + '\n' + body + '\n</body></html>\n', encoding='utf-8')
print('ok', ROOT / 'web' / 'index.html')
