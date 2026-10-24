#!/usr/bin/env python3
"""Capture and verify the local homepage concepts. Requires Playwright + Chromium.
Start: python -m http.server 4173 --directory review/homepage-concepts
Run: python review/homepage-concepts/capture.py
No external services are called or submitted to.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, os
ROOT=Path(__file__).resolve().parent
BASE=os.environ.get('CONCEPT_REVIEW_URL','http://127.0.0.1:4173')
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(device_scale_factor=1)
 errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
 for n in (1,2,3):
  for width in (1440,1024,768,390,320):
   page.set_viewport_size({'width':width,'height':1000 if width>700 else 844})
   response=page.goto(f'{BASE}/concept-{n}.html',wait_until='networkidle')
   page.evaluate('document.fonts.ready')
   assert response.status==200
   assert page.locator('h1').count()==1
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Overflow: {n} / {width}'
   assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
   for href in page.locator('a[href^="#"]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))'):
    if href!='#':assert page.locator(href).count(),href
   if width<=700:
    page.get_by_role('button',name='Menu').click()
    assert page.locator('#navigation').is_visible()
    assert page.locator('.menu').get_attribute('aria-expanded')=='true'
    page.keyboard.press('Escape')
    assert not page.locator('#navigation').is_visible()
    page.get_by_role('button',name='Menu').click()
    page.locator('#navigation a[href="#capabilities"]').click()
    assert not page.locator('#navigation').is_visible()
    page.evaluate('window.scrollTo(0,0)');page.wait_for_timeout(250)
   if width in (1440,390):
    kind='desktop' if width==1440 else 'mobile'
    page.screenshot(path=str(ROOT/f'screenshots/concept-{n}-{kind}.png'),full_page=True)
   results.append({'concept':n,'width':width,'http':response.status,'overflow':False,'images':'loaded','navigation':'passed'})
 page.set_viewport_size({'width':1440,'height':1050})
 page.goto(BASE+'/index.html',wait_until='networkidle')
 page.select_option('#right','3')
 assert page.locator('#right-image').get_attribute('src')=='screenshots/concept-3-desktop.png'
 page.select_option('#right','2')
 assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
 page.screenshot(path=str(ROOT/'screenshots/comparison-desktop.png'),full_page=True)
 page.screenshot(path=str(ROOT/'screenshots/comparison-overview.png'))
 for width in (390,320):
  page.set_viewport_size({'width':width,'height':844})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Review overflow'
 assert not errors,errors
 browser.close()
(ROOT/'validation.json').write_text(json.dumps({'browser':'Chromium','checks':results,'review':'comparison selectors, images and responsive layout passed','page_errors':errors},indent=2)+'\n')
print(f'PASS: {len(results)} concept/viewport checks; comparison controls; desktop/mobile screenshots; no browser errors.')
