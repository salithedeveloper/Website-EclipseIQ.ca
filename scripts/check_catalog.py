#!/usr/bin/env python3
"""Exercise product publication and catalogue growth in a disposable checkout.
Does not edit the website or contact external services.
"""
from pathlib import Path
from html.parser import HTMLParser
import copy,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
class Features(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='article' and 'product-feature' in a.get('class','').split():self.ids.append(a.get('id'))
with tempfile.TemporaryDirectory(prefix='eclipseiq-catalog-') as directory:
 r=Path(directory);(r/'scripts/partials').mkdir(parents=True)
 shutil.copy2(ROOT/'scripts/build.py',r/'scripts/build.py')
 for f in (ROOT/'scripts/partials').glob('*.tpl'):shutil.copy2(f,r/'scripts/partials'/f.name)
 data=json.loads((ROOT/'scripts/content.json').read_text())
 draft=copy.deepcopy(data['products'][0]);draft.update(id='test-draft',name='Unreleased Test Fixture',published=False)
 data['products'].append(draft)
 def build():
  (r/'scripts/content.json').write_text(json.dumps(data))
  subprocess.run([sys.executable,str(r/'scripts/build.py')],check=True,capture_output=True)
 def feature_ids(page):
  p=Features();p.feed((r/page).read_text());return p.ids
 build()
 for page in ('index.html','products/index.html'):
  assert feature_ids(page)==['eclipsesme'],page
  assert 'Unreleased Test Fixture' not in (r/page).read_text(),page
 # Explicit publication adds a second feature through the existing shared layout.
 draft['published']=True
 build()
 for page in ('index.html','products/index.html'):assert feature_ids(page)==['eclipsesme','test-draft'],page
print('PASS: draft products stay private; a second explicitly published product uses the existing homepage/catalogue layout')
