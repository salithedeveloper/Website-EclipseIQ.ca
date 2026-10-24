#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import re, xml.etree.ElementTree as ET
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
assert len(pages)==7
ET.parse(ROOT/'sitemap.xml')
for f in (ROOT/'assets').glob('*.js'):
 text=f.read_text()
 assert not re.search(r'G-6N90S2Y3DE|13041110|82fea225|eclipsesme\.analytics-consent',text),f'Reference identifiers: {f}'
print('PASS: 7 pages; local links, fragments, IDs, metadata, external link security, sitemap, identifier isolation')
