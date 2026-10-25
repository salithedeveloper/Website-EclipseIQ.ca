#!/usr/bin/env python3
"""Behavior checks with entirely intercepted provider requests. No real submissions.
Requires Playwright and Chromium. Start python -m http.server 4173 first.
"""
from pathlib import Path
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright
import json, re, time, os
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('ECLIPSEIQ_TEST_URL','http://127.0.0.1:4173')
CHROME=os.environ.get('ECLIPSEIQ_CHROMIUM','/usr/bin/chromium')
RESULTS=ROOT/'.test-results'; RESULTS.mkdir(exist_ok=True)
count=0

def ok(condition,label):
 global count
 assert condition,label
 count+=1;print('PASS:',label)

def fill(page):
 page.locator('#name').fill('  Test Reviewer  ')
 page.locator('#email').fill('reviewer@example.test')
 page.locator('#company').fill('Test Organization')
 page.locator('#interest').select_option('consulting')
 page.locator('#message').fill('A test inquiry about system integration.')

def configure(ctx, mode='production', endpoint='https://formspree.io/f/TESTONLY', result='success', ga='', captcha='', required=False, response='success', local_production=False, captcha_state='blocked', actual_config=False):
 requests=[];errors=[]
 config={'form':{'mode':mode,'endpoint':endpoint,'developmentResult':result,'allowLocalProduction':local_production,'requireRecaptcha':required,'recaptchaSiteKey':captcha},'analytics':{'measurementId':ga}}
 def handler(route):
  u=urlparse(route.request.url)
  if u.hostname in ['eclipseiq.ca','127.0.0.1','localhost']:
   if u.path.endswith('/assets/config.js') or u.path=='/assets/config.js':
    route.fulfill(content_type='text/javascript',body=(ROOT/'assets/config.js').read_text() if actual_config else 'window.ECLIPSEIQ_CONFIG='+json.dumps(config));return
   path=(ROOT/unquote(u.path).lstrip('/')).resolve()
   if not path.is_relative_to(ROOT):route.abort();return
   if path.is_dir():path/= 'index.html'
   if path.exists():
    mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.woff2':'font/woff2'}.get(path.suffix,'text/plain')
    route.fulfill(content_type=mime,body=path.read_bytes());return
   route.fulfill(status=404,body='not found');return
  requests.append(route.request)
  if u.hostname=='formspree.io':
   if response=='success':route.fulfill(content_type='application/json',body='{"ok":true}')
   elif response=='ambiguous':route.fulfill(content_type='application/json',body='{}')
   elif response=='malformed':route.fulfill(content_type='text/plain',body='broken')
   elif response=='reject-ok':route.fulfill(status=400,content_type='application/json',body='{"ok":true}')
   elif response=='rate':route.fulfill(status=429,content_type='application/json',body='{"ok":false}')
   elif response=='network':route.abort('failed')
   return
  if u.hostname=='www.googletagmanager.com':route.fulfill(content_type='text/javascript',body='/* GA provider stub: never sends requests */');return
  if u.hostname=='www.google.com':
   if captcha_state=='blocked':route.abort('failed');return
   stub="""window.grecaptcha={render:(id,opts)=>{window.__captchaOptions=opts;const label=document.createElement('label');label.textContent="I'm not a robot";const box=document.createElement('input');box.type='checkbox';box.id='mock-recaptcha';label.prepend(box);document.getElementById(id).append(label);return 0;},getResponse:()=>document.getElementById('mock-recaptcha')?.checked?'TEST-CAPTCHA-TOKEN':'',reset:()=>{document.getElementById('mock-recaptcha').checked=false;window.__captchaResets=(window.__captchaResets||0)+1;}};window.eclipseIQCaptchaReady();"""
   route.fulfill(content_type='text/javascript',body=stub);return
  errors.append(route.request.url);route.abort()
 ctx.route('**/*',handler)
 return requests,errors

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
 # Real static server: links, rendering and runtime errors at all sizes.
 ctx=browser.new_context();page=ctx.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
 paths=['/','/products/index.html','/services/index.html','/about/index.html','/faq/index.html','/contact/index.html','/privacy-policy/index.html','/404.html','/privacy/index.html','/cookie-policy-ca/index.html','/cookie-policy-ca-2/index.html']
 for width in [1440,1024,768,390,320]:
  page.set_viewport_size({'width':width,'height':900})
  for path in paths:
   page.goto(BASE+path)
   ok(page.locator('h1').count()==1,f'{width}px {path} loads')
   ok(page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'{width}px {path} no horizontal overflow')
   if width<=850:
    page.get_by_role('button',name=re.compile('Menu')).click()
    ok(page.locator('#navigation').is_visible(),'mobile navigation opens')
    page.keyboard.press('Escape')
    ok(not page.locator('#navigation').is_visible(),'Escape closes mobile navigation')
   else:ok(not page.locator('.menu-toggle').is_visible(),'desktop menu toggle hidden')
  page.goto(BASE+'/')
  page.locator('[data-cookie-choice="rejected"]').click() if page.locator('#cookie-banner').is_visible() else None
  if width in [1440,390]:page.screenshot(path=str(RESULTS/f'home-{width}.png'),full_page=True)
 page.goto(BASE+'/')
 logo=page.locator('.header .brand img')
 ok(logo.evaluate('(e)=>e.naturalWidth===202 && e.naturalHeight===88'),'actual corporate logo loads with original proportions')
 page.goto(BASE+'/contact/index.html')
 ok(page.locator('input:not([type=hidden]),select,textarea').evaluate_all("els=>els.every(e=>e.labels && e.labels.length > 0)"),'every form field has a programmatic label')
 ok(not errs,'no page JavaScript errors')
 page.goto(BASE+'/faq/index.html');page.locator('summary').first.click();ok(page.locator('details').first.get_attribute('open') is not None,'FAQ expands')
 page.goto(BASE+'/contact/index.html');fill(page)
 page.get_by_role('button',name='Send inquiry').click();page.wait_for_timeout(500)
 ok('SIMULATED SUCCESS' in page.locator('#form-status').inner_text(),'local success explicitly simulated')
 ok(page.locator('#name').input_value()=='Test Reviewer','required text trimmed; simulated entries preserved')
 ctx.close()
 # Concise corporate content and native disclosure behaviour.
 ctx=browser.new_context();page=ctx.new_page();page.goto(BASE+'/')
 page.locator('[data-cookie-choice="rejected"]').click() if page.locator('#cookie-banner').is_visible() else None
 ok(page.locator('#navigation a').all_text_contents()==['Products','Services','About','FAQ','Contact'],'navigation exposes the five requested destinations')
 ok(page.locator('.business-path').count()==2,'both business areas have dedicated entry points')
 page.locator('.business-path').first.click();page.wait_for_url('**/products/index.html')
 ok(page.locator('.product-catalog').is_visible(),'product entry opens the public catalogue')
 page.go_back();page.locator('.business-path').nth(1).click();page.wait_for_url('**/services/index.html')
 ok(page.locator('#transformation').is_visible(),'services entry opens implementation and other practices')
 page.goto(BASE+'/');page.evaluate('document.fonts.ready')
 ok(page.evaluate('document.fonts.check("16px \\"IBM Plex Sans\\"")'),'self-hosted enterprise body font loads')
 for asset in page.locator('img').all():
  asset.scroll_into_view_if_needed();asset.evaluate('(e)=>e.decode()')
 ok(page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete && i.naturalWidth>0)'),'all homepage images load including lazy assets')
 ok(page.locator('.offerings-composition article h3').all_text_contents()==['Insurance Software','Insurance Software Implementation, Integration & Modernization','Insurance Technology Consulting','Fractional CIO / COO / CTO Leadership'],'four offerings in the requested order')
 ok(page.locator('#navigation').get_by_role('link',name='Products',exact=True).is_visible(),'Products is a primary navigation item')
 ok(page.locator('#navigation').get_by_role('link',name='FAQ',exact=True).is_visible(),'FAQ is a primary navigation item')
 ok(page.locator('.faq-preview details').count()==3,'homepage FAQ preview provides three concise answers')
 page.goto(BASE+'/products/index.html')
 ok(page.locator('.product-catalog .product-feature').count()==1 and page.locator('.product-name').inner_text()=='EclipseSME™','only the available flagship product is published')
 ok(page.locator('#navigation a[aria-current=page]').inner_text()=='Products','product catalog navigation reflects current page')
 page.goto(BASE+'/')
 ok(page.locator('#eclipsesme').is_visible(),'EclipseSME is a distinct corporate product section')
 ok(page.get_by_role('link',name='Request a Demo',exact=False).get_attribute('href')=='https://eclipsesme.com/contact/','demo CTA goes to the verified product demo page')
 ok(page.locator('[data-explorer]').count()==0,'no service explorer complexity')
 page.goto(BASE+'/services/index.html#security');ok(page.locator('#security').is_visible(),'security review remains directly linkable')
 page.goto(BASE+'/faq/index.html');ok(page.locator('#faq-answers details').count()==9,'FAQ includes nine concise practical questions')
 page.emulate_media(reduced_motion='reduce');ok(page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto','reduced motion disables smooth scrolling');ctx.close()
 ctx=browser.new_context(java_script_enabled=False);page=ctx.new_page();page.set_viewport_size({'width':390,'height':844});page.goto(BASE+'/')
 ok(page.locator('#navigation').is_visible(),'navigation works without JavaScript')
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'mobile navigation fits without JavaScript')
 page.goto(BASE+'/faq/index.html');page.locator('summary').first.click();ok(page.locator('details').first.get_attribute('open') is not None,'FAQ works without JavaScript');ctx.close()
 # Production hostname: all pages/config/providers fulfilled from disk or stubs.
 ctx=browser.new_context();req,err=configure(ctx,mode='development');page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html')
 ok(page.locator('[type=submit]').is_disabled(),'public development mode fails closed')
 ok(not req,'no provider requests from unconfigured production preview');ctx.close()
 for kw,label in [({'endpoint':''},'empty endpoint'),({'mode':'invalid'},'invalid mode'),({'required':True},'missing required CAPTCHA key')]:
  ctx=browser.new_context();req,err=configure(ctx,**kw);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');ok(page.locator('[type=submit]').is_disabled(),label+' fails closed')
  page.locator('#inquiry-form').evaluate('(f)=>f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))')
  ok(page.locator('#form-status').get_attribute('data-state')=='error' and not req,label+' cannot report success or send a request');ctx.close()
 for response in ['success','ambiguous','malformed','rate','network','reject-ok']:
  ctx=browser.new_context();req,err=configure(ctx,response=response);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html')
  page.locator('[type=submit]').click();ok(not req,'invalid required fields block request')
  fill(page);page.get_by_label('Phone call',exact=True).check();page.locator('[type=submit]').click();ok(not req,'phone selection requires phone number')
  page.locator('#phone').fill('+1 555 0100');page.locator('[type=submit]').click();page.wait_for_timeout(200)
  state=page.locator('#form-status').get_attribute('data-state')
  ok(state==('success' if response=='success' else 'error'),'provider '+response+' has correct feedback')
  ok(len(req)==1,'one POST attempt, no duplicate provider calls')
  if response=='success':ok(page.locator('[type=submit]').is_disabled() and page.locator('#name').input_value()=='','confirmed success resets and locks form')
  else:
   ok(page.locator('#name').input_value()=='Test Reviewer','failure preserves entered data')
   page.locator('[type=submit]').click();ok(len(req)==1,'retry cooldown prevents immediate resend')
  ok(not err,'no unexpected external traffic');ctx.close()
 ctx=browser.new_context();req,err=configure(ctx,captcha='TEST-PUBLIC-KEY',required=True);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');fill(page);page.locator('[type=submit]').click()
 ok(not any('formspree' in x.url for x in req),'failed CAPTCHA load prevents delivery');ctx.close()
 ctx=browser.new_context();req,err=configure(ctx,mode='development',result='error');page=ctx.new_page();page.goto(BASE+'/contact/index.html');fill(page);page.locator('[type=submit]').click();page.wait_for_timeout(500)
 ok('SIMULATED ERROR' in page.locator('#form-status').inner_text() and not req,'local simulated error sends no requests');ctx.close()
 # reCAPTCHA v2: explicit rendering, token validation and server confirmation.
 for width in [1440,320]:
  ctx=browser.new_context(viewport={'width':width,'height':900});req,err=configure(ctx,captcha='TEST-PUBLIC-KEY',required=True,captcha_state='checkbox');page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html')
  page.wait_for_selector('#mock-recaptcha')
  ok(page.evaluate('window.__captchaOptions.sitekey')=='TEST-PUBLIC-KEY','v2 widget uses the public site key')
  ok(page.evaluate('window.__captchaOptions.size')==('compact' if width==320 else 'normal'),'checkbox size fits the form width')
  fill(page);page.locator('[type=submit]').click()
  ok(not any('formspree' in r.url for r in req),'unchecked CAPTCHA prevents a POST')
  page.locator('#mock-recaptcha').check();page.locator('[type=submit]').click();page.wait_for_timeout(200)
  posts=[r for r in req if 'formspree' in r.url]
  ok(len(posts)==1 and posts[0].method=='POST' and 'TEST-CAPTCHA-TOKEN' in posts[0].post_data,'AJAX POST includes CAPTCHA response token')
  ok(page.locator('#form-status').get_attribute('data-state')=='success' and page.locator('[type=submit]').is_disabled(),'provider-confirmed CAPTCHA submission reports success once')
  page.evaluate('window.__captchaOptions["expired-callback"]()')
  ok(page.locator('#form-status').get_attribute('data-state')=='success','later CAPTCHA expiry cannot overwrite confirmed receipt');ctx.close()
 ctx=browser.new_context();req,err=configure(ctx,captcha='TEST-PUBLIC-KEY',required=True,captcha_state='checkbox',response='ambiguous');page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');page.wait_for_selector('#mock-recaptcha');fill(page)
 page.evaluate('window.__captchaOptions["error-callback"]()');ok('could not complete' in page.locator('#form-status').inner_text(),'CAPTCHA error has accessible feedback')
 page.evaluate('window.__captchaOptions["expired-callback"]()');ok('expired' in page.locator('#form-status').inner_text(),'expired CAPTCHA prompts re-verification')
 page.locator('[type=submit]').click();ok(not any('formspree' in r.url for r in req),'expired/empty token blocks delivery')
 page.locator('#mock-recaptcha').check();page.locator('[type=submit]').click();page.wait_for_timeout(200)
 ok(page.locator('#form-status').get_attribute('data-state')=='error' and page.locator('#name').input_value()=='Test Reviewer','ambiguous response with CAPTCHA never reports success and preserves entries')
 ok(page.evaluate('window.__captchaResets')==1 and not page.locator('#mock-recaptcha').is_checked(),'failed provider response resets the challenge');ctx.close()
 # A pending provider response must not produce success or allow duplicate POSTs.
 ctx=browser.new_context();req,err=configure(ctx,captcha='TEST-PUBLIC-KEY',required=True,captcha_state='checkbox');page=ctx.new_page();held=[]
 page.route('https://formspree.io/**',lambda route:held.append(route))
 page.goto('https://eclipseiq.ca/contact/index.html');page.wait_for_selector('#mock-recaptcha');fill(page);page.locator('#mock-recaptcha').check();page.locator('[type=submit]').click();page.wait_for_timeout(100)
 ok(len(held)==1 and page.locator('#form-status').get_attribute('data-state')=='pending','no success before the provider responds')
 page.locator('#inquiry-form').evaluate('(f)=>f.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))')
 ok(len(held)==1 and page.locator('[type=submit]').is_disabled(),'pending state blocks duplicate submission')
 held[0].fulfill(content_type='application/json',body='{"ok":true}');page.wait_for_timeout(200)
 ok(page.locator('#form-status').get_attribute('data-state')=='success','success follows only the confirmed provider response');ctx.close()
 # Exercise the committed public endpoint/key through the hosted production path.
 ctx=browser.new_context();req,err=configure(ctx,captcha_state='checkbox',actual_config=True);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');page.wait_for_selector('#mock-recaptcha')
 ok(page.evaluate('window.__captchaOptions.sitekey')=='6LcYYf8tAAAAAL1iEM5TbzaZSiq4VEGSsfyBUOna','committed public v2 site key renders the checkbox')
 fill(page);page.locator('#mock-recaptcha').check();page.locator('[type=submit]').click();page.wait_for_timeout(200)
 posts=[r for r in req if 'formspree.io' in r.url]
 ok(len(posts)==1 and posts[0].url=='https://formspree.io/f/mkjjoneb' and 'TEST-CAPTCHA-TOKEN' in posts[0].post_data,'committed production configuration posts token and fields to the supplied endpoint (intercepted)')
 ok(page.locator('#form-status').get_attribute('data-state')=='success' and not err,'configured hosted flow succeeds only after mocked confirmation')
 ok(page.evaluate('window.ECLIPSEIQ_CONFIG.analytics.measurementId')=='' and not any('googletagmanager' in r.url for r in req),'analytics remains unconfigured and inactive');ctx.close()
 # The committed production configuration remains safe on an ordinary local preview.
 ctx=browser.new_context();req,err=configure(ctx,endpoint='https://formspree.io/f/mkjjoneb',captcha='6LcYYf8tAAAAAL1iEM5TbzaZSiq4VEGSsfyBUOna',required=True);page=ctx.new_page();page.goto(BASE+'/contact/index.html');fill(page);page.locator('[type=submit]').click();page.wait_for_timeout(500)
 ok('SIMULATED SUCCESS' in page.locator('#form-status').inner_text() and not req,'production config on localhost defaults to offline simulation without provider requests');ctx.close()
 ctx=browser.new_context();req,err=configure(ctx,captcha='TEST-PUBLIC-KEY',required=True,captcha_state='checkbox',local_production=True);page=ctx.new_page();page.goto(BASE+'/contact/index.html');page.wait_for_selector('#mock-recaptcha');fill(page);page.locator('#mock-recaptcha').check();page.locator('[type=submit]').click();page.wait_for_timeout(200)
 ok(page.locator('#form-status').get_attribute('data-state')=='success' and any('formspree' in r.url for r in req),'explicit local production opt-in exercises the real delivery code path with mocked providers');ctx.close()
 # Restored contact preferences: SMS and multiple selections.
 ctx=browser.new_context();req,err=configure(ctx);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');fill(page)
 page.get_by_label('SMS / text',exact=True).check();page.locator('[type=submit]').click()
 ok(not req,'SMS preference requires a phone number')
 page.locator('#phone').fill('+1 555 0100');page.locator('[type=submit]').click();page.wait_for_timeout(150)
 ok(page.locator('#form-status').get_attribute('data-state')=='success','SMS and email preferences can be submitted together')
 ok('SMS' in req[0].post_data and 'Email' in req[0].post_data,'multiple preferred contact methods are included in provider payload');ctx.close()
 ctx=browser.new_context();req,err=configure(ctx);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');fill(page);page.get_by_label('Email',exact=True).uncheck();page.locator('[type=submit]').click()
 ok(not req and 'at least one' in page.locator('#form-status').inner_text(),'missing contact preference blocks submission');ctx.close()
 ctx=browser.new_context();req,err=configure(ctx);page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html');fill(page);page.locator('#website').fill('spam.example');page.locator('[type=submit]').click()
 ok(not req,'honeypot blocks provider requests');ctx.close()
 # Consent with empty ID: zero external requests even after acceptance.
 ctx=browser.new_context();req,err=configure(ctx,endpoint='');page=ctx.new_page();page.goto('https://eclipseiq.ca/')
 ok(not req,'no external requests before consent')
 page.locator('[data-cookie-choice="accepted"]').click();ok(not req,'empty GA ID stays inactive after acceptance');ctx.close()
 # Configured GA test ID: load only upon consent, sanitized page event, withdraw.
 ctx=browser.new_context();req,err=configure(ctx,ga='G-TESTONLY');page=ctx.new_page();page.goto('https://eclipseiq.ca/contact/index.html?private=not-for-analytics#sensitive')
 ok(not req,'configured analytics makes no pre-consent requests')
 page.locator('[data-cookie-choice="rejected"]').click();page.reload();ok(not page.locator('#cookie-banner').is_visible() and not req,'rejection persists across reload with no tracking')
 page.locator('.cookie-preferences').click();ok(page.locator('[data-cookie-choice="rejected"]').evaluate('(e)=>e===document.activeElement'),'preferences focus previous choice')
 page.locator('[data-cookie-choice="accepted"]').click();page.wait_for_timeout(100)
 ok(len(req)==1 and 'googletagmanager.com' in req[0].url,'accept loads only mocked GA script once')
 events=page.evaluate('dataLayer.map(x=>Array.from(x))')
 event=[e for e in events if e[0]=='event'][0]
 ok(event[2]['page_location']=='https://eclipseiq.ca/contact/' and event[2]['page_referrer']=='','analytics event omits query/fragment/referrer')
 page.context.add_cookies([{'name':'_ga','value':'test','domain':'eclipseiq.ca','path':'/'}])
 page.locator('.cookie-preferences').click();page.locator('[data-cookie-choice="rejected"]').click();page.wait_for_load_state();page.wait_for_timeout(150)
 ok(len(req)==1,'withdrawal reload does not restart analytics')
 ok(not any(c['name']=='_ga' for c in ctx.cookies()),'withdrawal clears accessible GA cookie')
 ctx.close()
 # Expired/future/malformed consent must re-prompt without collecting.
 for saved in [{'choice':'accepted','at':1},{'choice':'accepted','at':99999999999999},{'choice':'bogus','at':int(time.time()*1000)}]:
  ctx=browser.new_context();req,err=configure(ctx,ga='G-TESTONLY');ctx.add_init_script('localStorage.setItem("eclipseiq.analytics-consent.v1",'+json.dumps(json.dumps(saved))+')');page=ctx.new_page();page.goto('https://eclipseiq.ca/')
  ok(page.locator('#cookie-banner').is_visible() and not req,'invalid/expired consent fails closed');ctx.close()
 # Cross-tab revoke.
 ctx=browser.new_context();req,err=configure(ctx,ga='G-TESTONLY');a=ctx.new_page();a.goto('https://eclipseiq.ca/');a.locator('[data-cookie-choice="accepted"]').click();b=ctx.new_page();b.goto('https://eclipseiq.ca/about/index.html');b.locator('.cookie-preferences').click();b.locator('[data-cookie-choice="rejected"]').click();a.wait_for_timeout(250)
 ok(a.evaluate('JSON.parse(localStorage.getItem("eclipseiq.analytics-consent.v1")).choice')=='rejected','cross-tab rejection synchronized')
 ok(a.locator('[data-optional-analytics]').count()==0,'cross-tab rejection unloads analytics');ctx.close()
 # Storage blocked: no automatic consent; explicit page choice still works.
 ctx=browser.new_context();req,err=configure(ctx,ga='G-TESTONLY');ctx.add_init_script('Storage.prototype.getItem=()=>{throw Error("blocked")}; Storage.prototype.setItem=()=>{throw Error("blocked")};');page=ctx.new_page();page.goto('https://eclipseiq.ca/');ok(page.locator('#cookie-banner').is_visible() and not req,'blocked storage defaults to no tracking');page.locator('[data-cookie-choice="rejected"]').click();ok(not req,'blocked storage rejection is respected');ctx.close()
 browser.close()
print(f'COMPLETE: {count} assertions. Screenshots: {RESULTS}')
