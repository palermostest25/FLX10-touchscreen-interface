#!/usr/bin/env python3
"""Structural/safety lint. This is NOT a VirtualDJ SDK parser or runtime test."""
from io import BytesIO
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from PIL import Image

ELEMENTS = {'skin','font','logo','oninit','button','textzone','square','panel','deck',
            'scratchwave','songpos','browser','filelist','pos','size','text','off',
            'over','down','selected','mouserect','tooltip','grid','cue','mask','cues',
            'up','colors','lists','columns','search','toolbars','scrollbars',
            'fontsearch','fontheader','textselected'}
POSITIONED = {'button','textzone','square','logo','scratchwave','songpos','browser','filelist'}


def bounds(e):
    p,s=e.find('pos'),e.find('size')
    assert p is not None and s is not None, f'Missing geometry: {e.tag}'
    return tuple(int(v) for v in (p.get('x'),p.get('y'),s.get('width'),s.get('height')))


def validate(path):
    with ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==len(set(names)), 'Duplicate archive entry'
        assert all('/' not in n and '\\' not in n for n in names), 'Skin must be flat'
        xmls=[n for n in names if n.endswith('.xml')]
        assert len(xmls)==1 and len(names)==2, 'Expected XML and PNG only'
        raw=z.read(xmls[0])
        assert b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw
        root=ET.fromstring(raw)
        assert root.tag=='skin' and root.get('version')=='8'
        assert (root.get('width'),root.get('height'),root.get('nbdecks'))==('1368','912','4')
        im=Image.open(BytesIO(z.read(root.get('image'))));im.load()
        assert im.size==(1368,1200) and im.mode=='RGBA'
    panels={e.get('name') for e in root.iter('panel') if e.get('name')}
    errors=[]
    for e in root.iter():
        if e.tag not in ELEMENTS: errors.append('Unsupported project vocabulary: '+e.tag)
        if e.tag in POSITIONED:
            x,y,w,h=bounds(e)
            if not (x>=0 and y>=0 and w>0 and h>0 and x+w<=1368 and y+h<=912):
                errors.append(f'Off canvas: {e.tag} {x,y,w,h}')
            if e.tag=='button' and e.get('action')!='nothing' and h<52:
                errors.append('Touch control below 52 design pixels')
        for state in ('up','down','over','off','selected','mask'):
            for sprite in e.findall(state):
                if 'x' in sprite.attrib and 'y' in sprite.attrib:
                    x,y=int(sprite.get('x')),int(sprite.get('y'))
                    if not (0<=x<im.width and 0<=y<im.height): errors.append('Sprite out of atlas')
        for attr in ('action','query','visibility'):
            script=e.get(attr,'')
            for name in re.findall(r"skin_panel '([^']+)'",script):
                if name not in panels: errors.append('Missing panel '+name)
            if e.tag=='oninit' and script and not re.fullmatch(r"skin_panel '[^']+' on(?: & skin_panel '[^']+' on)*",script):
                errors.append('Initialization may only select skin panels')
        if e.tag=='button' and re.search(r'\bload\b',e.get('action','')):
            if not re.fullmatch(r'deck [1-4] play \? nothing : deck [1-4] load', e.get('action','')):
                errors.append('Unguarded load action')
            else:
                decks=re.findall(r'deck ([1-4])',e.get('action'))
                if decks[0]!=decks[1]: errors.append('Guard and load deck differ')
    # Every seekable native renderer must have an explicit later no-op hit shield.
    for parent in root.iter():
        children=list(parent)
        for i,e in enumerate(children):
            if e.tag in {'scratchwave','songpos'}:
                found=False
                for later in children[i+1:]:
                    if later.tag=='button' and later.get('action')=='nothing' and bounds(later)==bounds(e):
                        m=later.find('mouserect')
                        if m is not None and tuple(int(m.get(k)) for k in ('x','y','width','height'))==bounds(e):
                            found=True;break
                if not found: errors.append('Missing waveform input shield')
    assert not errors, '\n'.join(errors)
    print(f'PASS structure: {path.name} ({len(list(root.iter()))} XML elements). Runtime NOT RUN.')
    return root


if __name__=='__main__':
    for arg in sys.argv[1:] or [str(Path(__file__).resolve().parents[1]/'dist/AZ-Touch-3x2.zip')]:
        validate(Path(arg))
