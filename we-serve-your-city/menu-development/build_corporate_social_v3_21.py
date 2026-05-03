#!/usr/bin/env python3
"""
Citizens Catering — Professional PDF Menu Generator
v3.21 — Corporate & Social Menu

Edits from v3.20:
   7. Sides — Southern: removed Candied Yams; added Brussels Sprouts & Bacon
   8. Salads: added Greek Salad
   9. Stations: "Avocado Bar" renamed to "Custom Guacamole Bar";
      habanero crema removed from description
  10. Stations: Pesto added to Interactive Pasta Bar
  11. Stations: BBQ Sundae Bar — mashed potatoes removed as a base option
  12. Stations: Breakfast Taco Station removed entirely
  13. Desserts: Assorted Cookie Platter — removed snickerdoodle and sugar,
      added white chocolate macadamia nut
  14. Desserts: Chocolate Covered Strawberries removed entirely
  15. Desserts: Bourbon sauce removed from Bread Pudding

Edits from v3.19 (carried over from v3.20):
   6. Page numbers added to interior page footers (cover unnumbered).

Edits from v3.18 (carried over from v3.19):
   1. Caprese Skewers: "EVOO" -> "balsamic glaze"
   2. Beef empanadas: drop "Mini" prefix on the two beef-section empanadas
   3. Charcuterie & Display Options: Custom Grazing Spreads moved to left column
   4. Turkey Meatloaf: "Classic glazed, mushroom gravy" -> "Classic glazed"
   5. SEAFOOD subsection header: keep with content (no orphan at bottom of page)
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import io, os

# ── REGISTER FONTS ────────────────────────────────────────────
BASE = '/usr/share/fonts/truetype/google-fonts'
pdfmetrics.registerFont(TTFont('Poppins',        f'{BASE}/Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Bold',   f'{BASE}/Poppins-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Medium', f'{BASE}/Poppins-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Light',  f'{BASE}/Poppins-Light.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Italic', f'{BASE}/Poppins-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-MedItal',f'{BASE}/Poppins-MediumItalic.ttf'))

# ── BRAND PALETTE ─────────────────────────────────────────────
TEAL    = HexColor('#00333D')
AMBER   = HexColor('#D4832A')
RED     = HexColor('#B83227')
CREAM   = HexColor('#FAF8F5')
LTGRAY  = HexColor('#F2F0ED')
MDGRAY  = HexColor('#D8D4CF')
DKGRAY  = HexColor('#4A4540')
SUBTXT  = HexColor('#8A8480')
WHITE   = white

# ── PAGE GEOMETRY ─────────────────────────────────────────────
W, H    = letter
ML      = 0.65 * inch
MR      = 0.65 * inch
MT      = 0.6  * inch
MB      = 0.55 * inch
CW      = W - ML - MR
COL     = (CW - 18) / 2
GUTTER  = 18

HDR_H   = 44
FTR_H   = 22
BODY_T  = H - HDR_H - MT
BODY_B  = MB + FTR_H + 8

# ── LOAD LOGOS ────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SCRIPT_DIR, 'assets')
LOGO_WHITE = ImageReader(os.path.join(ASSETS, 'logo_white.png'))
LOGO_TEAL  = ImageReader(os.path.join(ASSETS, 'CITIZENS_LOGO_NAVY.png'))

# Logo aspect ratio — measured from CITIZENS_LOGO_NAVY.png (1313 x 714)
LOGO_RATIO = 1313 / 714

def logo_w_to_h(w): return w / LOGO_RATIO
def logo_h_to_w(h): return h * LOGO_RATIO


# ══════════════════════════════════════════════════════════════
# SHARED PAGE ELEMENTS
# ══════════════════════════════════════════════════════════════

def draw_cover(c, menu_title, subtitle="", version="v3.18"):
    c.setFillColor(TEAL)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(AMBER)
    c.rect(0, H - 8, W, 8, fill=1, stroke=0)
    c.rect(0, 0, W, 8, fill=1, stroke=0)

    c.saveState()
    c.setStrokeColor(AMBER)
    c.setLineWidth(0.5)
    inset = 28
    c.rect(inset, inset, W - 2*inset, H - 2*inset, fill=0, stroke=1)
    c.restoreState()

    lw = 3.2 * inch
    lh = logo_w_to_h(lw)
    lx = (W - lw) / 2
    ly = H * 0.52
    c.drawImage(LOGO_WHITE, lx, ly, width=lw, height=lh, mask='auto')

    c.setFillColor(AMBER)
    c.setFont('Poppins-Medium', 9)
    tag = "CATERING"
    tw = c.stringWidth(tag, 'Poppins-Medium', 9)
    c.drawString((W - tw) / 2, ly + lh + 18, tag)

    rule_y = ly + lh + 14
    c.setStrokeColor(AMBER)
    c.setLineWidth(0.75)
    c.line(W/2 - 36, rule_y, W/2 + 36, rule_y)

    c.setFillColor(WHITE)
    c.setFont('Poppins-Bold', 22)
    tw = c.stringWidth(menu_title, 'Poppins-Bold', 22)
    c.drawString((W - tw) / 2, ly - 36, menu_title)

    if subtitle:
        c.setFillColor(HexColor('#C8B89A'))
        c.setFont('Poppins-Light', 9.5)
        sw = c.stringWidth(subtitle, 'Poppins-Light', 9.5)
        c.drawString((W - sw) / 2, ly - 56, subtitle)

    c.setStrokeColor(AMBER)
    c.setLineWidth(1.5)
    c.line(W/2 - 60, ly - 68, W/2 + 60, ly - 68)

    cb_y = 0.65 * inch
    c.setFillColor(HexColor('#C8B89A'))
    c.setFont('Poppins-Light', 8)
    contact = "citizenscatering.com   •   (855) 227-3783   •   nakia@weserveyourcity.org"
    cw = c.stringWidth(contact, 'Poppins-Light', 8)
    c.drawString((W - cw) / 2, cb_y, contact)

    c.setFillColor(HexColor('#4A6068'))
    c.setFont('Poppins-Light', 6.5)
    ver = f"{version}  •  2026"
    vw = c.stringWidth(ver, 'Poppins-Light', 6.5)
    c.drawString((W - vw) / 2, cb_y - 14, ver)

    c.setFillColor(AMBER)
    c.rect(0, 0, W, 4, fill=1, stroke=0)


def draw_page_header(c, section_name):
    c.setFillColor(TEAL)
    c.rect(0, H - HDR_H, W, HDR_H, fill=1, stroke=0)

    c.setFillColor(AMBER)
    c.rect(0, H - 3, W, 3, fill=1, stroke=0)

    lw = 1.05 * inch
    lh = logo_w_to_h(lw)
    c.drawImage(LOGO_WHITE, ML, H - HDR_H + (HDR_H - lh) / 2,
                width=lw, height=lh, mask='auto')

    c.setFillColor(HexColor('#C8B89A'))
    c.setFont('Poppins-Medium', 8)
    snw = c.stringWidth(section_name, 'Poppins-Medium', 8)
    c.drawString(W - MR - snw, H - HDR_H + (HDR_H - 8) / 2, section_name)

    c.setStrokeColor(AMBER)
    c.setLineWidth(1)
    c.line(0, H - HDR_H - 1, W, H - HDR_H - 1)


def draw_page_footer(c, version="v3.18", page_num=None):
    fy = MB + FTR_H - 4
    c.setStrokeColor(AMBER)
    c.setLineWidth(0.75)
    c.line(ML, fy, W - MR, fy)

    c.setFillColor(SUBTXT)
    c.setFont('Poppins-Medium', 6.5)
    c.drawString(ML, fy - 10, "CITIZENS CATERING")

    c.setFont('Poppins', 6.5)
    contact = "citizenscatering.com   |   (855) 227-3783   |   nakia@weserveyourcity.org"
    cw = c.stringWidth(contact, 'Poppins', 6.5)
    c.drawString((W - cw) / 2, fy - 10, contact)

    c.setFont('Poppins-Light', 6.5)
    right_text = f"{version}   |   Page {page_num}" if page_num is not None else version
    vw = c.stringWidth(right_text, 'Poppins-Light', 6.5)
    c.drawString(W - MR - vw, fy - 10, right_text)


# ══════════════════════════════════════════════════════════════
# CONTENT DRAWING PRIMITIVES
# ══════════════════════════════════════════════════════════════

def section_header(c, y, title):
    bar_h = 26
    c.setFillColor(AMBER)
    c.rect(ML, y - bar_h, 4, bar_h, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(ML + 4, y - bar_h, CW - 4, bar_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Poppins-Bold', 11)
    c.drawString(ML + 14, y - bar_h + 8, title.upper())
    return y - bar_h - 8


def section_intro(c, y, text):
    c.setFillColor(SUBTXT)
    c.setFont('Poppins-Italic', 7.5)
    words = text.split()
    line, lines = [], []
    for w in words:
        test = ' '.join(line + [w])
        if c.stringWidth(test, 'Poppins-Italic', 7.5) < CW:
            line.append(w)
        else:
            lines.append(' '.join(line))
            line = [w]
    if line:
        lines.append(' '.join(line))
    for ln in lines:
        c.drawString(ML, y, ln)
        y -= 10
    y -= 4
    c.setStrokeColor(MDGRAY)
    c.setLineWidth(0.4)
    c.line(ML, y, W - MR, y)
    return y - 8


def category_header(c, y, title):
    c.setFillColor(TEAL)
    c.setFont('Poppins-Bold', 7.5)
    c.drawString(ML, y, title.upper())
    c.setStrokeColor(AMBER)
    c.setLineWidth(0.75)
    c.line(ML, y - 3, W - MR, y - 3)
    return y - 13


def draw_item(c, x, y, col_w, name, desc="", tags=""):
    tag_list = [t.strip() for t in tags.split('·')] if tags else []
    name_w = c.stringWidth(name, 'Poppins-Medium', 8.5)

    c.setFillColor(TEAL)
    c.setFont('Poppins-Medium', 8.5)
    c.drawString(x, y, name)
    nx = x + name_w

    tag_x = nx + 5
    for tag in tag_list:
        if not tag:
            continue
        tw = c.stringWidth(tag, 'Poppins-Bold', 5.5) + 6
        c.setFillColor(HexColor('#FAF0EE'))
        c.setStrokeColor(RED)
        c.setLineWidth(0.4)
        c.roundRect(tag_x, y - 1.5, tw, 9, 1.5, fill=1, stroke=1)
        c.setFillColor(RED)
        c.setFont('Poppins-Bold', 5.5)
        c.drawString(tag_x + 3, y + 0.5, tag)
        tag_x += tw + 3

    if desc:
        c.setFillColor(DKGRAY)
        c.setFont('Poppins-Italic', 7.5)
        words = desc.split()
        line, lines = [], []
        for w in words:
            test = ' '.join(line + [w])
            if c.stringWidth(test, 'Poppins-Italic', 7.5) < col_w - 2:
                line.append(w)
            else:
                lines.append(' '.join(line))
                line = [w]
        if line:
            lines.append(' '.join(line))
        dy = y - 10
        for ln in lines:
            c.drawString(x, dy, ln)
            dy -= 9

        total_h = 11 + len(lines) * 9 + 5
        rule_y = y - total_h + 4
        c.setStrokeColor(HexColor('#EAE6E2'))
        c.setLineWidth(0.3)
        c.line(x, rule_y, x + col_w, rule_y)
        return total_h
    else:
        c.setStrokeColor(HexColor('#EAE6E2'))
        c.setLineWidth(0.3)
        c.line(x, y - 8, x + col_w, y - 8)
        return 14


def two_col_items(c, y, left_items, right_items, bottom_limit, row_index_start=0):
    lx = ML
    rx = ML + COL + GUTTER

    PAD_TOP = 7
    PAD_BOT = 5

    li, ri = 0, 0
    row_idx = row_index_start
    while li < len(left_items) or ri < len(right_items):
        lh = rh = 0
        l_lines = r_lines = 0
        if li < len(left_items):
            n, d, t = left_items[li]
            lh = estimate_item_h(c, COL, n, d)
            l_lines = _count_desc_lines(c, COL, d) if d else 0
        if ri < len(right_items):
            n, d, t = right_items[ri]
            rh = estimate_item_h(c, COL, n, d)
            r_lines = _count_desc_lines(c, COL, d) if d else 0
        row_h = max(lh, rh)
        max_lines = max(l_lines, r_lines)

        if y - row_h < bottom_limit:
            return y, li, ri

        if max_lines > 0:
            last_baseline = y - 10 - (max_lines - 1) * 9
            text_bottom = last_baseline - 2
        else:
            text_bottom = y - 8
        panel_top = y + PAD_TOP
        panel_bottom = text_bottom - PAD_BOT
        panel_h = panel_top - panel_bottom

        if row_idx % 2 == 0:
            c.setFillColor(LTGRAY)
            c.rect(ML, panel_bottom, CW, panel_h, fill=1, stroke=0)

        if li < len(left_items):
            n, d, t = left_items[li]
            draw_item(c, lx, y, COL, n, d, t)
            li += 1
        if ri < len(right_items):
            n, d, t = right_items[ri]
            draw_item(c, rx, y, COL, n, d, t)
            ri += 1

        y -= row_h
        row_idx += 1

    return y, li, ri


def _count_desc_lines(c, col_w, desc):
    if not desc:
        return 0
    words = desc.split()
    line, lines = [], []
    for w in words:
        test = ' '.join(line + [w])
        if c.stringWidth(test, 'Poppins-Italic', 7.5) < col_w - 2:
            line.append(w)
        else:
            lines.append(' '.join(line))
            line = [w]
    if line:
        lines.append(' '.join(line))
    return len(lines)


def estimate_item_h(c, col_w, name, desc):
    if not desc:
        return 16
    words = desc.split()
    line, lines = [], []
    for w in words:
        test = ' '.join(line + [w])
        if c.stringWidth(test, 'Poppins-Italic', 7.5) < col_w - 2:
            line.append(w)
        else:
            lines.append(' '.join(line))
            line = [w]
    if line:
        lines.append(' '.join(line))
    return 11 + len(lines) * 9 + 7


def package_card(c, y, title, includes):
    row_h = 14
    pad_v = 10
    hdr_h = 24
    n_rows = (len(includes) + 1) // 2
    body_h = pad_v + n_rows * row_h + pad_v
    total_h = hdr_h + body_h

    c.setFillColor(TEAL)
    c.roundRect(ML, y - hdr_h, CW, hdr_h, 3, fill=1, stroke=0)
    c.setFillColor(AMBER)
    c.rect(ML, y - hdr_h, 4, hdr_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Poppins-Bold', 9.5)
    c.drawString(ML + 14, y - hdr_h + 8, title)

    c.setFillColor(HexColor('#F7F5F2'))
    c.setStrokeColor(MDGRAY)
    c.setLineWidth(0.4)
    c.roundRect(ML, y - total_h, CW, body_h, 3, fill=1, stroke=1)

    half = (len(includes) + 1) // 2
    ly = y - hdr_h - pad_v - 2
    for i, inc in enumerate(includes):
        col_x = ML + 14 if i < half else ML + CW/2 + 8
        row_i = i if i < half else i - half
        iy = ly - row_i * row_h
        c.setFillColor(AMBER)
        c.setFont('Poppins-Bold', 7)
        c.drawString(col_x, iy, '✓')
        c.setFillColor(DKGRAY)
        c.setFont('Poppins', 7.5)
        c.drawString(col_x + 10, iy, inc)

    return y - total_h - 12


def contact_closer(c, y, cta="LET US SERVE YOUR CITY",
                   note="Vegetarian & vegan menus available. All dietary accommodations honored. *Prices subject to change."):
    block_h = 76
    if y - block_h < BODY_B - 10:
        return y

    c.setFillColor(TEAL)
    c.rect(ML, y - block_h, CW, block_h, fill=1, stroke=0)
    c.setFillColor(AMBER)
    c.rect(ML, y - 3, CW, 3, fill=1, stroke=0)
    c.rect(ML, y - block_h, CW, 3, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('Poppins-Bold', 12)
    cw = c.stringWidth(cta, 'Poppins-Bold', 12)
    c.drawString(ML + (CW - cw) / 2, y - 22, cta)

    c.setFillColor(AMBER)
    c.setFont('Poppins-Medium', 8.5)
    contact = "citizenscatering.com   •   (855) 227-3783   •   nakia@weserveyourcity.org"
    tw = c.stringWidth(contact, 'Poppins-Medium', 8.5)
    c.drawString(ML + (CW - tw) / 2, y - 38, contact)

    c.setFillColor(HexColor('#7AABB5'))
    c.setFont('Poppins-Italic', 6.5)
    nw = c.stringWidth(note, 'Poppins-Italic', 6.5)
    c.drawString(ML + (CW - nw) / 2, y - 52, note)

    return y - block_h - 10


# ══════════════════════════════════════════════════════════════
# MENU DATA — v3.18 baseline
# ══════════════════════════════════════════════════════════════

HORS_VEG = [
    ("Caprese Skewers", "Fresh mozzarella, grape tomato, basil, balsamic glaze", "GF"),
    ("Bruschetta Crostini", "Oven-dried tomato, garlic, white balsamic, micro basil", "Vegan"),
    ("Spanakopita", "Spinach, Greek feta, phyllo pastry", "Veg"),
    ("Stuffed Mini Bell Peppers", "Quinoa, roasted corn, fresh herbs, cotija", "GF · Vegan"),
    ("Whipped Feta Crostini", "Local honey drizzle, fresh herbs, crostini", "Veg"),
    ("Falafel Bites", "House tahini sauce, micro greens", "Vegan · GF"),
]
HORS_VEG_R = [
    ("Street Corn Cups", "Roasted corn, cotija, chili-lime crema", "GF · Veg"),
    ("Patatas Bravas", "Crispy baby potato, smoked tomato aioli", "GF · Vegan"),
    ("Guacamole Bites", "Crispy tortilla cups, fresh pico, lime", "GF · Vegan"),
    ("Watermelon & Feta Skewers", "Mint oil, cracked black pepper", "GF · Veg"),
    ("Whipped Ricotta & Roasted Berries Crostini", "House whipped ricotta, roasted seasonal berries, honey drizzle, fresh thyme", "Veg"),
]
HORS_SEAFOOD_L = [
    ("Shrimp Cocktail Cups", "Gulf shrimp, house cocktail sauce, lemon", "GF · DF"),
    ("Gulf Shrimp Skewers", "Chili-lime butter, scallion", "GF · DF"),
    ("Mini Crab Cakes", "Old bay aioli, chervil garnish", "DF"),
    ("Smoked Salmon Cucumber Rounds", "Cream cheese, capers, dill", "GF"),
]
HORS_SEAFOOD_R = [
    ("Blackened Shrimp Avocado Bites", "Cucumber round, chipotle crema", "GF"),
    ("Smoked Salmon Puff Pastry Squares", "Cream cheese, fresh herbs", ""),
    ("Bacon-Wrapped Shrimp", "Honey chipotle glaze", "GF · DF"),
]
HORS_POULTRY_L = [
    ("Mini Chicken & Waffles", "Sriracha maple syrup, powdered sugar", ""),
    ("Mediterranean Chicken Skewers", "Lemon herb marinade, tzatziki", "GF · DF"),
    ("Mole Chicken Skewers", "House mole sauce, sesame seeds", "GF · DF"),
    ("Fajita Chicken Empanadas", "Caramelized peppers & onions, salsa roja", "DF"),
]
HORS_POULTRY_R = [
    ("Thai Chicken Salad Wonton Cups", "Mango chutney, toasted almonds, micro greens", ""),
    ("BBQ Chicken Flatbread Bites", "Smoked BBQ sauce, red onion, cilantro", ""),
    ("Smoked Chicken Sliders", "Brioche rolls, coleslaw, house pickles", "DF"),
    ("Chicken Skewers", "Honey garlic glaze, sesame, scallion", "GF · DF"),
]
HORS_BEEF_L = [
    ("Smoked Brisket Crostini", "Horseradish cream, pickled red onion", "DF"),
    ("Beef Picadillo Empanadas", "Seasoned ground beef, olives, raisins", "DF"),
    ("All-Beef Cocktail Meatballs", "House sweet heat glaze, toasted sesame, scallion", "DF"),
    ("Beef Empanadas with Chimichurri", "Slow-cooked beef, golden pastry, chimichurri", "DF"),
]
HORS_BEEF_R = [
    ("Ribeye Steak Crostini", "Horseradish aioli, shaved radish", "DF"),
    ("BBQ Beef Empanadas", "Smoked beef, caramelized onion, salsa roja", "DF"),
    ("Birria Taco Bites", "Braised beef, consomme, cilantro, white onion", "GF · DF"),
    ("Beef Meatballs", "House tomato basil sauce, shaved parmesan", ""),
]
CHARCUTERIE = [
    ("Standard Charcuterie Board", "Curated meats, artisan cheeses, pickles, honey, crackers & bread", ""),
    ("Premium Charcuterie Board", "Elevated cured meats, artisan cheeses, fig jam, seasonal fruit, artisan bread", ""),
    ("Mediterranean Mezze Display", "Hummus, olives, dolmas, warm pita, roasted peppers", "Vegan"),
    ("Antipasto Board", "Marinated vegetables, cured meats, fresh mozzarella, olives", "GF · Veg"),
    ("Custom Grazing Spreads", "Savory and sweet grazing displays — see our Charcuterie & Grazing Spreads menu for full options", ""),
]

SIG_POULTRY_L = [
    ("Chicken Piccata", "Pan-seared chicken breast, lemon caper beurre blanc", ""),
    ("Chicken Marsala", "Mushroom & pearl onion Marsala wine sauce", "DF"),
    ("Smothered Chicken", "Southern-style mushroom & onion gravy", "GF"),
    ("BBQ Smoked Pulled Chicken", "Slow-smoked, house BBQ sauce", "GF · DF"),
    ("Honey Balsamic Glazed Chicken", "Grilled thigh, red pepper relish", "GF · DF"),
    ("Lemon Rosemary Chicken", "Pan-seared thigh, fresh rosemary bruschetta", "GF · DF"),
    ("Chicken Fettuccine Alfredo", "House fettuccine, scratch-made alfredo, grilled chicken breast, parmesan, fresh parsley", ""),
    ("Chicken Pesto Pasta", "House basil pesto, grilled chicken, cherry tomatoes, fettuccine, shaved parmesan", ""),
]
SIG_POULTRY_R = [
    ("Southern Oven-Roasted Chicken", "Herb seasoned, pan drippings jus", "GF · DF"),
    ("Honey Glazed Chicken Thighs", "Brown sugar honey glaze, fresh herbs", "GF · DF"),
    ("Cilantro Cream Chicken", "Roasted chicken thigh, cilantro cream sauce", "GF"),
    ("Chicken Tinga", "Braised shredded chicken, chipotle tomato sauce", "GF · DF"),
    ("Chicken Enchiladas", "Tomatillo cream sauce, Monterey Jack", ""),
    ("Turkey Meatloaf", "Classic glazed", "DF"),
]
SIG_BEEF_L = [
    ("Beef Tips & Gravy", "Braised beef tips, rich onion gravy, fresh herbs", "GF · DF"),
    ("Beef Barbacoa", "Slow-braised, ancho chiles, lime", "GF · DF"),
    ("Beef Lasagna", "House tomato basil & bechamel, ricotta, mozzarella, parmesan, slow-cooked beef", ""),
    ("Grilled Skirt Steak", "Chimichurri, roasted garlic", "GF · DF"),
]
SIG_BEEF_R = [
    ("Braised Beef Shanks", "Osso buco-style, gremolata, rich braising jus", "GF · DF"),
    ("Pasta Bolognese", "Hearty meat sauce, pappardelle, fresh parmesan", ""),
    ("Beef Pot Roast", "Slow-braised, root vegetables, fresh herbs", "GF · DF"),
    ("Birria-Style Beef", "Slow-braised, ancho & guajillo, consomme", "GF · DF"),
]
SIG_SEAFOOD_L = [
    ("Roasted Salmon Filet", "Herb butter, lemon, seasonal vegetables", "GF"),
    ("Gulf Shrimp Etouffee", "Classic Creole sauce, steamed rice", "GF"),
    ("Baked Catfish", "Lemon herb butter, cornmeal crust", "GF · DF"),
]
SIG_SEAFOOD_R = [
    ("Almond Crusted Tilapia", "Lemon beurre blanc, fresh herbs", ""),
    ("Firecracker Salmon", "Sweet & spicy shoyu glaze", "GF · DF"),
    ("Honey Glazed Salmon", "Roasted garlic & herb, citrus", "GF · DF"),
]
SIG_VEG_L = [
    ("Eggplant Parmesan", "Breaded, house tomato basil sauce, mozzarella", "Veg"),
    ("Cheese Enchiladas Rancheras", "Roasted tomato ranchero sauce, cotija", "Veg"),
    ("Black Bean Enchiladas", "Ancho sauce, roasted corn, cotija", "Vegan"),
    ("Vegetable Lasagna", "House tomato basil & bechamel, ricotta, mozzarella, layered roasted seasonal vegetables", "Veg"),
]
SIG_VEG_R = [
    ("Pasta al Pomodoro", "House tomato basil sauce, fresh basil, parmesan", "Vegan"),
    ("Pesto Pasta", "House basil pesto, sun-dried tomatoes, pine nuts, fettuccine, shaved parmesan", "Veg"),
    ("Stuffed Bell Peppers", "Wild rice, roasted vegetables, herb tomato sauce", "GF · Vegan"),
]

EL_POULTRY_L = [
    ("Coq au Vin", "Braised bone-in chicken thigh, red wine demi, herbs", "GF · DF"),
    ("Stuffed Chicken Breast", "Spinach & artichoke cream, roasted garlic", "GF"),
]
EL_POULTRY_R = [
    ("Herb-Roasted Half Chicken", "Pan jus, roasted garlic, fresh herbs", "GF · DF"),
    ("Pan-Seared Chicken Thighs", "Shallot pan jus, roasted root vegetables", "GF · DF"),
]
EL_BEEF_L = [
    ("Smoked Beef Brisket", "12-hour pit smoked, house BBQ, house pickles", "GF · DF"),
    ("Smoked Beef Short Ribs", "Dry-rubbed, slow smoked, red wine reduction", "GF · DF"),
    ("Garlic Herb Roasted Beef Sirloin", "Au jus, horseradish cream", "GF · DF"),
    ("Beef Tenderloin", "Roasted, herb butter, demi-glace", "GF"),
]
EL_BEEF_R = [
    ("Pan-Seared Filet Mignon", "Herb butter, red wine reduction", "GF"),
    ("Braised Lamb Shoulder", "Garlic, rosemary, red wine, slow-braised", "GF · DF"),
    ("Herb-Crusted Lamb Chops", "Dijon & herb crust, mint jus", "GF · DF"),
    ("Roasted Turkey Breast", "Herb-roasted, pan gravy, cranberry", "GF · DF"),
]
EL_SPEC_L = [
    ("Seared Salmon", "Lemon-dill beurre blanc, seasonal vegetables", "GF"),
]
EL_SPEC_R = [
    ("Carne Asada", "Marinated skirt steak, chimichurri, lime", "GF · DF"),
]

SALADS_L = [
    ("Garden Salad", "Mixed greens, cucumber, tomato, carrot, balsamic", "GF · Vegan"),
    ("Caesar Salad", "Romaine, herb croutons, shaved parmesan, house dressing", ""),
    ("Southwest Chopped Salad", "Black bean, corn, avocado, cilantro-lime dressing", "GF"),
    ("Strawberry Spinach Salad", "Candied pecans, red onion, balsamic vinaigrette", "GF"),
    ("Mediterranean Orzo Salad", "Kalamata, cucumber, feta, herbs", "Vegan"),
    ("Greek Salad", "Cucumber, tomato, kalamata olives, feta, lemon-oregano vinaigrette", "GF · Veg"),
    ("Blueberry Feta Salad", "Mixed greens, fresh blueberries, crumbled feta, candied pecans, red onion, lemon-poppy vinaigrette", "GF · Veg"),
]
SALADS_R = [
    ("Mixed Greens", "Candied pecans, cranberries, goat cheese, honey balsamic", "GF"),
    ("Quinoa Power Bowl Salad", "Roasted vegetables, chickpeas, lemon tahini dressing", "GF · Vegan"),
    ("Caprese Salad", "Fresh mozzarella, heirloom tomato, basil, EVOO", "GF"),
    ("Seasonal Fruit Salad", "Chef's selection, fresh herbs, citrus", "GF · Vegan"),
    ("Quinoa Crunch Salad", "Kale, romaine, crispy quinoa, avocado, roasted corn, cherry tomatoes, cilantro, cotija, chipotle vinaigrette — Mendocino-style", "GF · Veg"),
    ("Brussels Salad with Green Goddess", "Shaved Brussels sprouts, toasted almonds, dried cranberries, shaved pecorino, lemon green goddess dressing", "GF · Veg"),
]
SOUPS_L = [
    ("Tomato Bisque", "House tomato basil, cream, fresh basil oil", "GF · Vegan"),
    ("Italian Wedding Soup", "Mini meatballs, escarole, parmesan broth", "DF"),
]
SOUPS_R = [
    ("Black Bean Soup", "Roasted cumin, lime crema, cilantro", "GF · Vegan"),
    ("Greek-Style Lentil Soup", "Lemon, herbs, olive oil", "GF · Vegan"),
]

SIDES_SOUTH_L = [
    ("Smoked Gouda Mac & Cheese", "Smoked gouda, sharp cheddar, golden breadcrumb crust", ""),
    ("Collard Greens", "Slow-braised, smoked turkey, apple cider vinegar", "GF · DF"),
    ("Brussels Sprouts & Bacon", "Roasted, smoked bacon, balsamic glaze", "GF · DF"),
    ("Sweet Potato Mash", "Creamy mashed, butter, brown sugar, house cinnamon blend", "GF"),
    ("Red Beans & Rice", "Slow-cooked kidney beans, smoked seasonings", "GF · DF"),
]
SIDES_SOUTH_R = [
    ("Dirty Rice", "Ground beef, bell pepper, celery, Creole spices", "GF · DF"),
    ("Baked Beans", "Molasses, brown sugar, roasted peppers", "GF · Vegan"),
    ("Braised Cabbage", "Garlic, apple cider, herbs", "GF · Vegan"),
    ("Cornbread", "House recipe, honey butter", "Vegan"),
    ("Jalapeno Cornbread", "Fresh jalapeno, honey butter", "Veg"),
]
SIDES_MED_L = [
    ("Roasted Garlic Mashed Potatoes", "Roasted garlic, cream, butter", "GF"),
    ("Pasta Primavera", "Fresh vegetables, EVOO, lemon, fresh herbs", "Vegan"),
    ("Roasted Seasonal Vegetables", "EVOO, herbs, sea salt", "GF · Vegan"),
]
SIDES_MED_R = [
    ("Saffron Rice", "Fragrant saffron, herbs, citrus", "GF · Vegan"),
    ("White Bean Stew", "Rosemary, garlic, kale", "GF · Vegan"),
    ("Creamy Polenta", "Parmesan, herb butter", "GF"),
]
SIDES_AM_L = [
    ("Buttermilk Mashed Potatoes", "Butter, cream, chives", "GF"),
    ("Scalloped Potatoes", "Cream, gruyere, fresh thyme", "GF"),
    ("Garlic Parmesan Broccoli", "Roasted, parmesan, lemon zest", "GF"),
    ("Green Bean Casserole", "Cream of mushroom, crispy onions", ""),
]
SIDES_AM_R = [
    ("Rice Pilaf", "Herb butter, toasted vermicelli", "GF · DF"),
    ("Garlic Parmesan Rice Pilaf", "Roasted garlic, parmesan, fresh herbs", ""),
    ("Roasted Sweet Corn", "Herb butter, sea salt", "GF"),
    ("Herb Butter Rice", "Fresh herbs, clarified butter", "GF"),
]
SIDES_TEX_L = [
    ("Spanish Rice", "Roasted tomato, cumin, cilantro", "GF · Vegan"),
    ("Refried Beans", "Slow-cooked, seasoned", "GF · Vegan"),
    ("Charro Beans", "Pinto beans, smoked seasonings, cilantro", "GF · DF"),
]
SIDES_TEX_R = [
    ("Elote Casserole", "Roasted corn, cotija, chili butter, lime", "GF"),
    ("Roasted Corn & Black Bean Salad", "Lime vinaigrette, cilantro, red onion", "GF · Vegan"),
    ("Cilantro Lime Rice", "Lime-scented, fresh cilantro, EVOO", "GF · Vegan"),
]

STATIONS_BYO_L = [
    ("Build Your Own Taco Station", "Seasoned beef & chicken, warm tortillas, pico, guacamole, cheese, sour cream, salsa verde, jalapenos", "GF · DF"),
    ("Build Your Own Fajita Station", "Grilled chicken & steak, sauteed peppers & onions, flour & corn tortillas, full toppings bar", "GF · DF"),
    ("Baked Potato Bar", "Butter, sour cream, cheddar, bacon crumbles, chives, broccoli, chili", "GF"),
    ("Interactive Pasta Bar", "Penne & fettuccine, house tomato basil sauce, alfredo, pesto, grilled chicken, vegetables", ""),
]
STATIONS_BYO_R = [
    ("Nacho Bar", "Tortilla chips, nacho cheese, shredded chicken, refried beans, pico, jalapenos, guacamole, sour cream", "GF"),
    ("Custom Guacamole Bar", "Ripe avocado halves, smoked bacon, corn relish, cotija, pico de gallo", "GF"),
    ("Build Your Own Bruschetta Station", "Toasted crostini, roasted tomato, whipped ricotta, basil, olive tapenade, roasted garlic", "Vegan"),
    ("Mashed Potato Bar", "Whipped Yukon gold, smoked bacon, sour cream, scallions, assorted cheeses, gravy", "GF"),
]
STATIONS_CHEF_L = [
    ("Southern Shrimp & Grits Station", "Grilled Gulf shrimp, stone-ground cheddar grits, hot sauce, scallions in mini cast iron skillets", "GF"),
    ("Houston Street Corn Station", "Roasted corn, lime juice, chili salt, cotija, Valentina hot sauce, chipotle aioli", "GF · Veg"),
    ("Gourmet Slider Station", "Smoked brisket, BBQ pulled chicken, or fajita steak — brioche rolls, assorted toppings", "DF"),
    ("Empanada Station", "Beef picadillo, BBQ beef, rotisserie chicken, black bean & sweet potato — with dipping sauces", ""),
]
STATIONS_CHEF_R = [
    ("BBQ Sundae Bar", "Pulled chicken, brisket, or beans over mac & cheese, BBQ sauces, toppings", ""),
    ("Elote Station", "Roasted corn on the cob or in cups, cotija, chili, lime, cilantro, crema", "GF · Veg"),
    ("Mediterranean Mezze Station", "Hummus, dolmas, tabbouleh, pita, olives, roasted peppers, feta — full display", "Vegan"),
]
STATIONS_CARVE_L = [
    ("Smoked Beef Brisket", "12-hour pit smoked, house BBQ sauce, pickles, sliced bread", "GF · DF"),
    ("Garlic Herb Roasted Beef Sirloin", "Au jus, whipped horseradish cream", "GF · DF"),
]
STATIONS_CARVE_R = [
    ("Roasted Turkey Breast", "Pan gravy, cranberry relish, herb butter", "GF · DF"),
    ("Herb-Roasted Half Chicken", "Pan jus, roasted garlic, fresh herbs", "GF · DF"),
]

DES_SPECIALTY_L = [
    ("Build Your Own Ice Cream Bar", "Dairy: vanilla, chocolate, strawberry. Non-dairy: coconut, oat. Toppings include hot fudge, caramel, fresh berries, nuts, sprinkles, whipped cream, cherries, crushed cookies. Served in bowls, sugar cones, or waffle cones.", "Veg"),
    ("Affogato Bar — Dairy & Non-Dairy", "Vanilla bean ice cream (dairy or coconut) with a fresh-pulled espresso pour. Made to order. A perfect end-of-meal moment.", "Veg"),
]
DES_SPECIALTY_R = [
    ("Dessert Grazing Board", "Custom sweet display — chocolates, baked bites, fresh fruit, mini cheesecakes. See Charcuterie & Grazing Spreads menu for full styling options.", ""),
]

DES_CLASSIC_L = [
    ("Tres Leches Cake", "Cinnamon-infused coconut milk soak, vanilla cream", ""),
    ("Tiramisu", "Espresso-soaked ladyfingers, mascarpone, cocoa", ""),
    ("Cannoli", "Crispy hand-rolled shell, sweet ricotta filling, mini chocolate chips", ""),
    ("Banana Pudding", "Layered house recipe, Nilla wafers, whipped cream", ""),
    ("Bread Pudding", "Golden raisins, whipped cream", ""),
]
DES_CLASSIC_R = [
    ("Mini Cheesecakes", "Assorted flavors, graham crust, fresh fruit", ""),
    ("Brownie Bites", "Fudgy dark chocolate, powdered sugar", ""),
    ("Assorted Cookie Platter", "Chocolate chip, oatmeal raisin, white chocolate macadamia nut", ""),
    ("Lemon Bars", "Shortbread crust, lemon curd, powdered sugar", ""),
]

BEV_L = [
    ("Sweet Tea", "House-brewed, fresh lemon", "GF · Vegan"),
    ("Lemonade", "Fresh-squeezed style, classic or strawberry", "GF · Vegan"),
    ("Agua Fresca", "Hibiscus, tamarind, or cucumber lime", "GF · Vegan"),
    ("House Mocktail Station", "Rotating seasonal selections", "GF · Vegan"),
    ("Coffee Station", "Regular & decaf, cream & sugar service", "GF · Vegan"),
    ("Espresso Service", "Fresh-pulled single, double, or specialty espresso. Standalone or paired with desserts.", "GF · Vegan"),
]
BEV_R = [
    ("Unsweet Tea", "House-brewed", "GF · Vegan"),
    ("Infused Water", "Seasonal fruit & herb combinations", "GF · Vegan"),
    ("Sparkling Fruit Punch", "Seasonal fruit, sparkling water, citrus", "GF · Vegan"),
    ("Sparkling Water", "Still & sparkling options", "GF · Vegan"),
    ("Hot Tea Service", "Assorted teas, honey, lemon", "GF · Vegan"),
    ("Cafe Drinks", "Lattes, cappuccinos, cortados, mochas, americanos — fully customizable. Custom beverage service available.", "GF · Vegan"),
]


# ══════════════════════════════════════════════════════════════
# PAGE BUILDER HELPER
# ══════════════════════════════════════════════════════════════

class PageManager:
    def __init__(self, c, section, version="v3.18"):
        self.c = c
        self.section = section
        self.version = version
        self._start_page()

    def _start_page(self):
        draw_page_header(self.c, self.section)
        # Cover is PDF page 1 and is unnumbered. Interior pages start at "Page 1".
        interior_page = self.c.getPageNumber() - 1
        draw_page_footer(self.c, self.version, page_num=interior_page)
        self.y = BODY_T

    def need_space(self, needed):
        if self.y - needed < BODY_B:
            self.c.showPage()
            self._start_page()
            return True
        return False

    def section_header(self, title):
        self.need_space(40)
        self.y = section_header(self.c, self.y, title)

    def section_intro_text(self, text):
        self.need_space(30)
        self.y = section_intro(self.c, self.y, text)

    def cat(self, title, min_content_height=55):
        # Reserve space for the category header + one full row of content
        # (including a 2-line description). 13pt header + 55pt row = 68pt total.
        # Prevents the subsection header from orphaning at the bottom of a page.
        self.need_space(13 + min_content_height)
        self.y = category_header(self.c, self.y, title)

    def two_col(self, left, right):
        while left or right:
            self.need_space(40)
            self.y, li, ri = two_col_items(
                self.c, self.y, left, right, BODY_B)
            left  = left[li:]
            right = right[ri:]

    def spacer(self, pts=10):
        self.y -= pts


# ══════════════════════════════════════════════════════════════
# BUILD CORPORATE & SOCIAL MENU
# ══════════════════════════════════════════════════════════════

def build_corporate(path, version="v3.18"):
    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle("Citizens Catering — Corporate & Social Menu")

    draw_cover(c, "CORPORATE & SOCIAL MENU",
               "Houston, TX  •  Full-Service Catering  •  Custom Menus",
               version=version)
    c.showPage()

    pm = PageManager(c, "APPETIZERS & ENTREES", version=version)
    pm.section_header("HORS D'OEUVRES")
    pm.section_intro_text(
        "Can be passed butler-style or displayed. Minimums apply. Custom packages available.")

    pm.cat("Vegetarian & Vegan")
    pm.two_col(HORS_VEG, HORS_VEG_R)
    pm.spacer(2)

    pm.cat("Seafood")
    pm.two_col(HORS_SEAFOOD_L, HORS_SEAFOOD_R)
    pm.spacer(2)

    pm.cat("Poultry")
    pm.two_col(HORS_POULTRY_L, HORS_POULTRY_R)
    pm.spacer(2)

    pm.cat("Beef")
    pm.two_col(HORS_BEEF_L, HORS_BEEF_R)
    pm.spacer(2)

    pm.cat("Charcuterie & Display Options")
    # v3.19: Custom Grazing Spreads moved to left column.
    # Left:  Standard Charcuterie, Premium Charcuterie, Custom Grazing Spreads
    # Right: Mediterranean Mezze, Antipasto Board
    pm.two_col(
        [CHARCUTERIE[0], CHARCUTERIE[1], CHARCUTERIE[4]],
        [CHARCUTERIE[2], CHARCUTERIE[3]],
    )
    pm.spacer(20)

    pm.section_header("SIGNATURE ENTREES")
    pm.section_intro_text(
        "All entrees include one salad or soup and two sides. All sauces and pastas are made in-house from scratch. "
        "China, silverware, and linen napkins included with buffet and plated packages.")

    pm.cat("Poultry")
    pm.two_col(SIG_POULTRY_L, SIG_POULTRY_R)
    pm.spacer(6)

    pm.cat("Beef")
    pm.two_col(SIG_BEEF_L, SIG_BEEF_R)
    pm.spacer(6)

    pm.cat("Seafood")
    pm.two_col(SIG_SEAFOOD_L, SIG_SEAFOOD_R)
    pm.spacer(6)

    pm.cat("Vegetarian & Vegan")
    pm.two_col(SIG_VEG_L, SIG_VEG_R)
    pm.spacer(14)

    pm.section_header("ELEVATED ENTREES")
    pm.section_intro_text(
        "Premium selections for plated dinners, family-style service, "
        "and elevated buffet presentations.")

    pm.cat("Poultry")
    pm.two_col(EL_POULTRY_L, EL_POULTRY_R)
    pm.spacer(6)

    pm.cat("Beef & Lamb")
    pm.two_col(EL_BEEF_L, EL_BEEF_R)
    pm.spacer(6)

    pm.cat("Seafood & Specialty")
    pm.two_col(EL_SPEC_L, EL_SPEC_R)
    c.showPage()

    pm = PageManager(c, "ACCOMPANIMENTS & FINISH", version=version)
    pm.section_header("SALADS, SOUPS & SIDES")
    pm.section_intro_text(
        "All buffet and plated packages include one salad or soup selection plus two sides. "
        "Additional sides available at supplemental cost.")

    pm.cat("Salads")
    pm.two_col(SALADS_L, SALADS_R)
    pm.spacer(2)

    pm.cat("Soups")
    pm.two_col(SOUPS_L, SOUPS_R)
    pm.spacer(8)

    pm.cat("Sides — Southern")
    pm.two_col(SIDES_SOUTH_L, SIDES_SOUTH_R)
    pm.spacer(2)

    pm.cat("Sides — Mediterranean / Italian")
    pm.two_col(SIDES_MED_L, SIDES_MED_R)
    pm.spacer(2)

    pm.cat("Sides — Classic American")
    pm.two_col(SIDES_AM_L, SIDES_AM_R)
    pm.spacer(2)

    pm.cat("Sides — Tex-Mex / Latin")
    pm.two_col(SIDES_TEX_L, SIDES_TEX_R)
    pm.spacer(20)

    pm.section_header("ACTION STATIONS")
    pm.section_intro_text(
        "Three stations recommended for full action station dinner service. "
        "Individual stations may be added to any package. Chef-attended stations available.")

    pm.cat("Build-Your-Own Stations")
    pm.two_col(STATIONS_BYO_L, STATIONS_BYO_R)
    pm.spacer(6)

    pm.cat("Chef-Attended & Specialty Stations")
    pm.two_col(STATIONS_CHEF_L, STATIONS_CHEF_R)
    pm.spacer(6)

    pm.cat("Carving Stations")
    pm.two_col(STATIONS_CARVE_L, STATIONS_CARVE_R)
    pm.spacer(20)

    pm.section_header("DESSERT STATIONS & DISPLAYS")
    pm.section_intro_text(
        "Mix and match stations and displays for your perfect sweet finish. "
        "Custom packages available.")

    pm.cat("Citizens Specialty — Interactive & Featured")
    pm.two_col(DES_SPECIALTY_L, DES_SPECIALTY_R)
    pm.spacer(6)

    pm.cat("Classic Selections")
    pm.two_col(DES_CLASSIC_L, DES_CLASSIC_R)
    pm.spacer(10)

    pm.section_header("BEVERAGES")
    pm.two_col(BEV_L, BEV_R)
    pm.spacer(14)

    pm.need_space(280)
    pm.section_header("SERVICE PACKAGES")
    pm.spacer(6)
    pm.need_space(90)
    pm.y = package_card(c, pm.y,
        "Buffet or Seated Dinner",
        ["One or two entree selections",
         "One salad or soup",
         "Two sides",
         "China-like dinnerware, silverware & black linen napkins",
         "Pre-set water goblet",
         "Cake cutting & coffee service upon request"])
    pm.y = package_card(c, pm.y,
        "Action Stations Service",
        ["Three chef-attended stations",
         "China-like acrylic and unique dinnerware",
         "Cake cutting & coffee service upon request",
         "Individual stations may be added to any package",
         "Custom menus and dietary accommodations available",
         "Halal options available upon request"])
    pm.spacer(14)
    pm.need_space(80)
    pm.y = contact_closer(c, pm.y,
        "LET US SERVE YOUR CITY",
        "Vegetarian & vegan menus available. All dietary preferences accommodated. "
        "*Prices subject to change without prior notice.")

    c.save()
    print(f"Saved: {path}")


if __name__ == '__main__':
    out = os.path.join(SCRIPT_DIR, 'Citizens_Corporate_Social_v3.21.pdf')
    build_corporate(out, version="v3.21")
    print("All done.")
