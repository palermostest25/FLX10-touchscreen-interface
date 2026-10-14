#!/usr/bin/env python3
"""Offline EMPTY-state geometry diagram. Never used as VirtualDJ runtime evidence."""
from pathlib import Path
import argparse
import math
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
ACTIVE={'waveform','two12'}
ILLUSTRATIVE=False


def visible(expr,deck=1):
    if not expr:return True
    if ' & ' in expr:return all(visible(part,deck) for part in expr.split(' & '))
    if expr.startswith('not skin_panel '):return expr.split("'")[1] not in ACTIVE
    if expr.startswith('skin_panel '):return expr.split("'")[1] in ACTIVE
    if expr.startswith('not '):return not visible(expr[4:],deck)
    if expr=="display_time 'remain'":return True
    if expr=="setting 'skinWaveformType' 'shapes'":return True
    if ILLUSTRATIVE:
        if expr=='loaded':return True
        if expr=='play':return deck in (1,2)
        if expr=='masterdeck':return deck==1
        if expr=='is_sync':return deck==2
        if expr.startswith('has_cue '):return int(expr.split()[-1])<=6
        if expr=='quantize_setcue':return True
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
    global ACTIVE,ILLUSTRATIVE
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['four','two12','two34'],default='two12')
    parser.add_argument('--illustrative',action='store_true')
    args=parser.parse_args();ACTIVE={'waveform',args.mode};ILLUSTRATIVE=args.illustrative
    tree=ET.parse(ROOT/'skin/az-touch.xml').getroot()
    im=Image.open(ROOT/'skin/az-touch.png').crop((0,0,1368,912)).convert('RGB')
    draw=ImageDraw.Draw(im)
    def label(value,rect,t):
        x,y,w,h=rect;f=font(int(t.get('fontsize','18')))
        value=value or '';align=t.get('align','left')
        while value and draw.textlength(value,font=f)>w-4:value=value[:-1]
        dx=(w-draw.textlength(value,font=f))/2 if align=='center' else w-draw.textlength(value,font=f)-2 if align=='right' else 2
        draw.text((x+dx,y+h/2+int(t.get('dy','0'))),value,font=f,fill=t.get('color','#ffffff'),anchor='lm')
    def value_for(t,deck):
        if t.get('text') is not None:return t.get('text')
        if not ILLUSTRATIVE:return '--:--' if 'get_time' in t.get('action','') or t.get('format')=='%hour' else ''
        action=t.get('action','');fmt=t.get('format','')
        values={'get_title':f'AZ layout study — Track {deck:02d}','get_artist':'Illustrative fixture',
                'get_filepath':f'X:/Design-study/track-{deck:02d}.wav','get_bpm':'125.00'}
        if action in values:return values[action]
        if 'get_time' in action:return ['05:30','02:10','05:08','00:45'][deck-1]
        if 'get_key' in action:return ['Ebm','Gm','Am','Fm'][deck-1]
        if fmt=='%pitch':return ['+0.02%','+0.00%','+0.10%','−0.05%'][deck-1]
        if fmt=='%hour':return '17:16'
        if fmt.startswith('%namecue'):return ['Intro','Phase A','Break','Build','Drop','Outro'][int(fmt[8:])-1]
        return ''
    def illustrative_wave(rect,deck,overview=False):
        # Explicit diagram fixture. This data is never added to skin XML/PNG/ZIP.
        x,y,w,h=rect;mid=y+h/2
        for px in range(w):
            phase=(px/(27 if overview else 77)+deck*0.3)%1
            kick=math.exp(-phase*6)
            phrase=0.65+0.35*math.sin(px*0.014+deck)**2
            body=phrase*(0.22+0.64*kick+0.1*math.sin(px*0.31)**2)
            low=min(h*0.45,body*h*0.43)
            midamp=low*(0.56+0.08*math.sin(px*0.1))
            high=low*(0.10+0.78*math.exp(-((phase-0.52)/0.09)**2))
            for amplitude,color in [(low,'#1678ff'),(midamp,'#f6a21a'),(high,'#f7f1dd')]:
                draw.line((x+px,mid-amplitude,x+px,mid+amplitude),fill=color)
    def walk(e,deck=1):
        deck=int(e.get('deck',deck))
        if e.tag=='panel' and e.get('name') and e.get('name') not in ACTIVE:return
        if not visible(e.get('visibility'),deck):return
        g=geometry(e)
        if g:
            x,y,w,h=g;rect=(x,y,x+w-1,y+h-1)
            if e.tag=='square':
                draw.rectangle(rect,fill=e.get('color'),outline=e.get('border_color'),width=int(e.get('border','1')))
            elif e.tag=='button':
                if e.get('action')=='nothing':return
                state=e.find('selected' if visible(e.get('query','false'),deck) else 'off')
                draw.rectangle(rect,fill=state.get('color'),outline=state.get('border'),width=int(state.get('border_size','1')))
                t=e.find('text');value=value_for(t,deck)
                label(value,g,t)
            elif e.tag=='textzone':
                t=e.find('text');value=value_for(t,deck)
                label(value,g,t)
            elif e.tag in ('scratchwave','songpos'):
                draw.rectangle(rect,fill='#090909')
                if ILLUSTRATIVE:
                    illustrative_wave(g,deck,e.tag=='songpos')
                    if e.tag=='songpos':draw.line((x+w*0.24,y,x+w*0.24,y+h),fill='#ffffff',width=1)
                else:label('NATIVE LIVE WAVEFORM' if e.tag=='scratchwave' else 'NATIVE TRACK OVERVIEW',g,{'fontsize':'12','color':'#a1a1a1','align':'center'})
            elif e.tag=='overlay':draw.rectangle(rect,fill='#ffffff')
            elif e.tag=='logo':label('VirtualDJ',g,{'fontsize':'22','color':'#b8c2cd','align':'right'})
        for c in e:
            if c.tag not in ('text','textselected','off','on','up','down','over','selected','pos','size'):walk(c,deck)
    walk(tree)
    # Keep the evidence disclaimer outside the skin frame.
    out=Image.new('RGB',(1368,956),'#202020');out.paste(im,(0,44));d=ImageDraw.Draw(out)
    caption='DESIGN STUDY / ILLUSTRATIVE TRACK DATA AND WAVE SHAPES / NOT VIRTUALDJ' if ILLUSTRATIVE else 'LAYOUT ONLY / EMPTY HOST STATE / NOT A VIRTUALDJ SCREENSHOT'
    d.text((18,22),caption,font=font(18),fill='#ffffff',anchor='lm')
    filename=f'layout-az-{args.mode}-illustrative.png' if ILLUSTRATIVE else 'layout-reference-structure.png'
    path=ROOT/'docs/screenshots'/filename;out.save(path)
    print(path)


if __name__=='__main__':main()
