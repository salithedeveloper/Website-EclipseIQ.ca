#!/usr/bin/env python3
"""Render a sharing card with the unmodified original logo and verified fonts.
Requires Playwright and Chromium only when regenerating, never at runtime.
All asset requests are fulfilled locally; no external services are contacted.
"""
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
HTML='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Plex;src:url('https://eclipseiq.ca/assets/fonts/plex-regular.woff2')}@font-face{font-family:Condensed;src:url('https://eclipseiq.ca/assets/fonts/plex-condensed.woff2')}
*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#f0f6f8;color:#023047;font-family:Plex,Arial,sans-serif}.top{height:134px;background:white;padding:23px 64px}.top img{width:202px;height:88px}.content{padding:42px 64px}p{font-size:14px;letter-spacing:2px;color:#07688b;margin:0 0 24px}h1{font:500 76px/1.05 Condensed,Arial,sans-serif;letter-spacing:-1.5px;margin:0}h1 span{color:#087bad}.bottom{position:absolute;left:64px;right:64px;bottom:37px;border-top:1px solid #bfd5df;padding-top:20px;font-size:18px;display:flex;justify-content:space-between}.bar{position:absolute;top:134px;bottom:0;right:0;width:12px;background:#13a8ff}
</style></head><body><div class="top"><img src="https://eclipseiq.ca/assets/eclipseiq-logo-original.png" alt="EclipseIQ Technologies Inc."></div><div class="content"><p>INSURANCE TECHNOLOGY CONSULTING & SOFTWARE SOLUTIONS</p><h1>Insurance expertise.<br>Technology leadership.<br><span>Practical solutions.</span></h1></div><div class="bottom"><span>Advisory · Leadership · Software</span><span>eclipseiq.ca</span></div><div class="bar"></div></body></html>'''
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('ECLIPSEIQ_CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
 def local(route):
  path=(ROOT/urlparse(route.request.url).path.lstrip('/')).resolve()
  if not path.is_relative_to(ROOT) or not path.is_file():route.abort();return
  route.fulfill(body=path.read_bytes(),content_type='font/woff2' if path.suffix=='.woff2' else 'image/png')
 page.route('**/*',local);page.set_content(HTML);page.evaluate('document.fonts.ready');page.screenshot(path=str(ROOT/'assets/social.png'));browser.close()
print('Generated assets/social.png with the original logo and verified brand palette')
