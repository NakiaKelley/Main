#!/usr/bin/env python3
"""
Citizens Catering — Charcuterie & Grazing Spreads Menu
v1.6 baseline build script — recovered from the original Claude.ai chat.

Preserved here verbatim (chat-formatting artifacts cleaned, paths made
repo-relative) as the canonical baseline. Apply edits in a versioned
copy of this file (build_charcuterie_v1_7.py, etc.) so this baseline
stays known-good.
"""

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

BASE = '/usr/share/fonts/truetype/google-fonts'
pdfmetrics.registerFont(TTFont('Pop',   f'{BASE}/Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('PopB',  f'{BASE}/Poppins-Bold.ttf'))
pdfmetrics.registerFont(TTFont('PopM',  f'{BASE}/Poppins-Medium.ttf'))
pdfmetrics.registerFont(TTFont('PopL',  f'{BASE}/Poppins-Light.ttf'))
pdfmetrics.registerFont(TTFont('PopI',  f'{BASE}/Poppins-Italic.ttf'))
pdfmetrics.registerFont(TTFont('PopLI', f'{BASE}/Poppins-LightItalic.ttf'))
pdfmetrics.registerFont(TTFont('PopMI', f'{BASE}/Poppins-MediumItalic.ttf'))

TEAL  = HexColor('#00333D'); TDARK = HexColor('#001E25')
AMBER = HexColor('#D4832A'); AMDRK = HexColor('#B8671A')
RED   = HexColor('#B83227')
CREAM = HexColor('#FAF6EF'); PARCH = HexColor('#F2ECE0')
TAN   = HexColor('#DDD0B8'); MID   = HexColor('#C8B89A')
DK    = HexColor('#3E3A32'); SUB   = HexColor('#8A8070')
WHITE = white

W, H  = letter
ML    = 0.65*inch; MR = 0.65*inch
CW    = W-ML-MR; COL = (CW-18)/2; G = 18
HDR   = 48; FTR = 22
BT    = H-HDR-0.42*inch; BB = 0.52*inch+FTR+8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SCRIPT_DIR, 'assets')
LOGO_W = ImageReader(os.path.join(ASSETS, 'logo_white.png'))
# Aspect ratio measured from CITIZENS_LOGO_NAVY.png (1313 x 714)
LR = 1313 / 714
def lh(w): return w / LR

# ── PAGE CHROME ───────────────────────────────────────────────

def cover(c, version="v1.6"):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(TDARK); c.rect(0,H-130,W,130,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(W-90,H-130,90,130,fill=1,stroke=0)
    c.setFillColor(TDARK); c.rect(W-90,H-130,90,44,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(0,H-133,W-90,3,fill=1,stroke=0)
    c.setFillColor(PARCH); c.rect(0,0,24,H-133,fill=1,stroke=0)
    c.setFillColor(TAN);   c.rect(20,0,4,H-133,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(0,0,6,H-133,fill=1,stroke=0)
    lw = 2.1*inch
    c.drawImage(LOGO_W,ML,H-130+(130-lh(lw))/2,width=lw,height=lh(lw),mask='auto')
    cy = H*0.42
    c.setStrokeColor(AMBER); c.setLineWidth(1.5)
    c.line(ML+30,cy+96,ML+30+2.8*inch,cy+96)
    c.setFillColor(TEAL); c.setFont('PopB',36); c._charSpace=0
    c.drawString(ML+30,cy+60,'CHARCUTERIE')
    c.setFillColor(AMDRK); c.setFont('PopL',18); c._charSpace=3
    c.drawString(ML+30,cy+36,'& GRAZING SPREADS'); c._charSpace=0
    c.setStrokeColor(AMBER); c.setLineWidth(1.5)
    c.line(ML+30,cy+28,ML+30+3.0*inch,cy+28)
    c.setFillColor(SUB); c.setFont('PopLI',9); c._charSpace=0.5
    tag='Boards   ·   Platters   ·   Favor Cups   ·   Sweet & Savory Spreads'
    c.drawString(ML+30,cy+12,tag); c._charSpace=0
    c.setFillColor(AMBER)
    for i,dx in enumerate([0,8,16,24,32,40]):
        c.circle(ML+30+dx,cy-5,1.6 if i%2==0 else 2.4,fill=1,stroke=0)
    # Offerings card
    card_x=W*0.55; card_y=cy-20; card_w=W-card_x-MR; card_h=116
    c.setFillColor(PARCH); c.setStrokeColor(TAN); c.setLineWidth(0.5)
    c.roundRect(card_x,card_y-card_h,card_w,card_h,4,fill=1,stroke=1)
    c.setFillColor(AMBER); c.rect(card_x,card_y-card_h,4,card_h,fill=1,stroke=0)
    c.setFillColor(TEAL); c.setFont('PopB',7.5); c._charSpace=1
    c.drawString(card_x+12,card_y-14,'OUR OFFERINGS'); c._charSpace=0
    c.setFillColor(DK); c.setFont('Pop',7.5)
    for i,o in enumerate(['Standard & Premium Boards','Charcuterie Favor Cups',
                          'Savory Grazing Boards','Dessert & Sweet Grazing Boards',
                          'Candy Bar & Snack Boards','Specialty & Custom Builds','Tablescapes & Full Setups']):
        oy=card_y-27-i*12
        c.setFillColor(AMBER); c.circle(card_x+14,oy+2.5,1.5,fill=1,stroke=0)
        c.setFillColor(DK); c.drawString(card_x+20,oy,o)
    c.setFillColor(TDARK); c.rect(0,0,W,86,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(0,86,W,2,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('PopM',8.5)
    ct='citizenscatering.com   •   (855) 227-3783   •   nakia@weserveyourcity.org'
    ctw=c.stringWidth(ct,'PopM',8.5); c.drawString((W-ctw)/2,42,ct)
    c.setFillColor(MID); c.setFont('PopL',7); c._charSpace=1
    ver=f'{version}  •  2026'; vw=c.stringWidth(ver,'PopL',7)
    c.drawString((W-vw)/2,27,ver); c._charSpace=0

def phdr(c,section):
    c.setFillColor(CREAM); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(TEAL); c.rect(0,H-HDR,W,HDR,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(0,H-3,W,3,fill=1,stroke=0)
    c.rect(0,H-HDR,4,HDR,fill=1,stroke=0)
    lw=1.05*inch
    c.drawImage(LOGO_W,ML+4,H-HDR+(HDR-lh(lw))/2,width=lw,height=lh(lw),mask='auto')
    c.setFillColor(MID); c.setFont('PopM',7.5); c._charSpace=2
    snw=c.stringWidth(section,'PopM',7.5)
    c.drawString(W-MR-snw,H-HDR+(HDR-7.5)/2,section); c._charSpace=0
    c.setStrokeColor(AMBER); c.setLineWidth(0.75)
    c.line(0,H-HDR-0.75,W,H-HDR-0.75)

def pftr(c, version="v1.6"):
    fy=BB-6
    c.setStrokeColor(TAN); c.setLineWidth(0.75); c.line(ML,fy,W-MR,fy)
    c.setFillColor(TEAL); c.setFont('PopB',6); c._charSpace=1
    c.drawString(ML,fy-11,'CITIZENS CATERING'); c._charSpace=0
    c.setFillColor(SUB); c.setFont('Pop',6.5)
    ct='citizenscatering.com   |   (855) 227-3783   |   nakia@weserveyourcity.org'
    ctw=c.stringWidth(ct,'Pop',6.5); c.drawString((W-ctw)/2,fy-11,ct)
    c.setFont('PopL',6.5)
    vw=c.stringWidth(version,'PopL',6.5); c.drawString(W-MR-vw,fy-11,version)

# ── CONTENT PRIMITIVES ────────────────────────────────────────

def sh(c,y,title,sub=None,color=None):
    col=color if color else TEAL
    bh=30 if not sub else 42
    c.setFillColor(col); c.rect(ML,y-bh,CW,bh,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(ML,y-bh,4,bh,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('PopB',11.5); c._charSpace=1.5
    if sub:
        c.drawString(ML+14,y-18,title.upper()); c._charSpace=0
        c.setFillColor(MID); c.setFont('PopLI',8)
        c.drawString(ML+14,y-30,sub)
    else:
        c.drawString(ML+14,y-bh+10,title.upper()); c._charSpace=0
    return y-bh-10

def intr(c,y,text):
    c.setFillColor(SUB); c.setFont('PopI',7.5)
    words=text.split(); line=[]; lines=[]
    for w in words:
        test=' '.join(line+[w])
        if c.stringWidth(test,'PopI',7.5)<CW: line.append(w)
        else: lines.append(' '.join(line)); line=[w]
    if line: lines.append(' '.join(line))
    for ln in lines: c.drawString(ML,y,ln); y-=10
    c.setStrokeColor(TAN); c.setLineWidth(0.5); c.line(ML,y-2,W-MR,y-2)
    return y-10

def cat(c,y,title,color=None):
    col=color if color else TEAL
    c.setFillColor(col); c.setFont('PopB',7.5); c._charSpace=2
    c.drawString(ML,y,title.upper()); c._charSpace=0
    c.setStrokeColor(AMBER); c.setLineWidth(0.75)
    c.line(ML,y-3,W-MR,y-3)
    return y-14

def eh(c,cw,desc):
    if not desc: return 18
    words=desc.split(); line=[]; lines=[]
    for w in words:
        test=' '.join(line+[w])
        if c.stringWidth(test,'PopI',7.5)<cw-2: line.append(w)
        else: lines.append(' '.join(line)); line=[w]
    if line: lines.append(' '.join(line))
    return 13+len(lines)*9+6

def di(c,x,y,cw,name,desc='',tags='',price='',namecolor=None):
    nc=namecolor if namecolor else TEAL
    c.setFillColor(nc); c.setFont('PopM',8.5); c.drawString(x,y,name)
    tx=x+c.stringWidth(name,'PopM',8.5)+5
    for tag in ([t.strip() for t in tags.split('·')] if tags else []):
        if not tag: continue
        tw2=c.stringWidth(tag,'PopB',5.5)+6
        c.setFillColor(HexColor('#F0EBE0')); c.setStrokeColor(AMDRK); c.setLineWidth(0.4)
        c.roundRect(tx,y-1.5,tw2,9,1.5,fill=1,stroke=1)
        c.setFillColor(AMDRK); c.setFont('PopB',5.5)
        c.drawString(tx+3,y+0.5,tag); tx+=tw2+3
    if price:
        c.setFillColor(AMDRK); c.setFont('PopB',9)
        pw=c.stringWidth(price,'PopB',9); c.drawString(x+cw-pw,y,price)
    if desc:
        c.setFillColor(DK); c.setFont('PopI',7.5)
        words=desc.split(); line=[]; lines=[]
        for w in words:
            test=' '.join(line+[w])
            if c.stringWidth(test,'PopI',7.5)<cw-2: line.append(w)
            else: lines.append(' '.join(line)); line=[w]
        if line: lines.append(' '.join(line))
        dy=y-10
        for ln in lines: c.drawString(x,dy,ln); dy-=9
        total_h=13+len(lines)*9+5
    else: total_h=16
    c.setStrokeColor(TAN); c.setLineWidth(0.3)
    c.line(x,y-total_h+4,x+cw,y-total_h+4)
    return total_h

def twocol(c,y,left,right,bot,rowbg=None,namecolor=None):
    lx,rx=ML,ML+COL+G; li=ri=0
    bg=rowbg if rowbg else HexColor('#F5EFE4')
    while li<len(left) or ri<len(right):
        lh2=rh2=0
        if li<len(left): lh2=eh(c,COL,left[li][1] if len(left[li])>1 else '')
        if ri<len(right): rh2=eh(c,COL,right[ri][1] if len(right[ri])>1 else '')
        row_h=max(lh2,rh2,16)
        if y-row_h<bot: return y,left[li:],right[ri:]
        if (li+ri)%2==0:
            c.setFillColor(bg); c.rect(ML-4,y-row_h+2,CW+8,row_h-2,fill=1,stroke=0)
        if li<len(left):
            it=left[li]
            di(c,lx,y-2,COL,it[0],it[1] if len(it)>1 else '',it[2] if len(it)>2 else '',it[3] if len(it)>3 else '',namecolor)
            li+=1
        if ri<len(right):
            it=right[ri]
            di(c,rx,y-2,COL,it[0],it[1] if len(it)>1 else '',it[2] if len(it)>2 else '',it[3] if len(it)>3 else '',namecolor)
            ri+=1
        y-=row_h
    return y,[],[]

def board_card(c,y,name,tier,price,serves,includes,note='',accent=None):
    acc=accent if accent else AMBER
    card_h=18+len(includes)*11+(14 if note else 0)+24
    c.setFillColor(PARCH); c.setStrokeColor(TAN); c.setLineWidth(0.5)
    c.roundRect(ML,y-card_h,CW,card_h,4,fill=1,stroke=1)
    c.setFillColor(acc); c.rect(ML,y-card_h,4,card_h,fill=1,stroke=0)
    c.setFillColor(TEAL); c.setFont('PopB',9.5)
    c.drawString(ML+12,y-13,name)
    if tier:
        c.setFillColor(SUB); c.setFont('PopL',7.5)
        c.drawString(ML+12+c.stringWidth(name,'PopB',9.5)+8,y-12,tier)
    if serves:
        c.setFillColor(SUB); c.setFont('PopI',7)
        sw=c.stringWidth(serves,'PopI',7); c.drawString(W-MR-sw-4,y-12,serves)
    if price:
        c.setFillColor(AMDRK); c.setFont('PopB',11)
        pw=c.stringWidth(price,'PopB',11); c.drawString(W-MR-pw-4,y-24,price)
    c.setStrokeColor(TAN); c.setLineWidth(0.4)
    c.line(ML+12,y-28,W-MR-4,y-28)
    iy=y-40
    bul_w = W-MR-4-(ML+22)
    for inc in includes:
        c.setFillColor(acc); c.circle(ML+15,iy+2.5,1.5,fill=1,stroke=0)
        c.setFillColor(DK); c.setFont('Pop',7.5)
        words2=inc.split(); bline=[]; blines=[]
        for w2 in words2:
            test2=' '.join(bline+[w2])
            if c.stringWidth(test2,'Pop',7.5)<bul_w: bline.append(w2)
            else: blines.append(' '.join(bline)); bline=[w2]
        if bline: blines.append(' '.join(bline))
        for bi,bln in enumerate(blines):
            c.drawString(ML+22,iy,bln); iy-=9
        iy-=2
    if note:
        c.setFillColor(SUB); c.setFont('PopLI',6.5)
        c.drawString(ML+12,iy+2,note)
    return y-card_h-8

def pkg_grid(c,y,packages,bot,accent=None):
    acc=accent if accent else TEAL
    pkg_h=72
    rows=[packages[i:i+2] for i in range(0,len(packages),2)]
    for row in rows:
        if y-pkg_h<bot: return y
        for i,(name,subtitle,items_str,price) in enumerate(row):
            px=ML+i*(COL+G); pw=COL
            c.setFillColor(PARCH); c.setStrokeColor(TAN); c.setLineWidth(0.4)
            c.roundRect(px,y-pkg_h,pw,pkg_h,3,fill=1,stroke=1)
            c.setFillColor(acc); c.roundRect(px,y-18,pw,18,3,fill=1,stroke=0)
            c.rect(px,y-18,pw,9,fill=1,stroke=0)
            c.setFillColor(AMBER); c.rect(px,y-18,4,18,fill=1,stroke=0)
            c.setFillColor(WHITE); c.setFont('PopB',8.5); c._charSpace=0.5
            c.drawString(px+10,y-13,name.upper()); c._charSpace=0
            if price:
                c.setFillColor(AMBER); c.setFont('PopB',9)
                pric_w=c.stringWidth(price,'PopB',9)
                c.drawString(px+pw-pric_w-6,y-13,price)
            c.setFillColor(DK); c.setFont('PopMI',7.5)
            c.drawString(px+8,y-28,subtitle)
            c.setFillColor(SUB); c.setFont('Pop',7)
            words=items_str.split(); line=[]; lines=[]
            for w in words:
                test=' '.join(line+[w])
                if c.stringWidth(test,'Pop',7)<pw-14: line.append(w)
                else: lines.append(' '.join(line)); line=[w]
            if line: lines.append(' '.join(line))
            sy=y-40
            for ln in lines[:4]: c.drawString(px+8,sy,ln); sy-=9
        y-=pkg_h+8
    return y

def notes_box(c,y,title,lines):
    lh2=11; bh=14+len(lines)*lh2+6
    c.setFillColor(HexColor('#F5EFE4')); c.setStrokeColor(TAN); c.setLineWidth(0.4)
    c.roundRect(ML,y-bh,CW,bh,3,fill=1,stroke=1)
    c.setFillColor(AMBER); c.rect(ML,y-bh,4,bh,fill=1,stroke=0)
    c.setFillColor(TEAL); c.setFont('PopB',7.5); c._charSpace=1
    c.drawString(ML+12,y-11,title.upper()); c._charSpace=0
    ty=y-11-lh2
    for ln in lines:
        c.setFillColor(DK); c.setFont('Pop',7.5)
        c.drawString(ML+20,ty,f'–  {ln}'); ty-=lh2
    return y-bh-10

def contact_closer(c,y):
    bh=68
    c.setFillColor(TDARK); c.rect(ML,y-bh,CW,bh,fill=1,stroke=0)
    c.setFillColor(AMBER); c.rect(ML,y-3,CW,3,fill=1,stroke=0)
    c.rect(ML,y-bh,CW,3,fill=1,stroke=0); c.rect(ML,y-bh,4,bh,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('PopB',11); c._charSpace=2
    cta='LET US SERVE YOUR CITY'; ctw=c.stringWidth(cta,'PopB',11)
    c.drawString(ML+(CW-ctw)/2,y-20,cta); c._charSpace=0
    c.setFillColor(AMBER); c.setFont('PopM',8)
    ct='citizenscatering.com   •   (855) 227-3783   •   nakia@weserveyourcity.org'
    ccw=c.stringWidth(ct,'PopM',8); c.drawString(ML+(CW-ccw)/2,y-34,ct)
    c.setFillColor(MID); c.setFont('PopLI',6.5)
    note='Custom sizes, themed presentations & specialty dietary builds available. *Prices subject to change.'
    nw=c.stringWidth(note,'PopLI',6.5)
    if nw<CW-20: c.drawString(ML+(CW-nw)/2,y-46,note)
    return y-bh-10

class PM:
    def __init__(self,c_,sec_,version="v1.6"):
        self.c=c_; self.sec=sec_; self.version=version; self._new()
    def _new(self): phdr(self.c,self.sec); pftr(self.c,self.version); self.y=BT
    def need(self,pts=40):
        if self.y-pts<BB: self.c.showPage(); self._new()
    def s(self,title,sub=None,color=None): self.need(50); self.y=sh(self.c,self.y,title,sub,color)
    def i(self,text): self.need(30); self.y=intr(self.c,self.y,text)
    def k(self,title,color=None): self.need(28); self.y=cat(self.c,self.y,title,color)
    def two(self,left,right,rowbg=None,namecolor=None):
        while left or right:
            self.need(40)
            self.y,left,right=twocol(self.c,self.y,left,right,BB,rowbg,namecolor)
    def board(self,name,tier,price,serves,includes,note='',accent=None):
        h=18+len(includes)*11+(14 if note else 0)+24; self.need(h)
        self.y=board_card(self.c,self.y,name,tier,price,serves,includes,note,accent)
    def pkgs(self,packages,accent=None):
        pkg_h=72; rows=(len(packages)+1)//2; self.need(rows*(pkg_h+8)+20)
        self.y=pkg_grid(self.c,self.y,packages,BB,accent)
    def notes(self,title,lines):
        self.need(len(lines)*11+30); self.y=notes_box(self.c,self.y,title,lines)
    def closer(self): self.need(80); self.y=contact_closer(self.c,self.y)
    def gap(self,pts=12): self.y-=pts

# ══════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════

def build(path, version="v1.6"):
    c=canvas.Canvas(path,pagesize=letter)
    c.setTitle(f"Citizens Catering — Charcuterie & Grazing Spreads {version}")

    cover(c, version=version); c.showPage()

    # ── PAGE 2: Charcuterie Boards ─────────────────────────────
    pm=PM(c,'CHARCUTERIE BOARDS', version=version)
    pm.s('CHARCUTERIE BOARDS','Chef-curated · Professionally presented')
    pm.i('All charcuterie boards are professionally arranged and refreshed throughout service. Boards, tiers, and risers available with rental service fee. Minimum guest counts and order quantities apply.')
    pm.gap(8)
    pm.board('Standard Charcuterie Board','— Classic Presentation','$XX','Serves XX guests',
        ['3 artisan cheese varieties (cheddar, brie, gouda or seasonal selection)',
         '3 cured meat varieties (salami, peppered salami, prosciutto)',
         '3 seasonal fruit selections (grapes, berries, sliced seasonal fruit)',
         'Fresh seasonal vegetables and crudite accompaniments',
         'Dips & spreads: Dijon mustard, local honey, fig jam',
         'Assorted artisan crackers and sliced bread',
         'Toasted nuts and dried fruits',
         'Standard flat lay board presentation'],
        'Boards, tiers, and risers available with rental service fee.')
    pm.board('Premium Charcuterie Board','— Elevated Presentation','$XX','Serves XX guests',
        ['3 premium artisan cheese varieties (aged cheddar, double cream brie, manchego)',
         '3 premium cured meat varieties (prosciutto, soppressata, peppered salami)',
         '3 seasonal fruit selections with edible garnishes',
         'Loaded hummus with seasonal toppings and fresh vegetables',
         'Premium spreads: truffle honey, spiced fig jam, whole grain Dijon',
         'Assorted artisan crackers, sourdough and artisan bread',
         'Toasted nuts, dried fruits, cornichons and Castelvetrano olives',
         'Multi-level presentation with risers and styled boards'],
        'Premium presentation including tiered towers, seasonal floral garnish, and custom labeling available.')
    pm.board('Charcuterie Favor Cups','— Individual Portable Portions','$XX each','Per guest',
        ['Fresh strawberries, blackberries and red grapes',
         'Salami, brie bites, Gouda and Manchego',
         'Breadsticks and rustic flatbreads',
         'Honey stick, cornichons and olives',
         'Dried apricots and toasted nuts',
         'Topped with fresh rosemary sprig — individually packaged'],
        'Perfect for cocktail hours, wedding favors, corporate gifting, and place settings.')
    c.showPage()

    # ── PAGE 3: Savory Grazing Boards ─────────────────────────
    pm=PM(c,'SAVORY GRAZING BOARDS', version=version)
    pm.s('SAVORY GRAZING BOARDS','Complete curated spreads with a distinct culinary identity')
    pm.i('Each savory grazing board is a fully curated spread with a cohesive flavor story. Available in small (serves 15-20), standard (serves 30-40), and large (serves 60+).')
    pm.gap(4); pm.k('Boards & Display Spreads')
    pm.two([
        ('Artisan Cheese Board','Chef-curated artisan cheeses — Stilton bleu, sharp cheddar, double cream brie, manchego. Local honey, Dijon, nuts, dried fruits, artisan crackers.','GF'),
        ('Mediterranean Mezze Board','House hummus, baba ganoush, dolmas, warm pita, kalamata olives, roasted red peppers, marinated artichokes, feta crumbles, tzatziki.','Vegan'),
        ('Antipasto Board','Marinated vegetables, cured meats, fresh mozzarella, olives, roasted peppers, artichoke hearts, sun-dried tomatoes, artisan crackers.','GF · Veg'),
        ('Southern Grazing Board','Deviled eggs, house pimento cheese, house pickles, cornbread poppers, smoked meats, cornichons, honey butter, crackers.',''),
        ('Texas BBQ Spread','Sliced smoked brisket, pulled chicken, deviled eggs, pimento cheese celery boats, cornbread bites, house pickles, BBQ spiced nuts, honey butter.',''),
    ],[
        ('Tex-Mex Grazing Board','House guacamole, fresh pico de gallo, queso fundido, tortilla chips, jalapeno poppers, mini empanadas, elote cups, cowboy caviar.','GF · Vegan'),
        ('Smoked Salmon Display','Herb-roasted whole salmon, NY-style crackers, whipped cream cheese, capers, dill, sliced red onion, lemon wedges, pickled cucumber.','GF'),
        ('Seasonal Crudite Platter','Farmer\'s market cut vegetables — rainbow carrots, cucumber, radishes, snap peas, cherry tomatoes. House ranch, hummus, green goddess.','GF · Vegan'),
        ('Fruit & Nut Display','Seasonal fresh fruit, premium mixed nuts, local honey, fresh mint, honeycomb.','GF · Vegan · DF'),
        ('Seafood Display Board','Gulf shrimp cocktail, smoked salmon rounds, mini crab cakes, blackened shrimp avocado bites. House cocktail sauce, remoulade, dill cream cheese.','GF'),
    ])
    pm.gap(10); pm.k('Specialty Savory Boards')
    pm.two([
        ('Build Your Own Bruschetta Station','Toasted crostini, oven-dried tomato, whipped ricotta, fresh basil, olive tapenade, roasted garlic, EVOO, honey, micro herbs.','Vegan'),
        ('Dips & Spreads Station','Chips & guacamole, loaded hummus, spinach & artichoke dip, pimento cheese, house ranch. Tortilla chips, pita, artisan bread.','Veg'),
        ('BBQ Sundae Bar','Individual cups layered with pulled chicken or brisket over mashed potatoes or mac & cheese. House BBQ sauces, pickled jalapenos, cheddar, scallions.',''),
    ],[
        ('Bread & Dip Station','Selection of artisan breads and focaccia. House hummus, olive tapenade, roasted garlic EVOO, whipped ricotta, caponata.','Vegan'),
        ('Mini Cheese Ball Display','Individual cheese ball bites — dried fruit & herbs, BBQ spiced nuts, everything seasoning coatings. Pretzel crackers and breadsticks.','Veg'),
        ('Loaded Charcuterie Tablescape','Full-table styled spread combining premium charcuterie, fresh flowers, seasonal produce, candles, and styled props. Full kitchen and design build.',''),
    ])
    c.showPage()

    # ── PAGE 4: Dessert & Sweet Grazing ───────────────────────
    pm=PM(c,'DESSERT & SWEET GRAZING', version=version)
    pm.s('DESSERT & SWEET GRAZING BOARDS','House-made · Indulgent · Beautifully presented',RED)
    pm.i('Our dessert grazing boards are thoughtfully composed with a mix of baked desserts, fresh fruit, dips, and sweet accompaniments. Available in Standard and Premium tiers. Dessert selections listed are our most popular — additional options and fully custom boards are available upon request.')
    pm.gap(8)

    pm.board('Standard Dessert Grazing Board','— Classic Sweet Spread','$XX','Serves XX guests',
        ['3 desserts of your choice — brownies, blondies, mini cookies, mini cheesecake bites, lemon bars, macarons, chocolate croissants, butter croissants, donut holes, mini muffins, or cinnamon roll bites. Additional seasonal options available.',
         '2 fruits of your choice — strawberries, blueberries, or grapes. Additional seasonal options available.',
         '1 dip or spread: whipped cream cheese with honey, chocolate fondue sauce, or caramel dip',
         'Sweet accompaniments: dried fruits, toasted nuts, dark chocolate bites, and candy-coated pieces',
         'Artisan crackers, wafer cookies, and pretzel dippers',
         'Standard flat lay board presentation'],
        'Three desserts, two fruits, one dip — the foundation of every great dessert spread.',
        accent=RED)

    pm.board('Premium Dessert Grazing Board','— Elevated Sweet Experience','$XX','Serves XX guests',
        ['5 desserts of your choice — brownies, blondies, mini cookies, mini cheesecake bites, lemon bars, macarons, chocolate croissants, butter croissants, donut holes, mini muffins, cinnamon roll bites, chocolate-dipped strawberries, candied pecan clusters, and more. Additional seasonal options available.',
         '3 seasonal fruits: styled fruit display with grapes, berries, and citrus',
         '2 dips & spreads: whipped cream cheese with honey and zest + chocolate fondue or caramel dip',
         'Premium sweet accompaniments: honeycomb, dried apricots, candied pecans, dark chocolate bark, and gourmet confections',
         'Artisan wafers, pirouette cookies, pretzel dippers, and biscotti',
         'Multi-level presentation with risers, styled vessels, and edible florals',
         'Chocolate drizzle finish and custom labeling available'],
        'Five desserts, three fruits, two dips — the full sweet experience, styled for visual impact.',
        accent=RED)

    pm.gap(14)
    pm.s('SPECIALTY DESSERT BOARDS','Themed builds for a distinct sweet identity',TEAL)
    pm.i('Each specialty dessert board is built around a single flavor theme for events where the dessert table is a centerpiece.')
    pm.gap(8)

    pm.board('Fruit & Sweet Grazing Board','— Fresh & Bright','$XX','Serves XX guests',
        ['Seasonal fresh fruit display — grapes, berries, citrus',
         'Chocolate-dipped strawberries and fresh berry clusters',
         'Honeycomb and local Hive honey for drizzling',
         'Lemon bars with powdered sugar finish and mini fruit tarts with pastry cream',
         'Coconut macaroons and sugar cookies',
         'Whipped cream cheese dip with honey and fresh zest',
         'Candied citrus peel and dried fruit medley'],
        'Light and fruit-forward — ideal for daytime events, showers, and brunches.',
        accent=AMBER)
    c.showPage()

    # ── PAGE 5: Add a Bar ─────────────────────────────────────
    pm=PM(c,'ADD A BAR', version=version)
    pm.s('ADD A BAR TO YOUR ORDER','Interactive builds · Staffed or self-serve · Fully customizable')
    pm.i('Complement any grazing or charcuterie board with one of our interactive bar stations. The options below represent our most popular selections — additional bars and custom concepts are available. Ask us about anything not listed.')
    pm.gap(10)
    pm.k('Available Bars')
    pm.two([
        ('Candy Bar',
         'Assorted bulk candies, premium chocolates, and nostalgic favorites. Styled with decorative jars, risers, and scoops. Custom labels and themed color palettes available.',
         'Sugar-free avail.'),
        ('Popcorn Bar',
         'Fresh-popped popcorn in multiple house seasonings. Scooped into branded bags or boxes.',
         'GF · Vegan avail.'),
        ('Trail Mix Bar',
         'Base grains, nuts, and seeds with a full add-in station. Sweetener drizzles, dried fruits, and chocolate options. Packaged to go.',
         'GF · Vegan avail.'),
    ],[
        ('Avocado Toast Bar',
         'Artisan bread base with house-smashed avocado and a full toppings station. Great for brunch and wellness events.',
         'Vegan avail.'),
        ('BBQ Sundae Bar',
         'Individual sundae cups layered with pulled chicken or brisket, mashed potatoes or mac & cheese, and house BBQ sauces.',
         ''),
        ('Snack & Wellness Bar',
         'Jerky, protein balls, protein bars, fruit skewers, smoked nuts, decaf matcha bites, fancy smoked salts, and dark chocolate.',
         'GF · Vegan avail.'),
    ])
    pm.gap(14)
    pm.notes('Bar Service Notes',[
        'All bars available staffed or self-serve — staffed service recommended for events over 75 guests',
        'Bars can be added to any board or package order',
        'Custom theming, color palettes, branded signage, and packaging available for all bars',
        'Sugar-free, allergen-friendly, and dietary-specific builds available upon request',
        'Additional bar options and fully custom concepts available — ask us if you don\'t see what you\'re looking for',
        'Full bar details and customization options available in our Interactive Stations menu',
        'Contact us for per-person and per-display pricing',
    ])
    c.showPage()

    # ── PAGE 6: Themed Packages ────────────────────────────────
    pm=PM(c,'THEMED PACKAGES', version=version)
    pm.s('THEMED GRAZING PACKAGES','Curated multi-element packages for complete event experiences')
    pm.i('Themed packages combine savory boards, sweet boards, and specialty items into a cohesive food experience. All packages customizable — contact us for a tailored quote.')
    pm.gap(10)
    pm.pkgs([
        ('Mediterranean Mezze','A journey through the Mediterranean',
         'House hummus, baba ganoush, dolmas, pita, kalamata olives, roasted peppers, feta, tzatziki, spanakopita bites, caprese skewers','$XX pp'),
        ('Taste of Texas','Southern & Texas flavors done right',
         'Smoked brisket crostini, deviled eggs, pimento cheese, cornbread poppers, bacon-wrapped dates, BBQ spiced nuts, house pickles, jalapeño poppers','$XX pp'),
        ('Healthy Grazing','Fresh, wholesome, plant-forward spread',
         'Seasonal crudite, loaded hummus, fresh fruit display, whole grain crackers, nut & seed mix, Mediterranean skewers, roasted veggie display','$XX pp'),
        ('Global Street Food Tour','Four cuisines, one unforgettable table',
         'Guacamole bites, Vietnamese summer rolls, spanakopita, deviled eggs, street corn cups, mini empanadas, Mediterranean chicken skewers','$XX pp'),
        ('Sweet & Savory Experience','The best of both worlds on one table',
         'Standard charcuterie board + dessert grazing board + seasonal fruit display + candy bar selections. Full sweet-to-savory journey.','$XX pp'),
        ('Build Your Own Bar','Guests craft their own perfect plate',
         'Choice of any 5 items from our full grazing & charcuterie menu. Boards, tongs, and plates provided. Staffed service available.','$XX pp'),
    ])
    pm.gap(14)
    pm.notes('Service & Ordering Notes',[
        'Savory boards available in Small (serves 15-20), Standard (serves 30-40), and Large (serves 60+)',
        'Dessert and sweet boards sized to match your savory order or ordered independently',
        'Candy bar and snack boards priced per person or per display — contact us for details',
        'Charcuterie Favor Cups priced individually — minimum order quantities apply',
        'All boards professionally arranged and refreshed throughout service',
        'Boards, tiers, risers, and vessels available with rental service fee',
        'Custom dietary builds (GF, vegan, dairy-free, sugar-free) available across all offerings',
        'Custom labeling, signage, and themed presentation available for all boards',
        '*Prices subject to change without prior notice',
    ])
    pm.gap(10); pm.closer()

    c.save(); print(f'Saved: {path}')


if __name__ == '__main__':
    out = os.path.join(SCRIPT_DIR, 'Citizens_Charcuterie_v1.6.pdf')
    build(out, version="v1.6")
    print('Done.')
