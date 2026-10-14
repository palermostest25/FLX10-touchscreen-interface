#!/usr/bin/env python3
"""Generate an original SDK 8 skin and reproducible, flat VirtualDJ archives."""
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZipInfo, ZIP_STORED
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
W, H = 1368, 912
BG, CELL, LINE, MUTED = '#090909', '#11161d', '#34495e', '#7f8d9b'
COLORS = ['#00a9dc', '#00a9dc', '#00a9dc', '#00a9dc']
VERSION = '0.2.0'


def element(parent, tag, **attrs):
    return ET.SubElement(parent, tag, {k: str(v) for k, v in attrs.items()})


def box(parent, x, y, w, h):
    element(parent, 'pos', x=x, y=y)
    element(parent, 'size', width=w, height=h)


def square(parent, x, y, w, h, color=CELL, **attrs):
    e = element(parent, 'square', color=color, **attrs)
    box(e, x, y, w, h)
    return e


def text(parent, x, y, w, h, value, size=18, color='#eef5ff', dynamic=False,
         fmt=False, visibility=None, align='left'):
    e = element(parent, 'textzone', **({'visibility': visibility} if visibility else {}))
    box(e, x, y, w, h)
    element(e, 'text', font='Segoe UI', fontsize=size, color=color, align=align,
            **{('action' if dynamic else 'format' if fmt else 'text'): value})
    return e


def button(parent, x, y, w, h, label, action, query='false', color='#245e9f',
           dynamic=False, **attrs):
    e = element(parent, 'button', action=action, query=query, **attrs)
    box(e, x, y, w, h)
    for state, fill in [('off', '#10151c'), ('over', '#243647'), ('down', color), ('selected', color)]:
        element(e, state, color=fill, border=LINE, border_size=2, radius=0)
    element(e, 'text', font='Segoe UI', fontsize=18, color='#eef5ff', align='center',
            **{('action' if dynamic else 'text'): label})
    return e


def shield(parent, x, y, w, h):
    # Explicit hit rectangle avoids reliance on the alpha of an invisible graphic.
    e = element(parent, 'button', action='nothing', query='false',
                rightclick='nothing', middleclick='nothing', dblclick='nothing')
    box(e, x, y, w, h)
    element(e, 'off', color='transparent')
    element(e, 'mouserect', x=x, y=y, width=w, height=h)
    element(e, 'tooltip').text = 'Display only. Use the FLX10 to control playback.'


def root(name, image):
    e = ET.Element('skin', name=name, version='8', width=str(W), height=str(H),
                   nbdecks='4', image=image, author='AZ Touch project',
                   comment=f'Independent Surface 3:2 display. Hardware candidate {VERSION}.')
    element(e, 'font', name='Segoe UI')
    text(e, 24, 14, 230, 42, 'AZ TOUCH', 30, COLORS[0])
    text(e, 255, 18, 560, 32, 'FLX10 / FOUR-DECK TOUCH DISPLAY', 16, MUTED)
    text(e, 952, 18, 150, 32, '%hour', 22, fmt=True, align='right')
    logo = element(e, 'logo')
    box(logo, 1150, 20, 190, 30)
    return e


def status(parent, x, y, w, deck, compact=False):
    c = COLORS[deck-1]
    d = element(parent, 'deck', deck=deck)
    square(d, x, y, w, 96, border=1, border_color=LINE)
    square(d, x, y, 5, 96, c)
    text(d, x+16, y+8, 34, 28, str(deck), 24, c)
    text(d, x+56, y+8, w-70, 26, 'get_title', 17, dynamic=True, visibility='loaded')
    text(d, x+56, y+8, w-70, 26, 'EMPTY', 17, MUTED, visibility='not loaded')
    text(d, x+16, y+39, 92, 26, 'get_bpm', 20, dynamic=True, visibility='loaded')
    text(d, x+119, y+39, 75, 26, 'get_key \'harmonic\'', 20, c, dynamic=True, visibility='loaded')
    text(d, x+w-117, y+39, 101, 26, 'get_time \'remain\' \'short\'', 20,
         dynamic=True, visibility='loaded', align='right')
    text(d, x+16, y+70, 118, 20, 'PLAYING', 14, c, visibility='play')
    text(d, x+16, y+70, 118, 20, 'STOPPED', 14, MUTED, visibility='loaded & not play')
    text(d, x+w-170, y+70, 154, 20, 'LOAD LOCKED', 14, COLORS[1], visibility='play', align='right')


def live_row(parent, deck, y, height):
    c = COLORS[deck-1]
    d = element(parent, 'deck', deck=deck)
    square(d, 24, y, 1320, height, border=1, border_color=LINE)
    square(d, 24, y, 5, height, c)
    text(d, 40, y+8, 40, 42, str(deck), 32, c)
    text(d, 92, y+8, 650, 30, 'get_title', 23, dynamic=True, visibility='loaded')
    text(d, 92, y+8, 650, 30, 'NO TRACK LOADED', 23, MUTED, visibility='not loaded')
    text(d, 92, y+39, 650, 24, 'get_artist', 17, MUTED, dynamic=True, visibility='loaded')
    # The time button affects display format only; no transport action.
    timer = button(d, 775, y+8, 170, 52, 'get_time \'short\'',
           "display_time 'remain' ? display_time 'elapsed' : display_time 'remain'",
           dynamic=True)
    timer.find('text').set('dy', '-8')
    text(d, 775, y+47, 170, 12, 'REMAIN / TAP', 12, MUTED,
         visibility="display_time 'remain'", align='center')
    text(d, 775, y+47, 170, 12, 'ELAPSED / TAP', 12, MUTED,
         visibility="not display_time 'remain'", align='center')
    text(d, 961, y+9, 119, 28, 'get_bpm', 25, dynamic=True, visibility='loaded')
    text(d, 961, y+39, 119, 22, '%pitch', 16, MUTED, fmt=True, visibility='loaded')
    text(d, 1095, y+9, 82, 28, "get_key 'harmonic'", 25, c, dynamic=True, visibility='loaded')
    text(d, 1190, y+9, 138, 24, 'PLAYING', 16, c, visibility='play', align='right')
    text(d, 1190, y+9, 138, 24, 'STOPPED', 16, MUTED, visibility='loaded & not play', align='right')
    text(d, 1190, y+39, 138, 22, 'LOOP', 15, c, visibility='loop', align='right')
    # Q LOOP/Q CUE reflect individual native quantize options, not an invented aggregate.
    text(d, 1095, y+39, 80, 12, 'Q LOOP', 12, c, visibility='quantize_loop')
    text(d, 1095, y+52, 80, 12, 'Q CUE', 12, c, visibility='quantize_setcue')
    wx, wy, ww, wh = 92, y+66, 940, height-93
    square(d, wx, wy, ww, wh, '#090f18')
    sw = element(d, 'scratchwave', orientation='horizontal', color=c, color2='#d6efff')
    box(sw, wx, wy, ww, wh)
    element(sw, 'grid', mainsize=2, phrasesize=3, size=1, height=7, pos=0,
            maincolor='#dde8f8', phrasecolor=c, color=LINE, transparency=0.65,
            mirrored='yes', background='no')
    cue = element(sw, 'cue', y=0, height=wh)
    element(cue, 'text', dx=12, dy=0, size=14)
    element(cue, 'mask', width=12, height=wh, x=0, y=912)
    # Centre needle rendered separately, followed by a no-op hit shield.
    square(d, wx+ww//2, wy, 2, wh, '#f0f6ff')
    shield(d, wx, wy, ww, wh)
    spx, spy, spw, sph = 1054, y+66, 274, height-93
    square(d, spx, spy, spw, sph, '#090f18')
    sp = element(d, 'songpos', orientation='horizontal', colorPlayed='#405166',
                 colorBass=c, colorMed=c, colorHigh='#eff8ff')
    box(sp, spx, spy, spw, sph)
    cues = element(sp, 'cues')
    element(cues, 'size', width=8, height=20)
    for state in ['up', 'down', 'over']:
        element(cues, state, x=24, y=912)
    shield(d, spx, spy, spw, sph)
    # Eight passive cue labels; touching cannot create or trigger cues.
    for n in range(1, 9):
        cx = 92+(n-1)*117
        square(d, cx, y+height-27, 109, 22, '#172434')
        text(d, cx+4, y+height-27, 101, 22, "cue_display "+str(n), 13, c,
             dynamic=True, visibility='has_cue '+str(n))
        text(d, cx+4, y+height-27, 101, 22, chr(64+n)+' —', 13, MUTED,
             visibility='not has_cue '+str(n))
    text(d, 1054, y+height-27, 274, 22, 'DISPLAY ONLY / USE FLX10', 12, MUTED, align='center')


def browser(parent, y=224, tag=False):
    if tag:
        b = element(parent, 'filelist', source='sidelist', lineheight='1.8')
    else:
        b = element(parent, 'browser', toolbar='yes', folders='yes', sideview='no',
                    infos='no', effects='no', searchbar='yes', lineheight='1.8')
    box(b, 24, y, 1320, 520)
    colors = element(b, 'colors', background=BG)
    element(colors, 'lists', background=CELL, stripes='#152332', selected='#214f7d',
            focus='#286498', text='#eef5ff', selectedtext='#ffffff', focustext='#ffffff', label=MUTED)
    element(colors, 'columns', background='#223248', text='#c9d9eb')
    element(colors, 'search', background='#182638', border=LINE, text='#ffffff', cursor='#48aaff')
    element(colors, 'toolbars', background='#152332', text='#eef5ff', label=MUTED)
    element(colors, 'scrollbars', background='#182638', button='#8da9c6')
    for name in ['font', 'fontsearch', 'fontheader']:
        element(b, name, size=20)


def performance_wave(parent, deck, y, height):
    """Reference hierarchy: one large native wave, not a metadata card per row."""
    d=element(parent,'deck',deck=deck)
    button(d,160,y,44,height,str(deck),f"skin_panel 'display{deck}' on",
           query=f"skin_panel 'display{deck}'",color='#106d9d')
    sw=element(d,'scratchwave',orientation='horizontal',color='full')
    box(sw,212,y,1132,height)
    element(sw,'grid',mainsize=2,phrasesize=3,size=1,height=6,pos=0,
            maincolor='#dddddd',phrasecolor='#ffffff',color='#4a4a4a',
            transparency=0.5,mirrored='yes',background='no')
    cue=element(sw,'cue',y=0,height=height)
    element(cue,'text',dx=12,dy=0,size=14)
    element(cue,'mask',width=12,height=height,x=0,y=912)
    square(d,777,y,2,height,'#ffffff')
    shield(d,212,y,1132,height)


def cue_bank(parent, deck):
    x=160+(deck-1)*300
    d=element(parent,'deck',deck=deck)
    text(d,x,488,282,20,'DECK '+str(deck),13,'#00a9dc')
    for n in range(1,9):
        cx=x+((n-1)%4)*74;cy=512+((n-1)//4)*44
        square(d,cx,cy,68,38,border=2,border_color=LINE)
        square(d,cx+2,cy+2,64,3,'#00a9dc',visibility='has_cue '+str(n))
        text(d,cx+4,cy+7,60,25,'cue_display '+str(n),14,'#f6f6f6',
             dynamic=True,visibility='has_cue '+str(n),align='center')
        text(d,cx+4,cy+7,60,25,chr(64+n),14,'#3e4f60',
             visibility='not has_cue '+str(n),align='center')


def player_tile(parent,deck,x,y):
    d=element(parent,'deck',deck=deck)
    square(d,x,y,654,116)
    text(d,x+10,y+5,36,38,str(deck),30,'#00a9dc')
    text(d,x+56,y+7,496,27,'get_title',21,dynamic=True,visibility='loaded')
    text(d,x+56,y+7,496,27,'NO TRACK LOADED',21,'#91a1af',visibility='not loaded')
    text(d,x+555,y+7,84,22,'PLAYING',12,'#00a9dc',visibility='play',align='right')
    text(d,x+56,y+36,125,16,'REMAIN',12,MUTED,visibility="display_time 'remain'")
    text(d,x+56,y+36,125,16,'ELAPSED',12,MUTED,visibility="not display_time 'remain'")
    timer=button(d,x+54,y+48,142,52,"get_time 'short'",
                 "display_time 'remain' ? display_time 'elapsed' : display_time 'remain'",dynamic=True)
    for tag in ('off','over','down','selected'):
        timer.find(tag).set('color',CELL);timer.find(tag).set('border_size','0')
    timer.find('text').set('fontsize','30');timer.find('text').set('align','left')
    text(d,x+210,y+36,100,16,'BPM',12,'#fa834a')
    text(d,x+210,y+52,110,40,'get_bpm',30,'#ff7b48',dynamic=True,visibility='loaded')
    text(d,x+330,y+36,100,16,'KEY',12,MUTED)
    text(d,x+330,y+52,100,40,"get_key 'harmonic'",30,'#00d2a0',dynamic=True,visibility='loaded')
    text(d,x+435,y+36,110,16,'TEMPO',12,MUTED)
    text(d,x+435,y+52,110,40,'%pitch',26,'#c0ccda',fmt=True,visibility='loaded')
    text(d,x+56,y+101,490,13,'get_artist',13,MUTED,dynamic=True,visibility='loaded')
    text(d,x+555,y+41,84,18,'LOOP',12,'#00a9dc',visibility='loop',align='right')
    text(d,x+555,y+63,84,18,'Q LOOP',12,'#00a9dc',visibility='quantize_loop',align='right')
    text(d,x+555,y+85,84,18,'Q CUE',12,'#00a9dc',visibility='quantize_setcue',align='right')
    # Reference deck tiles contain a large overall waveform. Keep host rendering live.
    # The 3:2 height allows an overview below each tile instead of a squeezed mini wave.
    sp=element(d,'songpos',orientation='horizontal',colorPlayed='#535353',
               colorBass='#ed7054',colorMed='#66e499',colorHigh='#c8b1ff')
    box(sp,x,y+116,654,30)
    cues=element(sp,'cues');element(cues,'size',width=8,height=20)
    for state in ('up','down','over'):element(cues,state,x=24,y=912)
    shield(d,x,y+116,654,30)


def performance(parent):
    for name,decks in [('four',[1,2,3,4]),('two12',[1,2]),('two34',[3,4])]:
        mode=element(parent,'panel',name=name,group='az-performance',visible='yes' if name=='four' else 'no')
        height=72 if len(decks)==4 else 148
        for i,deck in enumerate(decks): performance_wave(mode,deck,184+i*(height+4),height)
    # Four cue banks and a 2x2 deck grid stay visible for every waveform pair.
    for deck in range(1,5):cue_bank(parent,deck)
    for deck,x,y in [(1,24,606),(2,690,606),(3,24,756),(4,690,756)]:
        player_tile(parent,deck,x,y)
    for deck in range(1,5):
        panel=element(parent,'panel',name=f'display{deck}',group='az-display',visible='yes' if deck==1 else 'no')
        d=element(panel,'deck',deck=deck)
        text(d,24,180,124,32,'DECK '+str(deck),24,'#00a9dc')
        text(d,24,225,124,20,'BPM',13,MUTED)
        text(d,24,249,124,34,'get_bpm',30,'#ff7b48',dynamic=True,visibility='loaded')
        text(d,24,298,124,20,'KEY',13,MUTED)
        text(d,24,322,124,34,"get_key 'harmonic'",30,'#00d2a0',dynamic=True,visibility='loaded')
        text(d,24,372,124,20,'TEMPO',13,MUTED)
        text(d,24,396,124,34,'%pitch',28,'#eef4fa',fmt=True,visibility='loaded')
        text(d,24,460,124,23,'TOUCH LOCK',13,'#fa834a')


def loads(parent, tag=False):
    for deck in range(1, 5):
        x=24+(deck-1)*204
        action=f'deck {deck} play ? nothing : deck {deck} load'
        b=button(parent, x, 162, 192, 52, f'LOAD {deck}', action, query=f'deck {deck} play', color='#79353e')
        element(b,'textselected',fontsize=16,color='#ffffff',align='center',text='PLAYING / LOCKED')
    if not tag:
        button(parent, 840, 162, 156, 52, 'PARENT',
               "browser_window 'folders' & browser_scroll 'parent'")
        button(parent, 1008, 162, 156, 52, 'ADD TO TAG', "browser_window 'songs' & sidelist_add")
        button(parent, 1176, 162, 168, 52, 'KEYBOARD', 'search & show_keyboard')


def make_skin():
    r = root('AZ Touch 3x2 · Hardware candidate', 'az-touch.png')
    pages = [('source','SOURCE'), ('browse','BROWSE'), ('tag','TAG LIST'),
             ('playlist','PLAYLIST'), ('search','SEARCH'), ('waveform','WAVEFORM')]
    for i,(name,label) in enumerate(pages):
        action=f"skin_panel '{name}' on"
        if name in ('source','playlist'): action+=" & browser_window 'folders'"
        if name=='browse': action+=" & browser_window 'songs'"
        if name=='search': action+=' & search & show_keyboard'
        if name=='tag': action+=" & browser_window 'sidelist'"
        button(r, 24+i*165, 68, 153, 52, label, action, query=f"skin_panel '{name}'")
    button(r, 1014, 68, 155, 52, 'FULLSCREEN', 'maximize')
    button(r, 1181, 68, 163, 52, 'SETTINGS', 'settings')
    # oninit only controls visibility, never the mixer, audio device, or playback.
    element(r, 'oninit', action="skin_panel 'waveform' on & skin_panel 'four' on & skin_panel 'display1' on")
    p=element(r, 'panel', name='waveform', group='az-pages', visible='yes')
    for x,w,name,label in [(24,160,'four','4 DECK'),(196,218,'two12','2 DECK / 1 + 2'),(426,218,'two34','2 DECK / 3 + 4')]:
        button(p,x,130,w,52,label,f"skin_panel '{name}' on",query=f"skin_panel '{name}'")
    text(p, 676, 139, 120, 30, 'SOURCE', 13, MUTED, align='right')
    performance(p)
    hints={
        'source':'SOURCE / Expand OneLibrary and choose the attached test USB; local folders stay separate.',
        'browse':'BROWSE / Select a track, then choose LOAD 1–4. Playing targets are locked.',
        'playlist':'PLAYLIST / Select a playlist in the native folder tree. No copying or conversion needed by this skin.',
        'search':'SEARCH / Type in the native search bar. KEYBOARD opens the VirtualDJ touch keyboard.',
        'tag':'TAG LIST / VirtualDJ SIDELIST. This list is local to VirtualDJ, not a Pioneer USB Tag List.'}
    for name in hints:
        page=element(r,'panel',name=name,group='az-pages',visible='no')
        text(page,24,126,1320,30,hints[name],16,MUTED)
        loads(page,tag=name=='tag')
        browser(page,tag=name=='tag')
        if name=='tag':
            button(page,1180,162,164,52,'BROWSE',"skin_panel 'browse' on")
    # Common status strips and source breadcrumb survive all page switches.
    text(p,812,139,532,30,'get_browsed_folder_path',13,MUTED,dynamic=True)
    browse_status=element(r,'panel',visibility="not skin_panel 'waveform'")
    text(browse_status,24,752,115,25,'SOURCE',13,MUTED)
    text(browse_status,139,752,1205,25,'get_browsed_folder_path',15,dynamic=True)
    for deck in range(1,5): status(browse_status,24+(deck-1)*334,786,318,deck)
    text(browse_status,24,886,1320,20,'AZ TOUCH / INDEPENDENT INTERFACE',12,MUTED)
    return r


def make_spike():
    r=root('AZ Touch SDK spike · Hardware candidate', 'az-touch.png')
    button(r,24,68,220,52,'WAVEFORM',"skin_panel 'spike-wave' on",query="skin_panel 'spike-wave'")
    button(r,260,68,220,52,'BROWSE',"skin_panel 'spike-browse' on",query="skin_panel 'spike-browse'")
    button(r,1100,68,244,52,'SETTINGS','settings')
    a=element(r,'panel',name='spike-wave',group='spike',visible='yes')
    live_row(a,1,194,250);live_row(a,2,456,250)
    b=element(r,'panel',name='spike-browse',group='spike',visible='no')
    loads(b);browser(b)
    return r


def write_xml(path, r):
    ET.indent(r, space='  ')
    ET.ElementTree(r).write(path, encoding='utf-8', xml_declaration=True)


def package(path, files):
    with ZipFile(path, 'w', compression=ZIP_STORED) as z:
        for name,data in sorted(files.items()):
            info=ZipInfo(name, date_time=(2026,1,1,0,0,0))
            info.compress_type=ZIP_STORED;info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,data)


def main():
    skin=ROOT/'skin';dist=ROOT/'dist';skin.mkdir(exist_ok=True);dist.mkdir(exist_ok=True)
    # Background + original cue sprites. No fake audio bars or track names.
    atlas=Image.new('RGBA',(W,1200),BG);draw=ImageDraw.Draw(atlas)
    draw.rectangle((0,0,W,61),fill=BG)
    draw.line((24,60,1344,60),fill=LINE,width=1)
    draw.rectangle((0,912,11,1199),fill=(0,0,0,255))
    draw.rectangle((0,912,2,1199),fill=(255,255,255,255))
    draw.polygon([(0,912),(11,912),(0,923)],fill=(255,255,255,255))
    draw.rectangle((24,912,31,931),fill='#eef5ff')
    atlas.save(skin/'az-touch.png',optimize=False,compress_level=9)
    r=make_skin();write_xml(skin/'az-touch.xml',r)
    write_xml(skin/'az-touch-spike.xml',make_spike())
    for file,xml in [('AZ-Touch-3x2.zip','az-touch.xml'),('AZ-Touch-SDK-Spike.zip','az-touch-spike.xml')]:
        package(dist/file,{xml:(skin/xml).read_bytes(),'az-touch.png':(skin/'az-touch.png').read_bytes()})
    bindings=[]
    def walk(e,deck='global',panel='global'):
        deck=e.get('deck',deck);panel=e.get('name',panel) if e.tag=='panel' else panel
        for attr in ['action','query','visibility','rightclick','middleclick','dblclick','format']:
            if attr in e.attrib:
                bindings.append(dict(element=e.tag,deck=deck,panel=panel,attribute=attr,
                                     expression=e.get(attr),runtime_evidence='NOT RUN'))
        for child in e: walk(child,deck,panel)
    walk(r)
    (ROOT/'docs'/'bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
    sums=[]
    for path in sorted(dist.glob('*.zip')):
        sums.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}')
    (dist/'SHA256SUMS.txt').write_text('\n'.join(sums)+'\n')
    print('\n'.join(sums))
    # Validation is structural, and is never advertised as VirtualDJ execution.
    from validate_skin import validate
    for path in sorted(dist.glob('*.zip')): validate(path)


if __name__=='__main__': main()
