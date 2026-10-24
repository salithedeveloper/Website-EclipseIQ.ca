#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re, hashlib, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.refs=[];self.h1=0;self.canonical=[];self.descriptions=[];self.lang=False;self.has_title=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='html':self.lang=bool(a.get('lang'))
  if tag=='title':self.has_title=True
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='meta' and a.get('name')=='description':self.descriptions.append(a.get('content'))
  if tag=='a' and a.get('target')=='_blank':assert 'noopener' in a.get('rel',''), 'Missing noopener'
  for k in ('href','src'):
   if k in a:self.refs.append(a[k])
pages={}
for f in ROOT.rglob('*.html'):
 if 'review' in f.relative_to(ROOT).parts:continue
 p=Page();p.feed(f.read_text());pages[f]=p
 assert len(p.ids)==len(set(p.ids)),f'Duplicate IDs: {f}'
 assert p.h1==1 and p.lang and p.has_title and len(p.canonical)==1 and len(p.descriptions)==1,f'Metadata: {f}'
for f,p in pages.items():
 for ref in p.refs:
  u=urlparse(ref)
  if u.scheme or u.netloc:continue
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if target.is_dir():target=target/'index.html'
  assert target.exists(),f'Broken reference {f}: {ref}'
  if u.fragment and target in pages:assert u.fragment in pages[target].ids,f'Broken fragment: {ref}'
assert len(pages)==10
assert hashlib.sha256((ROOT/'assets/eclipseiq-logo-original.png').read_bytes()).hexdigest()=='e9edbbf8165884a95bdbf18d2a7007b911fbaf35306d39c65a42bb1036b4b9fd', 'Original logo bytes changed'
for f in pages:
 text=f.read_text()
 assert 'Temporary logo placeholder' not in text, f'Placeholder branding: {f}'
 assert 'assets/eclipseiq-logo-original.png' in text, f'Missing original logo: {f}'
 assert 'mailto:' not in text and not re.search(r'[A-Za-z0-9._%+-]+@eclipseiq\.ca',text), f'Public email address: {f}'
for name in ['privacy','cookie-policy-ca','cookie-policy-ca-2']:
 text=(ROOT/name/'index.html').read_text()
 assert 'https://eclipseiq.ca/privacy-policy/' in text and 'name="robots" content="noindex"' in text

ET.parse(ROOT/'sitemap.xml')
for f in (ROOT/'assets').glob('*.js'):
 text=f.read_text()
 assert not re.search(r'G-6N90S2Y3DE|13041110|82fea225|eclipsesme\.analytics-consent',text),f'Reference identifiers: {f}'
print('PASS: 10 pages; local links, fragments, IDs, metadata, external link security, sitemap, identifier isolation, original logo integrity and legacy privacy URLs')
