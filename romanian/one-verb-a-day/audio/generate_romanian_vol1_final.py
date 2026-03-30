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
DARK_GREY = (80, 80, 80)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PRONOUNS = ["Eu", "Tu", "El/Ea", "Noi", "Voi", "Ei/Ele"]

class Vol1Book(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', (PAGE_W, PAGE_H))
        self.add_font('DS', '', FONT_PATH)
        self.add_font('DS', 'B', FONT_PATH_BOLD)
        self.set_auto_page_break(auto=True, margin=MARGIN)

    def title_page(self):
        self.add_page()
        self.set_y(60)
        self.set_font('DS', 'B', 48)
        self.set_text_color(*BLACK)
        self.cell(0, 20, "ONE VERB", 0, 1, 'C')
        self.cell(0, 20, "A DAY", 0, 1, 'C')
        
        self.ln(20)
        self.set_font('DS', '', 24)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 15, "Romanian Verb Mastery", 0, 1, 'C')
        
        self.ln(20)
        self.set_font('DS', 'B', 20)
        self.set_text_color(*BLACK)
        self.cell(0, 15, "VOLUME 1: Survival & Basics", 0, 1, 'C')
        
        self.ln(10)
        self.set_font('DS', '', 14)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 10, "Verbs 1 - 100", 0, 1, 'C')
        
        self.set_y(220)
        self.set_font('DS', '', 12)
        self.cell(0, 10, "by Maryna Skliar", 0, 1, 'C')

    def intro_pages(self):
        self.add_page()
        self.set_font('DS', 'B', 20)
        self.set_text_color(*BLACK)
        self.cell(0, 15, "HOW TO USE THIS BOOK", 0, 1, 'L')
        self.ln(5)
        
        self.set_font('DS', '', 11)
        self.set_text_color(*BLACK)
        intro = (
            "Welcome to Volume 1 of the Romanian Verb Challenge!\n"
            "Verbs are the engine of any language. Without them, you can't build a single sentence. "
            "This workbook is designed to help you master the 100 most essential Romanian verbs.\n\n"
            "Here is your daily routine:\n"
            "1. Learn the Conjugation: Every day, you will learn a new verb and its forms in the Past, Present, and Future tenses.\n"
            "2. Write Your Own (The Magic Step!): This is where real learning happens. "
            "Write 6 completely new sentences using the verb of the day. Follow the prompts for each tense.\n\n"
            "PRO TIP: Independent Work is Your Superpower!\n"
            "Don't limit yourself to the vocabulary on the page. We strongly encourage you to look up new words! "
            "Want to say 'I drank coffee with my dog yesterday'? Look up the Romanian words for coffee and dog. "
            "Use the 'My Custom Vocabulary Bank' pages to write down all the new nouns, adjectives, and time markers you discover. "
            "Mix and match these words with your daily verbs to build sentences that are meaningful to YOUR life."
        )
        self.multi_cell(0, 7, intro)
        
        self.ln(15)
        self.set_font('DS', 'B', 20)
        self.set_text_color(*BLACK)
        self.cell(0, 15, "THE 400-VERB JOURNEY", 0, 1, 'L')
        self.ln(5)
        
        self.set_font('DS', '', 11)
        self.set_text_color(*BLACK)
        journey = (
            "Learning a language is a journey. To truly master Romanian, you don't need to memorize 5,000 random words. "
            "You need to confidently use the top 400 verbs that native speakers use every single day.\n\n"
            "This workbook is part of a 4-Volume series:\n\n"
            "VOLUME 1: Survival & Basics (Verbs 1-100)\n"
            "(You are here!) This is your foundation. Master these, and you can survive in Romania.\n\n"
            "VOLUME 2: Daily Life & Routine (Verbs 101-200)\n"
            "Once you can survive, it's time to talk about your day! Waking up, eating, cleaning, sleeping.\n\n"
            "VOLUME 3: Work, Travel & Community (Verbs 201-300)\n"
            "Verbs you need to commute, work in an office, travel, buy things, and interact with the world.\n\n"
            "VOLUME 4: Thoughts, Emotions & Abstract (Verbs 301-400)\n"
            "The final boss. Express deep feelings, argue opinions, remember the past, and explain complex ideas."
        )
        self.multi_cell(0, 7, journey)
        
        # Question Builder Page
        self.add_page()
        self.set_font('DS', 'B', 20)
        self.set_text_color(*BLACK)
        self.cell(0, 15, "THE QUESTION BUILDER", 0, 1, 'L')
        self.ln(5)
        
        self.set_font('DS', '', 11)
        self.set_text_color(*BLACK)
        questions = (
            "How to Ask Questions in Romanian\n"
            "Asking questions is half of any conversation! Before you start building your daily sentences, keep these question words and rules handy.\n\n"
            "The Golden Rule of Romanian Questions:\n"
            "In Romanian, you don't need complicated helper words like 'do' or 'does'. You simply use a questioning tone of voice or flip the subject and the verb. It is very similar to Spanish or Italian!\n"
            "• Statement: Tu vorbești engleză. (You speak English.)\n"
            "• Question: Vorbești engleză? (Do you speak English?)\n\n"
            "The Essential Question Words:\n"
            "• Ce? = What? (Ce vrei să mănânci? - What do you want to eat?)\n"
            "• Cine? = Who? (Cine este prietenul tău? - Who is your friend?)\n"
            "• Unde? = Where? (Unde locuiești? - Where do you live?)\n"
            "• Când? = When? (Când ajungi? - When do you arrive?)\n"
            "• De ce? = Why? (De ce studiezi româna? - Why do you study Romanian?)\n"
            "• Cum? = How? (Cum ești? - How are you?)\n"
            "• Cât / Câtă / Câți / Câte? = How much/many? (Cât costă? - How much does it cost?)\n\n"
            "Challenge: Try starting some of your daily sentences with these question words! Instead of just writing 'I will travel to Bucharest', challenge yourself to write 'When will I travel to Bucharest?'"
        )
        self.multi_cell(0, 7, questions)

    def vocab_bank(self):
        for _ in range(2):
            self.add_page()
            self.set_font('DS', 'B', 20)
            self.set_text_color(*BLACK)
            self.cell(0, 15, "MY CUSTOM VOCABULARY BANK", 0, 1, 'C')
            self.set_font('DS', '', 10)
            self.set_text_color(*DARK_GREY)
            self.cell(0, 8, "Write down new nouns, adjectives, and time markers you find or look up.", 0, 1, 'C')
            self.ln(5)
            
            self.set_font('DS', 'B', 12)
            self.set_text_color(*BLACK)
            col_w = CONTENT_W / 2
            self.cell(col_w, 10, "Romanian Word", 1, 0, 'C')
            self.cell(col_w, 10, "English Translation", 1, 1, 'C')
            
            self.set_draw_color(*GREY)
            for _ in range(21):
                self.cell(col_w, 10, "", 1, 0)
                self.cell(col_w, 10, "", 1, 1)

    def draw_divider(self, part_num, theme_name, verb_range):
        self.add_page()
        self.set_fill_color(245, 245, 245)
        self.rect(MARGIN, MARGIN, CONTENT_W, PAGE_H - 2*MARGIN, 'F')
        
        self.set_y(100)
        self.set_font('DS', 'B', 48)
        self.set_text_color(40, 40, 40)
        self.cell(0, 20, f"PART {part_num}", 0, 1, 'C')
        
        self.ln(20)
        self.set_font('DS', '', 24)
        self.cell(0, 15, theme_name, 0, 1, 'C')
        
        self.ln(10)
        self.set_font('DS', '', 16)
        self.cell(0, 10, f"(Verbs {verb_range})", 0, 1, 'C')

    def draw_verb_page(self, day_num, verb_info):
        self.add_page()
        verb, translation, present, past, future = verb_info
        
        self.set_font('DS', 'B', 16)
        self.set_text_color(*BLACK)
        self.cell(100, 10, f"DAY {day_num}/100", 0, 0, 'L')
        
        self.set_font('DS', '', 10)
        self.cell(0, 10, "DATE: ___/___/___", 0, 1, 'R')
        self.ln(5)
        
        self.set_font('DS', 'B', 14)
        self.cell(0, 10, f"TODAY'S VERB: {verb} — {translation}", 0, 1, 'R')
        self.ln(5)
        
        col1_w = 30
        col_w = (CONTENT_W - col1_w) / 3
        
        self.set_fill_color(*LIGHT_GREY)
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
            
        self.ln(10)
        
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
pdf.title_page()
pdf.intro_pages()
pdf.vocab_bank()

themes = [
    ("Survival Basics", "1-25"),
    ("Desires & Needs", "26-50"),
    ("Movement & Location", "51-75"),
    ("People & Actions", "76-100")
]

verb_idx = 0
for part_num in range(1, 5):
    theme_name, v_range = themes[part_num - 1]
    pdf.draw_divider(part_num, theme_name, v_range)
    
    for _ in range(25):
        if verb_idx < len(verbs_100):
            pdf.draw_verb_page(verb_idx + 1, verbs_100[verb_idx])
            verb_idx += 1

pdf.output("/workspace/one-verb-a-day/Romanian_Vol1_Survival_Basics.pdf")
