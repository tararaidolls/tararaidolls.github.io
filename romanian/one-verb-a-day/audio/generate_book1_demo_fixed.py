#!/usr/bin/env python3
import sys, os
sys.path.append("/workspace/one-verb-a-day/romanian")
from fpdf import FPDF

from extract_import import verbs_100

PAGE_W = 8.5 * 25.4  # mm
PAGE_H = 11 * 25.4   # mm
MARGIN = 0.5 * 25.4   # 12.7 mm
CONTENT_W = PAGE_W - 2 * MARGIN
GREY = (221, 221, 221)
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
DARK_GREY = (80, 80, 80)
TEAL = (40, 100, 100)

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

    def draw_verb_page(self, day_num, verb_info, example_text):
        self.add_page()
        verb, translation, present, past, future = verb_info
        
        # Header - Day N
        self.set_fill_color(*TEAL)
        self.rect(MARGIN, MARGIN, CONTENT_W, 15, 'F')
        self.set_y(MARGIN + 3)
        self.set_font('DS', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"VERB {day_num} / 100", 0, 1, 'C')
        
        self.ln(10)
        self.set_font('DS', 'B', 32)
        self.set_text_color(*BLACK)
        self.cell(0, 15, verb, 0, 1, 'C')
        
        self.set_font('DS', '', 16)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 10, f"- to {translation} -", 0, 1, 'C')
        self.ln(10)
        
        # Tense table
        col_w = CONTENT_W / 3
        y_start = self.get_y()
        self.set_fill_color(*LIGHT_GREY)
        self.rect(MARGIN, y_start, CONTENT_W, 10, 'F')
        
        self.set_font('DS', 'B', 12)
        self.set_text_color(*BLACK)
        for t in TENSES:
            self.cell(col_w, 10, t, 1, 0, 'C')
        self.ln(10)
        
        self.set_font('DS', '', 11)
        for i in range(6):
            self.cell(col_w, 10, present[i], 1, 0, 'C')
            self.cell(col_w, 10, past[i], 1, 0, 'C')
            self.cell(col_w, 10, future[i], 1, 1, 'C')
            
        self.ln(15)
        
        # Examples Box
        self.set_font('DS', 'B', 14)
        self.set_text_color(*TEAL)
        self.cell(0, 10, "READ IT (Examples in Context):", 0, 1, 'L')
        self.set_fill_color(245, 245, 250)
        self.rect(MARGIN, self.get_y(), CONTENT_W, 25, 'F')
        self.set_y(self.get_y() + 4)
        self.set_x(MARGIN + 5)
        self.set_font('DS', 'B', 11)
        self.set_text_color(40, 40, 50)
        self.multi_cell(CONTENT_W - 10, 6, f"• {example_text[0]}")
        self.set_x(MARGIN + 5)
        self.set_font('DS', '', 10)
        self.set_text_color(100, 100, 110)
        self.multi_cell(CONTENT_W - 10, 6, f"  ({example_text[1]})")
        self.ln(5)

        # WRITE IT Section with Specific Prompts
        self.set_font('DS', 'B', 14)
        self.set_text_color(*TEAL)
        self.cell(0, 10, "WRITE IT (Your Daily Practice):", 0, 1, 'L')
        
        self.set_font('DS', '', 10)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 6, "Write 3 different sentences using this verb.", 0, 1, 'L')
        self.ln(5)
        
        self.set_draw_color(*GREY)
        line_h = 10
        prompts = ["1. Use this verb in the PRESENT tense:", 
                   "2. Use this verb in the PAST tense:", 
                   "3. Use this verb in the FUTURE tense:"]
                   
        for prompt in prompts:
            self.set_font('DS', 'B', 11)
            self.set_text_color(*DARK_GREY)
            self.cell(0, line_h, prompt, 0, 1, 'L')
            
            start_x = MARGIN
            y_pos = self.get_y() + line_h
            
            # Draw 2 lines per sentence prompt
            for _ in range(2):
                self.line(start_x, y_pos, MARGIN + CONTENT_W, y_pos)
                y_pos += line_h
                
            self.ln(line_h * 2.5)

pdf = VerbBook()

ex1 = ("Eu sunt foarte fericit astăzi.", "I am very happy today.")
ex2 = ("Ea are o casă mare în oraș.", "She has a big house in the city.")

pdf.draw_verb_page(1, verbs_100[0], ex1)
pdf.draw_verb_page(2, verbs_100[1], ex2)

pdf.output("/workspace/one-verb-a-day/test_book1_format_fixed.pdf")
