#!/usr/bin/env python3
"""Render the corporate share card using the unchanged original logo and local font.
Playwright/Chromium are development-only; every asset request is served from disk.
"""
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
HTML='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Manrope;src:url('https://eclipseiq.ca/assets/fonts/manrope.woff2');font-weight:200 800}*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#071f2c;color:white;font-family:Manrope,Arial,sans-serif}.top{position:absolute;top:30px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center}.logo{background:white;padding:7px 10px;line-height:0}.logo img{width:166px;height:auto}.top span{font-size:12px;letter-spacing:1.5px;color:#a5b7c0}.title{position:absolute;top:182px;left:60px}h1{font-size:64px;line-height:1.15;font-weight:650;letter-spacing:-2px;margin:0}h1 span{color:#13a8ff}.bottom{position:absolute;left:60px;right:60px;bottom:38px;border-top:1px solid #344954;padding-top:23px;font-size:13px;display:flex;justify-content:space-between;color:#b1c5d0}
</style></head><body><div class="top"><div class="logo"><img src="https://eclipseiq.ca/assets/eclipseiq-logo-original.png" alt="EclipseIQ Technologies Inc."></div><span>ECLIPSEIQ TECHNOLOGIES INC.</span></div><div class="title"><h1>Insurance technology.<br><span>Software, consulting<br>and senior leadership.</span></h1></div><div class="bottom"><span>Consulting. Leadership. Software.</span><span>eclipseiq.ca</span></div></body></html>'''
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('ECLIPSEIQ_CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
 def local(route):
  path=(ROOT/urlparse(route.request.url).path.lstrip('/')).resolve()
  if not path.is_relative_to(ROOT) or not path.is_file():route.abort();return
  route.fulfill(body=path.read_bytes(),content_type='font/woff2' if path.suffix=='.woff2' else 'image/png')
 page.route('**/*',local);page.set_content(HTML);page.evaluate('document.fonts.ready');page.screenshot(path=str(ROOT/'assets/social.png'));browser.close()
print('Generated corporate sharing card')
