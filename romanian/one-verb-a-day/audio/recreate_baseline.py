#!/usr/bin/env python3
import sys, os
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
DARK_GREY = (80, 80, 80)

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
        self.ln(2)
        
        prompts = [
            ("PREZENT", "—   Write about TODAY:"),
            ("PERFECT COMPUS", "—   Write about YESTERDAY:"),
            ("VIITOR", "—   Write about TOMORROW:"),
            ("NEGATIV", "—   Write what you DON'T do:"),
            ("ÎNTREBARE", "—   Ask someone a question:"),
            ("VIAȚA TA", "—   Use this verb about YOUR life:")
        ]
        
        self.set_draw_color(*GREY)
        for title, subtitle in prompts:
            self.set_font('DS', 'B', 9)
            self.set_text_color(*BLACK)
            self.cell(40, 10, title, 0, 0, 'L')
            self.set_font('DS', '', 9)
            self.cell(0, 10, subtitle, 0, 1, 'L')
            
            y_pos = self.get_y() + 8
            self.line(MARGIN, y_pos, MARGIN + CONTENT_W, y_pos)
            self.ln(12)
            
        self.ln(5)
        
        # --- BONUS ---
        self.set_font('DS', 'B', 11)
        self.cell(0, 10, "BONUS", 0, 1, 'L')
        self.set_font('DS', '', 9)
        self.cell(0, 8, "Related words/phrases: 1.________________ 2.________________ 3.________________", 0, 1, 'L')
        self.cell(0, 8, "Idiom or expression: _____________________ Meaning: _____________________", 0, 1, 'L')
        self.ln(5)
        
        # --- TODAY'S LOG ---
        self.set_font('DS', 'B', 11)
        self.cell(0, 10, "TODAY'S LOG", 0, 1, 'L')
        
        self.set_fill_color(252, 252, 252)
        self.set_draw_color(220, 220, 220)
        self.rect(MARGIN, self.get_y(), CONTENT_W, 12, 'DF')
        
        self.set_y(self.get_y() + 2)
        self.set_x(MARGIN + 2)
        self.set_font('DS', '', 8)
        self.set_text_color(*DARK_GREY)
        
        log_text = "Time spent: ___ min | Difficulty: O Easy O Medium O Hard | Confidence: 1 2 3 4 5 | Review again? [ ]"
        self.cell(0, 8, log_text, 0, 1, 'L')

pdf = VerbBook()
pdf.draw_verb_page(1, verbs_100[0])
pdf.draw_verb_page(2, verbs_100[1])

pdf.output("/workspace/one-verb-a-day/test_baseline_recreated.pdf")
