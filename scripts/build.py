#!/usr/bin/env python3
"""Generate the concise corporate site. Generated HTML works directly from disk."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'scripts/content.json').read_text())
PAGES=DATA['pages'];OFFERINGS=DATA['offerings'];FAQ=DATA['faq']

def icon(name):
 paths={
 'consulting':'M5 4h14v16H5zM8 8h8M8 12h8M8 16h5',
 'engineering':'m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16',
 'leadership':'M4 20v-3c0-4 16-4 16 0v3M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8',
 'software':'M3 4h18v13H3zM8 21h8M12 17v4M3 8h18',
 'menu':'M4 6h16M4 12h16M4 18h16'}
 return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{paths.get(name,paths["software"])}"/></svg>'

def link(label,url,cls='text-link',external=False):
 return f'<a class="{cls}" href="{url}"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+f'>{label}'+('<span class="sr-only"> (opens in a new tab)</span>' if external else '')+'</a>'

def build_page(key,body,alias=None):
 path,title,desc=PAGES[key];pre='./' if key in ('home','404') else '../'
 if alias:path=alias;pre='../'
 def href(k):
  p=PAGES[k][0];return pre+(p+'index.html' if p.endswith('/') else p or 'index.html')
 canonical='https://eclipseiq.ca/'+(PAGES[key][0] if alias else path)
 brand=f'<img src="{pre}assets/eclipseiq-logo-original.png" width="202" height="88" alt="EclipseIQ Technologies Inc. — Smarter Insurance Solutions">'
 nav=''.join(f'<a href="{href(k)}"'+(' aria-current="page"' if k==key else '')+f'>{label}</a>' for k,label in [('services','Services'),('about','Company')])
 nav+=f'<a href="{href("home")}#eclipsesme">EclipseSME™</a>'+link('Contact us',href('contact'),'button nav-contact')
 schema={'@context':'https://schema.org','@type':'Organization','name':'EclipseIQ Technologies Inc.','url':'https://eclipseiq.ca/','logo':'https://eclipseiq.ca/assets/eclipseiq-logo-original.png','description':PAGES['home'][2],'sameAs':['https://www.linkedin.com/company/eclipseiq']}
 html=f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | EclipseIQ Technologies Inc.</title><meta name="description" content="{escape(desc,quote=True)}"><meta name="theme-color" content="#023047"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="canonical" href="{canonical}">{'<meta name="robots" content="noindex">' if alias or key=='404' else ''}<meta property="og:type" content="website"><meta property="og:locale" content="en_CA"><meta property="og:site_name" content="EclipseIQ Technologies Inc."><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://eclipseiq.ca/assets/social.png"><meta property="og:image:alt" content="EclipseIQ — Insurance technology solutions. Software, consulting and senior leadership."><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{pre}assets/eclipseiq-logo-original.png" type="image/png"><link rel="preload" href="{pre}assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{pre}assets/styles.css"><script src="{pre}assets/config.js" defer></script><script src="{pre}assets/site.js" defer></script><script src="{pre}assets/consent.js" defer></script><script type="application/ld+json">{json.dumps(schema)}</script></head>
<body class="page-{key}"><a class="skip-link" href="#main">Skip to content</a><header class="header"><div class="container header-inner"><a class="brand" href="{href('home')}" aria-label="EclipseIQ Technologies Inc. home">{brand}</a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" hidden>Menu {icon('menu')}</button><nav id="navigation" aria-label="Main navigation">{nav}</nav></div></header><main id="main">{body.replace('@ROOT@',pre)}</main>
<footer class="footer"><div class="container footer-content"><div class="footer-brand"><a class="brand" href="{href('home')}">{brand}</a><p>Insurance technology solutions.<br>Software, consulting and senior leadership.</p></div><div><h2>Explore</h2><a href="{href('services')}">Services & capabilities</a><a href="{href('about')}">About EclipseIQ</a><a href="{href('home')}#eclipsesme">EclipseSME™</a></div><div><h2>Get in touch</h2><a href="{href('contact')}">Contact us</a><a href="{href('faq')}">Common questions</a>{link('LinkedIn','https://www.linkedin.com/company/eclipseiq','footer-social',True)}<p>Based in Canada. Working internationally.</p></div></div><div class="container footer-bottom"><p>© 2026 EclipseIQ Technologies Inc.</p><div><a href="{href('privacy')}">Cookies & privacy</a><button class="cookie-preferences" hidden>Cookie preferences</button></div></div></footer>
<section id="cookie-banner" class="cookie-banner" aria-labelledby="cookie-title" hidden><div><h2 id="cookie-title">Your privacy choices</h2><p>Optional cookies help us understand website usage. Accept or reject them and change your choice at any time. <a href="{href('privacy')}">Cookies & privacy</a></p></div><div class="cookie-actions"><button class="button button-small" data-cookie-choice="accepted">Accept</button><button class="button button-outline button-small" data-cookie-choice="rejected">Reject</button></div></section></body></html>'''
 target=ROOT/('index.html' if key=='home' else path if key=='404' else path+'index.html');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)

def contact_strip():
 return '<section class="contact-strip"><div class="container"><div><h2>Let’s discuss your technology priorities.</h2><p>Tell us what your organization needs — we’ll help define the next step.</p></div>'+link('Contact EclipseIQ','@ROOT@contact/index.html','button')+'</div></section>'

def intro(eyebrow,title,copy):
 return f'<section class="page-intro"><div class="container"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="intro-copy">{copy}</p></div></section>'

def main():
 home='''<section class="home-hero"><div class="container hero-layout"><div class="hero-copy"><p class="eyebrow">EclipseIQ Technologies Inc.</p><h1>Insurance technology.<br><span>Software, consulting<br>and senior leadership.</span></h1><p>We help insurers, MGAs and specialty insurance organizations modernize systems and operations — from technology strategy to software delivery.</p><div class="actions">'''+link('Explore our services','./services/index.html','button')+link('Talk to us','./contact/index.html','text-link')+'''</div></div><figure class="hero-photo"><img src="./assets/insurance-engineering.png" width="1536" height="1024" alt="Illustrative engineering workspace with source code, operational software and technical plans" fetchpriority="high"><figcaption><span>Our focus</span>Technology that supports the way your insurance business works.</figcaption></figure></div></section>
<section class="audience"><div class="container"><span>Who we work with</span><p>Insurers <i>·</i> MGAs <i>·</i> Reinsurers <i>·</i> Brokers <i>·</i> Underwriting organizations</p></div></section>
<section class="section" id="offerings-section"><div id="capabilities"></div><div class="container"><div class="section-heading"><div><p class="eyebrow">How we can help</p><h2>Insurance knowledge.<br>Practical technology expertise.</h2></div><p>Support for the decisions, systems and people behind your operations.</p></div><div class="service-overview">'''
 for slug,title,heading,desc,items,ico in OFFERINGS[:3]:
  home+=f'<article class="service-{slug}"><div class="service-media" aria-hidden="true"><img src="./assets/{dict(consulting="insurance-planning.png",transformation="insurance-engineering.png",leadership="insurance-leadership.png")[slug]}" alt="" width="800" height="534" loading="lazy"></div>{icon(ico)}<h3>{title}</h3><p>'+({'consulting':'Assess your systems, align technology with business priorities and plan the improvements that matter.','transformation':'Develop software, modernize existing systems and connect platforms, workflows and data.','leadership':'Bring experienced CIO, COO or CTO leadership to strategy, delivery and operational change.'}[slug])+f'</p>{link("View capabilities","./services/index.html#"+slug)}</article>'
 home+='''</div></div></section>
<section class="product-section" id="eclipsesme"><div class="container product-layout"><div><img class="product-art" src="./assets/insurance-documents.svg" width="400" height="290" alt="" aria-hidden="true" loading="lazy"><p class="eyebrow">Our insurance software</p><h2>EclipseSME<span>™</span></h2><p class="product-subtitle">A product of EclipseIQ Technologies Inc.</p></div><div class="product-copy"><h3>Cloud software for insurance operations.</h3><p>EclipseSME brings underwriting, policy administration, billing and reporting into a configurable platform for MGAs, insurers and specialty insurance businesses — helping teams reduce manual work and manage the policy lifecycle in one place.</p><div class="product-features"><span>Configurable products & workflows</span><span>Partner integrations</span><span>Role-based access & reporting</span></div>'''+'<div class="product-actions">'+link('Request a Demo','https://eclipsesme.com/contact/','button button-light',True)+link('Explore EclipseSME','https://eclipsesme.com/','text-link',True)+'</div>'+'''</div></div></section>
<section class="section" id="company"><div class="container company-summary"><div><p class="eyebrow">About EclipseIQ</p><h2>Insurance experience.<br>Across technology and operations.</h2></div><div><p>EclipseIQ combines decades of insurance industry experience with senior CIO / COO / CTO-level leadership, insurance operations knowledge and solution architecture.</p><p>That experience extends to hands-on software delivery: connecting technology decisions to underwriting, policy administration and day-to-day operations, from architecture through implementation.</p>'''+link('More about EclipseIQ','./about/index.html')+'''</div></div></section>'''+contact_strip()
 build_page('home',home)
 services=intro('Services & capabilities','Technology expertise for insurance.','Software, consulting and senior leadership to help your organization plan, build and improve its technology.')
 services+='<section class="section services-section"><div class="container"><nav class="service-jump" aria-label="Service areas">'+''.join(link(t,'#'+slug) for slug,t,*_ in OFFERINGS)+'</nav><div class="service-details">'
 for slug,title,heading,desc,items,ico in OFFERINGS:
  services+=f'<article id="{slug}" class="service-detail service-{slug}"><div class="service-title">{icon(ico)}<h2>{title}</h2></div><div><p>{desc}</p><ul>'+''.join(f'<li>{escape(x)}</li>' for x in items)+'</ul>'
  if slug=='consulting':services+='<p id="assessment" class="service-note">The Eclipse Totality Assessment™ reviews systems, processes, data and governance to identify risks and prioritize improvements.</p>'
  if slug=='software':services+=link('Visit the EclipseSME website','https://eclipsesme.com/','text-link',True)
  services+='</div></article>'
 services+='''</div><section class="supporting-services"><h2>Additional support</h2><div><article id="audit"><h3>Audit readiness</h3><p>Review operational processes, documentation and governance before an internal or regulatory audit.</p></article><article id="security"><h3>Security reviews</h3><p>Assess insurance systems for vulnerabilities and identify practical security improvements.</p></article><article id="coaching"><h3>Team development & coaching</h3><p>Support leaders and teams through technology and operational change.</p></article></div></section></div></section>'''+contact_strip()
 build_page('services',services)
 about=intro('About EclipseIQ','An insurance technology company.','We combine insurance software, technology consulting and experienced leadership to help organizations modernize technology and operations.')
 about+='''<section class="section"><div class="container about-layout"><figure><img src="../assets/insurance-planning.png" width="800" height="534" alt="Technology planning with laptops and working documents" loading="lazy"></figure><div><p class="eyebrow">Business understanding. Technical delivery.</p><h2>Experience across the insurance business.</h2><p>EclipseIQ Technologies Inc. is based in Canada and works with insurance organizations in Canada and internationally.</p><p>Our experience combines senior CIO / COO / CTO-level leadership with insurance operations, solution architecture and hands-on software delivery. It spans systems modernization, data and analytics, reinsurance and enterprise transformation.</p><p>We understand both the executive decisions and the implementation work behind insurance systems — aligning technology plans with underwriting, policy administration and operational requirements.</p><p>We support insurers, MGAs, reinsurers, brokers, program administrators and specialty insurance organizations.</p></div></div></section><section class="section approach-section"><div class="container"><div class="section-heading"><div><p class="eyebrow">Working with EclipseIQ</p><h2>Support shaped around your needs.</h2></div></div><div class="approach-list"><article><h3>Consulting & implementation</h3><p>Start with your business objectives and technology environment. Define priorities, agree the scope and work through delivery.</p></article><article><h3>Fractional leadership</h3><p>Access CIO, COO or CTO expertise for strategy, operational alignment and transformation oversight.</p></article><article><h3>Our software</h3><p>EclipseSME™ is our configurable cloud insurance platform. We also advise on and implement third-party platforms.</p></article></div></div></section>'''+contact_strip()
 build_page('about',about)
 faq=intro('Common questions','A few things to know.','Brief answers about our services and working with EclipseIQ.')
 faq+='<section class="section"><div class="container faq-container"><div id="faq-answers" class="faq-list">'+''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in FAQ)+'</div><p class="faq-followup">Have a specific requirement? '+link('Get in touch','../contact/index.html')+'</p></div></section>'
 build_page('faq',faq)
 form=(ROOT/'scripts/partials/contact-form.tpl').read_text()
 contact=intro('Contact EclipseIQ','Let’s talk about your requirements.','Tell us about your organization and the technology or operational challenge you want to address.')
 contact+='''<section class="section contact-section"><div class="container contact-layout"><aside><h2>How can we help?</h2><p>Contact us about consulting, software engineering, fractional leadership or an EclipseSME demonstration.</p><p>Based in Canada.<br>Working internationally.</p><p class="contact-discretion">Please share only a high-level overview. Leave confidential and policyholder information out of your inquiry.</p></aside><div class="contact-form-wrap">'''+form+'</div></div></section>'
 build_page('contact',contact)
 legal=(ROOT/'scripts/partials/privacy-body.tpl').read_text()
 def heading(m):
  attrs,title=m.groups();slug='cookies' if 'id="cookies"' in attrs else re.sub('[^a-z0-9]+','-',title.lower()).strip('-');return f'<h2 id="{slug}">{title}</h2>'
 legal=re.sub(r'<h2([^>]*)>(.*?)</h2>',heading,legal)
 privacy=intro('Website information','Cookies & privacy.','How this website handles inquiries and optional analytics.')+'<section class="section"><div class="container legal">'+legal+'</div></section>'
 build_page('privacy',privacy)
 for alias in ['privacy/','cookie-policy-ca/','cookie-policy-ca-2/']:build_page('privacy',privacy,alias)
 build_page('404',intro('Page not found','This page may have moved.','Explore our services or return to the homepage.')+'<section class="section"><div class="container">'+link('Return to the homepage','./index.html','button')+'</div></section>')
 (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://eclipseiq.ca/{path}</loc></url>\n' for k,(path,_,_) in PAGES.items() if k!='404')+'</urlset>\n')
 print('Generated concise corporate website: 10 pages including compatibility URLs')
if __name__=='__main__':main()
