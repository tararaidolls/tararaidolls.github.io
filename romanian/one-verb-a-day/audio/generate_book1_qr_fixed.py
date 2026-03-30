#!/usr/bin/env python3
import sys, json, os
import qrcode
from fpdf import FPDF
from gtts import gTTS

sys.path.append("/workspace/one-verb-a-day/romanian")

# Only generate first 2 verbs to show the concept
verbs_100 = [
    ["a fi", "to be", ["sunt", "ești", "este", "suntem", "sunteți", "sunt"], ["am fost", "ai fost", "a fost", "am fost", "ați fost", "au fost"], ["voi fi", "vei fi", "va fi", "vom fi", "veți fi", "vor fi"]],
    ["a avea", "to have", ["am", "ai", "are", "avem", "aveți", "au"], ["am avut", "ai avut", "a avut", "am avut", "ați avut", "au avut"], ["voi avea", "vei avea", "va avea", "vom avea", "veți avea", "vor avea"]]
]

os.makedirs("/workspace/one-verb-a-day/romanian/audio", exist_ok=True)
os.makedirs("/workspace/one-verb-a-day/romanian/qr", exist_ok=True)

# Generate Audio & QR for 2 verbs
for i, v in enumerate(verbs_100):
    idx = i + 1
    text = f"{v[0]}. {v[2][0]}, {v[2][1]}, {v[2][2]}, {v[2][3]}, {v[2][4]}, {v[2][5]}."
    tts = gTTS(text=text, lang="ro")
    tts.save(f"/workspace/one-verb-a-day/romanian/audio/verb_{idx}.mp3")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    url = f"https://tararaidolls.github.io/romanian/one-verb-a-day/audio/verb_{idx}.mp3"
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"/workspace/one-verb-a-day/romanian/qr/verb_{idx}.png")

PAGE_W = 8.5 * 25.4
PAGE_H = 11 * 25.4
MARGIN = 0.5 * 25.4
CONTENT_W = PAGE_W - 2 * MARGIN

GREY = (221, 221, 221)
LIGHT_GREY = (245, 245, 245)
BLACK = (0, 0, 0)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PRONOUNS = ["Eu", "Tu", "El/Ea", "Noi", "Voi", "Ei/Ele"]

class Vol1Book(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', (PAGE_W, PAGE_H))
        self.add_font('DS', '', FONT_PATH)
        self.add_font('DS', 'B', FONT_PATH_BOLD)
        self.set_auto_page_break(auto=True, margin=MARGIN)

    def draw_verb_page(self, day_num, verb_info):
        self.add_page()
        verb, translation, present, past, future = verb_info
        
        # --- HEADER ---
        self.set_font('DS', 'B', 16)
        self.set_text_color(*BLACK)
        self.cell(100, 10, f"DAY {day_num}/100", 0, 0, 'L')
        
        self.set_font('DS', '', 10)
        self.cell(0, 10, "DATE: ___/___/___", 0, 1, 'R')
        self.ln(5)
        
        self.set_font('DS', 'B', 14)
        self.cell(0, 10, f"TODAY'S VERB: {verb} — {translation}", 0, 1, 'R')
        self.ln(5)
        
        y_before_table = self.get_y()
        
        # QR Code Center (Higher, between Header and Table)
        qr_w = 16 # slightly smaller
        qr_x = MARGIN + (CONTENT_W - qr_w) / 2
        qr_path = f"/workspace/one-verb-a-day/romanian/qr/verb_{day_num}.png"
        self.image(qr_path, x=qr_x, y=y_before_table, w=qr_w)
        
        # "Scan to listen" under QR
        self.set_y(y_before_table + qr_w)
        self.set_font('DS', '', 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Scan to listen", 0, 1, 'C')
        
        self.ln(2) # very small gap to save space
        
        # --- TABLE ---
        col1_w = 30
        col_w = (CONTENT_W - col1_w) / 3
        
        self.set_fill_color(*LIGHT_GREY)
        self.set_text_color(*BLACK)
        self.set_font('DS', 'B', 9)
        self.cell(col1_w, 8, "", 'TLR', 0, 'C', True)
        self.cell(col_w, 8, "Prezent", 1, 0, 'C', True)
        self.cell(col_w, 8, "Perfect Compus", 1, 0, 'C', True)
        self.cell(col_w, 8, "Viitor", 1, 1, 'C', True)
        
        self.set_font('DS', 'B', 8)
        for i in range(6):
            self.set_font('DS', 'B', 8)
            self.cell(col1_w, 8, PRONOUNS[i], 1, 0, 'L')
            self.set_font('DS', '', 8)
            self.cell(col_w, 8, present[i], 1, 0, 'L')
            self.cell(col_w, 8, past[i], 1, 0, 'L')
            self.cell(col_w, 8, future[i], 1, 1, 'L')
            
        self.ln(8) # reduced margin to save space
        
        # --- USE IT - 6 Sentences ---
        self.set_font('DS', 'B', 12)
        self.cell(0, 10, "USE IT — 6 Sentences", 0, 1, 'L')
        self.ln(2) # reduced margin to save space
        
        prompts = [
            ("PREZENT", "—   Write about TODAY:"),
            ("PERFECT COMPUS", "—   Write about YESTERDAY:"),
            ("VIITOR", "—   Write about TOMORROW:"),
            ("NEGATIV", "—   Write what you DON'T do:"),
            ("ÎNTREBARE", "—   Ask someone a question:"),
            ("VIAȚA TA", "—   Use this verb about YOUR life:")
        ]
        
        self.set_draw_color(*GREY)
        line_spacing = 8
        for title, subtitle in prompts:
            self.set_font('DS', 'B', 9)
            self.cell(40, 10, title, 0, 0, 'L')
            self.set_font('DS', '', 9)
            self.cell(0, 10, subtitle, 0, 1, 'L')
            
            y_pos = self.get_y() + 2
            self.line(MARGIN, y_pos, MARGIN + CONTENT_W, y_pos)
            y_pos += line_spacing
            self.line(MARGIN, y_pos, MARGIN + CONTENT_W, y_pos)
            
            self.ln(line_spacing * 1.5)

pdf = Vol1Book()
pdf.draw_verb_page(1, verbs_100[0])
pdf.draw_verb_page(2, verbs_100[1])

pdf.output("/workspace/one-verb-a-day/test_qr_book1_fixed.pdf")
