#!/usr/bin/env python3
"""Offline EMPTY-state geometry diagram. Never used as VirtualDJ runtime evidence."""
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ACTIVE={'waveform','four','display1'}


def visible(expr):
    if not expr:return True
    if expr.startswith('not skin_panel '):return expr.split("'")[1] not in ACTIVE
    if expr.startswith('skin_panel '):return expr.split("'")[1] in ACTIVE
    if expr=='not loaded' or expr.startswith('not has_cue'):return True
    if expr=="display_time 'remain'":return True
    return False


def geometry(e):
    p,s=e.find('pos'),e.find('size')
    if p is None or s is None:return None
    return tuple(int(v) for v in (p.get('x'),p.get('y'),s.get('width'),s.get('height')))


def font(size):
    for path in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/segoeui.ttf']:
        if Path(path).exists():return ImageFont.truetype(path,size)
    return ImageFont.load_default(size=size)


def main():
    tree=ET.parse(ROOT/'skin/az-touch.xml').getroot()
    im=Image.open(ROOT/'skin/az-touch.png').crop((0,0,1368,912)).convert('RGB')
    draw=ImageDraw.Draw(im)
    def label(value,rect,t):
        x,y,w,h=rect;f=font(int(t.get('fontsize','18')))
        value=value or '';align=t.get('align','left')
        while value and draw.textlength(value,font=f)>w-4:value=value[:-1]
        dx=(w-draw.textlength(value,font=f))/2 if align=='center' else w-draw.textlength(value,font=f)-2 if align=='right' else 2
        draw.text((x+dx,y+h/2+int(t.get('dy','0'))),value,font=f,fill=t.get('color','#ffffff'),anchor='lm')
    def walk(e):
        if e.tag=='panel' and e.get('name') and e.get('name') not in ACTIVE:return
        if not visible(e.get('visibility')):return
        g=geometry(e)
        if g:
            x,y,w,h=g;rect=(x,y,x+w-1,y+h-1)
            if e.tag=='square':
                draw.rectangle(rect,fill=e.get('color'),outline=e.get('border_color'),width=int(e.get('border','1')))
            elif e.tag=='button':
                if e.get('action')=='nothing':return
                state=e.find('selected' if visible(e.get('query','false')) else 'off')
                draw.rectangle(rect,fill=state.get('color'),outline=state.get('border'),width=int(state.get('border_size','1')))
                t=e.find('text');value=t.get('text') or ('--:--' if 'get_time' in t.get('action','') else '')
                label(value,g,t)
            elif e.tag=='textzone':
                t=e.find('text');value=t.get('text') or ('--:--' if t.get('format')=='%hour' else '')
                label(value,g,t)
            elif e.tag in ('scratchwave','songpos'):
                draw.rectangle(rect,fill='#090909')
                label('NATIVE LIVE WAVEFORM' if e.tag=='scratchwave' else 'NATIVE TRACK OVERVIEW',g,{'fontsize':'12','color':'#44515c','align':'center'})
            elif e.tag=='logo':label('VirtualDJ',g,{'fontsize':'22','color':'#b8c2cd','align':'right'})
        for c in e:
            if c.tag not in ('text','textselected','off','on','up','down','over','selected','pos','size'):walk(c)
    walk(tree)
    # Keep the evidence disclaimer outside the skin frame.
    out=Image.new('RGB',(1368,956),'#202020');out.paste(im,(0,44));d=ImageDraw.Draw(out)
    d.text((18,22),'LAYOUT ONLY / EMPTY HOST STATE / NOT A VIRTUALDJ SCREENSHOT',font=font(18),fill='#ffffff',anchor='lm')
    path=ROOT/'docs/screenshots/layout-reference-structure.png';out.save(path)
    print(path)


if __name__=='__main__':main()
