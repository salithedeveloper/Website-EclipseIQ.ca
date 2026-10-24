#!/usr/bin/env python3
"""Generate a lightweight sharing card, not a logo. Requires Pillow only to regenerate."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root = Path(__file__).resolve().parents[1]
im = Image.new('RGB',(1200,630),'#102f46'); d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def text(x,y,s,size,fill='#f7f9f6',family=font):
    d.text((x,y),s,font=ImageFont.truetype(family,size),fill=fill)
d.line((65,105,1135,105),fill='#476879',width=1)
text(65,48,'EclipseIQ Technologies Inc.',24)
text(65,178,'Insurance technology.',64)
text(65,267,'Business perspective.',64,'#8edfd3',serif)
text(65,424,'Advisory  /  Leadership  /  Software & systems',23,'#c1d3dc')
d.line((65,520,1135,520),fill='#476879',width=1)
text(65,553,'eclipseiq.ca',20,'#c1d3dc')
im.save(root/'assets/social.png',optimize=True)
