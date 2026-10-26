#!/usr/bin/env python3
"""Generate the concise corporate site. Generated HTML works directly from disk."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'scripts/content.json').read_text())
PAGES=DATA['pages'];OFFERINGS=DATA['offerings'];FAQ=DATA['faq']
PUBLIC_PRODUCTS=[p for p in DATA['products'] if p.get('published') is True]

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
 nav=''.join(f'<a href="{href(k)}"'+(' aria-current="page"' if k==key else '')+f'>{label}</a>' for k,label in [('products','Products'),('services','Services'),('about','About'),('faq','FAQ')])
 nav+=link('Contact',href('contact'),'button nav-contact').replace('<a ', '<a aria-current="page" ',1) if key=='contact' else link('Contact',href('contact'),'button nav-contact')
 schema={'@context':'https://schema.org','@type':'Organization','name':'EclipseIQ Technologies Inc.','url':'https://eclipseiq.ca/','logo':'https://eclipseiq.ca/assets/eclipseiq-logo-original.png','description':PAGES['home'][2],'sameAs':['https://www.linkedin.com/company/eclipseiq']}
 html=f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | EclipseIQ Technologies Inc.</title><meta name="description" content="{escape(desc,quote=True)}"><meta name="theme-color" content="#023047"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="canonical" href="{canonical}">{'<meta name="robots" content="noindex">' if alias or key=='404' else ''}<meta property="og:type" content="website"><meta property="og:locale" content="en_CA"><meta property="og:site_name" content="EclipseIQ Technologies Inc."><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://eclipseiq.ca/assets/social.png"><meta property="og:image:alt" content="EclipseIQ — Insurance technology products and services."><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{pre}assets/eclipseiq-logo-original.png" type="image/png"><link rel="preload" href="{pre}assets/fonts/ibm-plex-sans.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{pre}assets/styles.css"><script src="{pre}assets/config.js" defer></script><script src="{pre}assets/site.js" defer></script><script src="{pre}assets/consent.js" defer></script><script type="application/ld+json">{json.dumps(schema)}</script></head>
<body class="page-{key}"><a class="skip-link" href="#main">Skip to content</a><header class="header"><div class="container header-inner"><a class="brand" href="{href('home')}" aria-label="EclipseIQ Technologies Inc. home">{brand}</a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" hidden>Menu {icon('menu')}</button><nav id="navigation" aria-label="Main navigation">{nav}</nav></div></header><main id="main">{body.replace('@ROOT@',pre)}</main>
<footer class="footer"><div class="container footer-content"><div class="footer-brand"><a class="brand" href="{href('home')}">{brand}</a><p>Insurance technology products & services.<br>Develop. Implement. Modernize.</p></div><div><h2>Explore</h2><a href="{href('products')}">Our products</a><a href="{href('services')}">Services & capabilities</a><a href="{href('about')}">About EclipseIQ</a><a href="{href('home')}#eclipsesme">EclipseSME™</a></div><div><h2>Get in touch</h2><a href="{href('contact')}">Contact us</a><a href="{href('faq')}">Common questions</a>{link('LinkedIn','https://www.linkedin.com/company/eclipseiq','footer-social',True)}<p>Based in Canada. Working internationally.</p></div></div><div class="container footer-bottom"><p>© 2026 EclipseIQ Technologies Inc.</p><div><a href="{href('privacy')}">Cookies & privacy</a><button class="cookie-preferences" hidden>Cookie preferences</button></div></div></footer>
<section id="cookie-banner" class="cookie-banner" aria-labelledby="cookie-title" hidden><div><h2 id="cookie-title">Your privacy choices</h2><p>Optional cookies help us understand website usage. Accept or reject them and change your choice at any time. <a href="{href('privacy')}">Cookies & privacy</a></p></div><div class="cookie-actions"><button class="button button-small" data-cookie-choice="accepted">Accept</button><button class="button button-outline button-small" data-cookie-choice="rejected">Reject</button></div></section></body></html>'''
 target=ROOT/('index.html' if key=='home' else path if key=='404' else path+'index.html');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)

def contact_strip():
 return '<section class="contact-strip"><div class="container"><div><h2>Let’s discuss your technology priorities.</h2><p>Tell us what your organization needs — we’ll help define the next step.</p></div>'+link('Contact EclipseIQ','@ROOT@contact/index.html','button')+'</div></section>'

def intro(eyebrow,title,copy):
 return f'<section class="page-intro"><div class="container"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="intro-copy">{copy}</p></div></section>'

def product_visual(product):
 p=product
 return f'<figure class="platform-visual"><img src="@ROOT@assets/{p.get("visual_image","enterprise-product.webp")}" width="1448" height="1086" alt="Insurance software and policy documents" loading="lazy"></figure>'

def product_feature(product, show_capabilities=False):
 p=product
 capabilities=('<ul class="product-capability-list">'+''.join(f'<li>{escape(c)}</li>' for c in p["capabilities"])+'</ul>') if show_capabilities else ''
 return f'''<article class="product-feature" id="{p['id']}"><div class="product-description"><span class="product-tag">{p['tag']}</span><p class="product-name">{p['name']}<sup>{p['trademark']}</sup></p><h3>{p['heading']}</h3><p>{p['description']}</p><p>{p['benefit']}</p><div class="actions">{link('Request a Demo',p['demo_url'],'button',True)}{link('Explore '+p['name'],p['url'],'text-link',True)}</div>{capabilities}<p class="product-byline">A product of EclipseIQ Technologies Inc.</p></div>{product_visual(p)}</article>'''

def faq_details(indices, prefix='q'):
 return ''.join(f'<details id="{prefix}-{i}"><summary>{escape(FAQ[i][0])}</summary><p>{escape(FAQ[i][1])}</p></details>' for i in indices)

def offering_art(slug):
 if slug=='software':return '<div class="offering-software-art" aria-hidden="true"><img src="./assets/enterprise-product.webp" width="1448" height="1086" alt="" loading="lazy"><span>EclipseSME<sup>™</sup> · Our flagship product</span></div>'
 return '<div class="offering-icon" aria-hidden="true">'+icon({'transformation':'engineering','consulting':'consulting','leadership':'leadership'}[slug])+'</div>'

def main():
 home='''<section class="tech-hero"><img class="hero-image" src="./assets/enterprise-hero.webp" width="1672" height="941" alt="Software engineering workspace with code and technical documents" fetchpriority="high"><div class="hero-shade" aria-hidden="true"></div><div class="container tech-hero-grid"><div class="hero-copy"><p class="eyebrow">Insurance technology products & services</p><h1>Insurance software.<br><span>Built, implemented<br>and supported.</span></h1><p>EclipseIQ develops proprietary insurance products and delivers the expertise to implement, integrate and modernize insurance systems.</p><div class="actions">'''+link('Explore products','./products/index.html','button')+link('Explore services','./services/index.html','button button-outline')+'''</div></div></div></section>
<section class="business-paths" aria-label="Our two business areas"><div class="container"><a class="business-path" href="./products/index.html"><span class="path-label">Products</span><h2>Insurance Technology Products</h2><p>Proprietary software. Configured for insurance operations.</p><span class="path-action">Discover EclipseSME™</span></a><a class="business-path" href="./services/index.html"><span class="path-label">Services</span><h2>Professional Technology Services</h2><p>Implementation, integration and modernization — including third-party platforms.</p><span class="path-action">Explore our expertise</span></a></div></section>
<section class="audience"><div class="container"><p>Built for the business of insurance</p><div><span>Insurers</span><span>MGAs</span><span>Reinsurers</span><span>Brokers & underwriting organizations</span></div></div></section>
<section class="section offerings-section" id="offerings-section"><div id="capabilities"></div><div class="container"><div class="section-heading"><div><p class="eyebrow">Our Offerings</p><h2>Products and expertise.<br>From development to delivery.</h2></div><p>Four connected capabilities for your insurance technology requirements.</p></div><div class="offerings-composition">'''
 summaries={
 'software':'EclipseSME and proprietary insurance software, configured around your products, workflows and operations.',
 'transformation':'Implementation of EclipseIQ and third-party platforms. Integrations, data migration, custom development and legacy modernization.',
 'consulting':'InsurTech advisory, strategy, architecture and operational improvement — including Eclipse Totality Assessment™.',
 'leadership':'Senior executive expertise in governance, transformation oversight, operational alignment and team development.'}
 for i,(slug,title,heading,desc,items,ico) in enumerate(OFFERINGS):
  dest='./products/index.html' if slug=='software' else './services/index.html#'+slug
  home+=f'<article class="offering offering-{slug}"><span class="offering-number">0{i+1}</span><div class="offering-copy"><h3>{title}</h3><p>{summaries[slug]}</p>{link("Explore insurance software" if slug=="software" else "Explore this offering",dest)}</div>{offering_art(slug)}</article>'
 home+='''</div></div></section><section class="section products-section"><div class="container"><div class="section-heading"><div><p class="eyebrow">Our flagship product</p><h2>Insurance software.<br>Developed by EclipseIQ.</h2></div><p>Proprietary insurance technology, backed by the people who build and implement it.</p></div>'''+''.join(product_feature(p,True) for p in PUBLIC_PRODUCTS)+'''<div class="section-foot">'''+link('Discover our products','./products/index.html')+'''<span>Built by EclipseIQ. Supported by our implementation expertise.</span></div></div></section>
<section class="section company-section" id="company"><div class="container company-summary"><div><p class="eyebrow">The company behind the technology</p><h2>Insurance experience.<br>Built into the work.</h2>'''+link('About EclipseIQ','./about/index.html')+'''</div><div><p>EclipseIQ combines decades of insurance industry experience with senior CIO / COO / CTO-level leadership, solution architecture and hands-on software delivery.</p><p>We understand both the decisions behind insurance systems and the engineering required to make them work. Based in Canada, we work with organizations in Canada and internationally.</p></div></div></section><section class="section faq-preview"><div class="container faq-preview-layout"><div><p class="eyebrow">Frequently asked questions</p><h2>A clear starting point.</h2><p>Software, implementation or a specialized requirement — here are a few answers.</p>'''+link('View all FAQ','./faq/index.html')+'''</div><div class="faq-list">'''+faq_details([0,2,3],'home-q')+'</div></div></section>'+contact_strip()
 build_page('home',home)
 # A data-driven public catalog: only products explicitly added here are rendered.
 products=intro('Our products','Insurance software. Developed by EclipseIQ.','Our product development focuses on practical needs across insurance operations. EclipseSME™ is our flagship platform, backed by our implementation, engineering and support expertise. We also explore new products for other insurance technology needs.')
 products+='<section class="section product-catalog"><div class="container">'+''.join(product_feature(p) for p in PUBLIC_PRODUCTS)+'</div></section>'
 p=PUBLIC_PRODUCTS[0]
 products+='''<section class="section product-capabilities"><div class="container"><div class="section-heading"><div><p class="eyebrow">Inside EclipseSME</p><h2>Configured for your insurance business.</h2></div><p>For MGAs, insurers and specialty insurance organizations.</p></div><div class="capability-register">'''+''.join(f'<div><span>0{i+1}</span><h3>{c}</h3></div>' for i,c in enumerate(p['capabilities']))+'''</div><p class="scope-note">Specific modules, configuration and integration requirements are agreed during discovery.</p></div></section><section class="section implementation-bridge"><div class="container"><div><p class="eyebrow">Beyond the product</p><h2>Implementation is part of our expertise.</h2><p>From configuration and data migration to integration and custom development, we help put insurance software to work. That includes EclipseSME and third-party insurance platforms.</p></div>'''+link('Explore implementation & modernization','../services/index.html#transformation','button')+'</div></section>'+contact_strip()
 build_page('products',products)
 services=intro('Our Offerings','Insurance technology. From product to implementation.','Proprietary software and the expertise to implement, integrate, modernize and lead. Work with us on EclipseSME, third-party platforms or a specialized requirement.')
 services+='<section class="section services-section"><div class="container"><nav class="service-jump" aria-label="Our offerings">'+''.join(link(t,'#'+slug) for slug,t,*_ in OFFERINGS)+'</nav><div class="service-details">'
 for i,(slug,title,heading,desc,items,ico) in enumerate(OFFERINGS):
  services+=f'<article id="{slug}" class="service-detail"><div class="service-title"><span class="service-number">0{i+1}</span>{icon(ico)}<h2>{title}</h2></div><div><h3>{heading}</h3><p>{desc}</p><ul>'+''.join(f'<li>{escape(x)}</li>' for x in items)+'</ul>'
  if slug=='software':services+=link('Explore our products','../products/index.html')
  if slug=='consulting':services+='''<div class="practice-notes"><p id="assessment"><b>Eclipse Totality Assessment™</b> reviews systems, processes, data and governance to identify risks and prioritize improvements.</p><p id="audit"><b>Audit readiness:</b> review operational processes, documentation and governance.</p><p id="security"><b>Security reviews:</b> assess insurance systems for vulnerabilities and practical improvements.</p></div>'''
  if slug=='leadership':services+='<p class="practice-note" id="coaching"><b>Team development & coaching:</b> support leaders and teams through technology and operational change.</p>'
  services+='</div></article>'
 services+='</div></div></section>'+contact_strip();build_page('services',services)
 about=intro('About EclipseIQ','A product-building insurance technology company.','EclipseIQ Technologies Inc. develops insurance software and delivers the implementation, engineering and leadership expertise behind insurance systems.')
 about+='''<section class="section"><div class="container about-layout"><div class="company-signature"><img class="signature-image" src="../assets/enterprise-hero.webp" width="1672" height="941" alt="Engineering workspace with code and technical documents" loading="lazy"><p class="eyebrow">Our perspective</p><h2>We build the software.<br>We understand the operation.</h2><div class="signature-practices"><span>Product development</span><span>Insurance operations</span><span>Technical delivery</span></div></div><div class="about-copy"><h2>Experience across the insurance business.</h2><p>Our experience combines decades in insurance technology and operations with senior CIO / COO / CTO-level leadership, solution architecture and hands-on software delivery.</p><p>It spans systems modernization, data and analytics, reinsurance and enterprise transformation — connecting technology decisions with underwriting, policy administration and operational requirements.</p><p>Based in Canada, we work with insurers, MGAs, reinsurers, brokers, program administrators and specialty insurance organizations in Canada and internationally.</p></div></div></section><section class="section company-practice"><div class="container"><div class="section-heading"><div><p class="eyebrow">Products + services</p><h2>Our own software. Your choice of platform.</h2></div></div><div class="two-column"><div><h3>Proprietary product development</h3><p>EclipseSME™ is our flagship product. We build insurance technology around practical operational requirements, with configuration, implementation and support shaped around your organization.</p>'''+link('Explore our products','../products/index.html')+'''</div><div><h3>Expertise beyond our products</h3><p>We also implement, integrate and modernize third-party insurance systems, develop custom software and provide InsurTech consulting and fractional executive leadership.</p>'''+link('Explore our offerings','../services/index.html')+'</div></div></div></section>'+contact_strip()
 build_page('about',about)
 faq=intro('FAQ','Answers for your next technology decision.','Concise guidance on insurance software, implementations and working with EclipseIQ.')
 faq+='<section class="section"><div class="container faq-layout"><aside class="faq-index"><p class="eyebrow">Browse questions</p>'+''.join(link(g['title'],'#faq-'+g['id']) for g in DATA['faq_groups'])+'<p>Have a specific requirement?</p>'+link('Contact EclipseIQ','../contact/index.html')+'</aside><div id="faq-answers">'
 for g in DATA['faq_groups']:
  faq+=f'<section class="faq-group" id="faq-{g["id"]}"><div class="faq-group-heading"><h2>{g["title"]}</h2><p>{g["intro"]}</p></div><div class="faq-list">'+faq_details(g['questions'])+'</div></section>'
 faq+='</div></div></section>';build_page('faq',faq)
 form=(ROOT/'scripts/partials/contact-form.tpl').read_text()
 contact=intro('Contact EclipseIQ','Let’s discuss your insurance technology requirements.','Explore EclipseSME, plan an implementation or tell us about your systems, software and leadership needs.')
 contact+='''<section class="section contact-section"><div class="container contact-layout"><aside><p class="eyebrow">Products & services</p><h2>How can we help?</h2><p>Contact us about our software, implementations, integration and modernization, InsurTech consulting or fractional leadership.</p><p>Based in Canada.<br>Working internationally.</p><p class="contact-discretion">Please share only a high-level overview. Leave confidential and policyholder information out of your inquiry.</p></aside><div class="contact-form-wrap">'''+form+'</div></div></section>';build_page('contact',contact)
 legal=(ROOT/'scripts/partials/privacy-body.tpl').read_text()
 def heading(m):
  attrs,title=m.groups();slug='cookies' if 'id="cookies"' in attrs else re.sub('[^a-z0-9]+','-',title.lower()).strip('-');return f'<h2 id="{slug}">{title}</h2>'
 legal=re.sub(r'<h2([^>]*)>(.*?)</h2>',heading,legal)
 privacy=intro('Website information','Cookies & privacy.','How this website handles inquiries and optional analytics.')+'<section class="section"><div class="container legal">'+legal+'</div></section>'
 build_page('privacy',privacy)
 for alias in ['privacy/','cookie-policy-ca/','cookie-policy-ca-2/']:build_page('privacy',privacy,alias)
 build_page('404',intro('Page not found','This page may have moved.','Explore our products and offerings, or return to the homepage.')+'<section class="section"><div class="container">'+link('Return to the homepage','./index.html','button')+'</div></section>')
 (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://eclipseiq.ca/{path}</loc></url>\n' for k,(path,_,_) in PAGES.items() if k!='404')+'</urlset>\n')
 print('Generated products-and-services website: 11 pages including compatibility URLs')
if __name__=='__main__':main()
