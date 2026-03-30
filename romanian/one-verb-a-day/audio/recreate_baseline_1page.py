#!/usr/bin/env python3
import sys
sys.path.append("/workspace/one-verb-a-day/romanian")
from fpdf import FPDF
from extract_import import verbs_100

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
TENSES = ["Prezent", "Perfect Compus", "Viitor"]

class VerbBook(FPDF):
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
        
        # --- TABLE ---
        col1_w = 30
        col_w = (CONTENT_W - col1_w) / 3
        y_start = self.get_y()
        
        # Table Header
        self.set_fill_color(*LIGHT_GREY)
        self.set_font('DS', 'B', 9)
        self.cell(col1_w, 8, "", 'TLR', 0, 'C', True)
        self.cell(col_w, 8, "Prezent", 1, 0, 'C', True)
        self.cell(col_w, 8, "Perfect Compus", 1, 0, 'C', True)
        self.cell(col_w, 8, "Viitor", 1, 1, 'C', True)
        
        # Table Rows
        self.set_font('DS', 'B', 8)
        for i in range(6):
            self.set_font('DS', 'B', 8)
            self.cell(col1_w, 8, PRONOUNS[i], 1, 0, 'L')
            self.set_font('DS', '', 8)
            self.cell(col_w, 8, present[i], 1, 0, 'L')
            self.cell(col_w, 8, past[i], 1, 0, 'L')
            self.cell(col_w, 8, future[i], 1, 1, 'L')
            
        self.ln(10)
        
        # --- USE IT - 6 Sentences ---
        self.set_font('DS', 'B', 12)
        self.cell(0, 10, "USE IT — 6 Sentences", 0, 1, 'L')
        self.ln(5)
        
        prompts = [
            ("PREZENT", "—   Write about TODAY:"),
            ("PERFECT COMPUS", "—   Write about YESTERDAY:"),
            ("VIITOR", "—   Write about TOMORROW:"),
            ("NEGATIV", "—   Write what you DON'T do:"),
            ("ÎNTREBARE", "—   Ask someone a question:"),
            ("VIAȚA TA", "—   Use this verb about YOUR life:")
        ]
        
        self.set_draw_color(*GREY)
        # Reduced line spacing so it fits neatly on ONE page
        line_spacing = 8
        for title, subtitle in prompts:
            self.set_font('DS', 'B', 9)
            self.cell(40, 10, title, 0, 0, 'L')
            self.set_font('DS', '', 9)
            self.cell(0, 10, subtitle, 0, 1, 'L')
            
            y_pos = self.get_y() + 2
            # Just 2 lines per prompt to ensure it fits perfectly
            self.line(MARGIN, y_pos, MARGIN + CONTENT_W, y_pos)
            y_pos += line_spacing
            self.line(MARGIN, y_pos, MARGIN + CONTENT_W, y_pos)
            
            self.ln(line_spacing * 1.5)

pdf = VerbBook()
pdf.draw_verb_page(1, verbs_100[0])
pdf.draw_verb_page(2, verbs_100[1])

pdf.output("/workspace/one-verb-a-day/test_baseline_1page.pdf")
