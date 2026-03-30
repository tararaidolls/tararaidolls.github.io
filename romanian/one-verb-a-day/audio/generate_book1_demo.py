#!/usr/bin/env python3
import sys, os
sys.path.append("/workspace/one-verb-a-day/romanian")
from fpdf import FPDF
from PyPDF2 import PdfMerger

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
        
        # Examples Box (New Addition)
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

        # Write 3 sentences section (Same as original)
        self.set_font('DS', 'B', 14)
        self.set_text_color(*TEAL)
        self.cell(0, 10, "WRITE IT (Your Daily Practice):", 0, 1, 'L')
        
        self.set_font('DS', '', 10)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 6, "Write 3 different sentences using this verb (try using Past, Present, and Future tenses).", 0, 1, 'L')
        self.ln(5)
        
        self.set_draw_color(*GREY)
        line_h = 10
        for i in range(1, 4):
            self.set_font('DS', 'B', 14)
            self.set_text_color(*GREY)
            self.cell(10, line_h, f"{i}.", 0, 0, 'L')
            
            start_x = self.get_x() + 2
            y_pos = self.get_y() + line_h
            
            # Draw 3 lines per sentence
            for _ in range(3):
                self.line(start_x, y_pos, MARGIN + CONTENT_W, y_pos)
                y_pos += line_h
                
            self.ln(line_h * 3.5)

pdf = VerbBook()

# Intro Pages (Simulated)
pdf.add_page()
pdf.set_font('DS', 'B', 24)
pdf.set_text_color(*TEAL)
pdf.cell(0, 20, "HOW TO USE THIS BOOK", 0, 1, 'L')
pdf.set_font('DS', '', 12)
pdf.set_text_color(*BLACK)
intro_text = """Welcome to the 100-Day Romanian Verb Challenge!
Verbs are the engine of any language. Without them, you can’t build a single sentence. This workbook is designed to help you master the 100 most essential Romanian verbs in 100 days.

Here is your daily routine:
1. Learn the Conjugation: Study the Past, Present, and Future tenses.
2. Read the Examples: See the verb used in a real-life context.
3. Write Your Own (The Magic Step!): This is where real learning happens. Do not just copy our examples. Write 3 completely new sentences using the verb of the day. 

PRO TIP: Independent Work is Your Superpower!
Don't limit yourself to the vocabulary on the page. We strongly encourage you to look up new words! Use the "My Custom Vocabulary Bank" pages to write down all the new nouns, adjectives, and time markers you discover."""
pdf.multi_cell(0, 8, intro_text)

# Vocabulary Bank Page
pdf.add_page()
pdf.set_font('DS', 'B', 24)
pdf.set_text_color(*TEAL)
pdf.cell(0, 20, "MY CUSTOM VOCABULARY BANK", 0, 1, 'C')
pdf.set_font('DS', '', 10)
pdf.set_text_color(*DARK_GREY)
pdf.cell(0, 10, "Write down new nouns, adjectives, and time markers you find or look up.", 0, 1, 'C')
pdf.ln(5)

pdf.set_font('DS', 'B', 12)
pdf.set_text_color(*BLACK)
col_w_v = CONTENT_W / 2
pdf.cell(col_w_v, 10, "Romanian Word", 1, 0, 'C')
pdf.cell(col_w_v, 10, "English Translation", 1, 1, 'C')
pdf.set_draw_color(*GREY)
for i in range(20):
    pdf.cell(col_w_v, 10, "", 1, 0)
    pdf.cell(col_w_v, 10, "", 1, 1)

# Theme 1 Divider
pdf.add_page()
pdf.set_fill_color(*TEAL)
pdf.rect(MARGIN, MARGIN, CONTENT_W, PAGE_H - 2*MARGIN, 'F')
pdf.ln(100)
pdf.set_font('DS', 'B', 48)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 20, "PART 1", 0, 1, 'C')
pdf.ln(20)
pdf.set_font('DS', '', 24)
pdf.cell(0, 20, "Survival & Basics", 0, 1, 'C')
pdf.cell(0, 20, "(Verbs 1 - 25)", 0, 1, 'C')

# First 3 verbs for demo
ex1 = ("Eu sunt foarte fericit astăzi.", "I am very happy today.")
ex2 = ("Ea are o casă mare în oraș.", "She has a big house in the city.")
ex3 = ("Noi mergem la școală cu autobuzul.", "We go to school by bus.")

pdf.draw_verb_page(1, verbs_100[0], ex1)
pdf.draw_verb_page(2, verbs_100[1], ex2)
pdf.draw_verb_page(3, verbs_100[2], ex3)

pdf.output("/workspace/one-verb-a-day/test_book1_format.pdf")
