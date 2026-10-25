#!/usr/bin/env python3
"""Explicit local real-delivery preview. No repository files are changed.
The browser sends an inquiry only after a human completes CAPTCHA and submits.
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from functools import partial
import argparse
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--real-delivery',action='store_true',required=True,help='Explicitly allow real Formspree delivery in this loopback preview')
parser.add_argument('--port',type=int,default=4174)
args=parser.parse_args()
config=(ROOT/'assets/config.js').read_text()
assert config.count('allowLocalProduction: false')==1,'Expected safe committed local configuration'
config=config.replace('allowLocalProduction: false','allowLocalProduction: true').encode()
class Preview(SimpleHTTPRequestHandler):
 def do_GET(self):
  if urlsplit(self.path).path=='/assets/config.js':
   self.send_response(200);self.send_header('Content-Type','text/javascript; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(config)));self.end_headers();self.wfile.write(config)
  else:super().do_GET()
with ThreadingHTTPServer(('127.0.0.1',args.port),partial(Preview,directory=str(ROOT))) as server:
 print(f'REAL DELIVERY ENABLED for this preview only: http://127.0.0.1:{args.port}/contact/index.html',flush=True)
 print('Complete the real checkbox and submit only a clearly labelled test inquiry. Ctrl+C stops the preview. Repository files are unchanged.',flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
