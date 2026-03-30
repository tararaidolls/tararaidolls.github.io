import sys
import json
import os
import qrcode
from fpdf import FPDF
from gtts import gTTS

sys.path.append("/workspace/one-verb-a-day/romanian")

# 1. EXTRACT 360 VERBS
with open("/workspace/one-verb-a-day/romanian/generate_verbs.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.split("class VerbPDF(FPDF):")[0]
lines = [l for l in text.split('\n') if not l.startswith('from ') and not l.startswith('import ')]
code = '\n'.join(lines)
loc = {}
exec(code, {}, loc)

all_verbs = []
for i in range(1, 13):
    key = f"MONTH{i}_VERBS"
    if key in loc:
        for v in loc[key]:
            # Convert to list to be consistent, v is either (ro, en) or (ro, en, pres, past, fut)
            all_verbs.append(list(v))

# 2. ADD 40 ADVANCED VERBS
extra_verbs = [
    ["a argumenta", "to argue"], ["a dovedi", "to prove"], ["a analiza", "to analyze"],
    ["a presupune", "to assume"], ["a se aștepta", "to expect"], ["a nega", "to deny"],
    ["a confirma", "to confirm"], ["a respinge", "to reject"], ["a ignora", "to ignore"],
    ["a asigura", "to ensure"], ["a proteja", "to protect"], ["a preveni", "to prevent"],
    ["a influența", "to influence"], ["a reacționa", "to react"], ["a provoca", "to provoke"],
    ["a încuraja", "to encourage"], ["a descuraja", "to discourage"], ["a inspira", "to inspire"],
    ["a dezamăgi", "to disappoint"], ["a regreta", "to regret"], ["a aprecia", "to appreciate"],
    ["a critica", "to criticize"], ["a ierta", "to forgive"], ["a pedepsi", "to punish"],
    ["a răsplăti", "to reward"], ["a compensa", "to compensate"], ["a sacrifica", "to sacrifice"],
    ["a renunța", "to give up"], ["a persevera", "to persevere"], ["a rezista", "to resist"],
    ["a insista", "to insist"], ["a se conforma", "to conform"], ["a se adapta", "to adapt"],
    ["a evolua", "to evolve"], ["a dezvolta", "to develop"], ["a stagna", "to stagnate"],
    ["a declina", "to decline"], ["a progresa", "to progress"], ["a îmbunătăți", "to improve"],
    ["a înrăutăți", "to worsen"]
]
all_verbs.extend(extra_verbs)

print(f"Total verbs ready: {len(all_verbs)}")

# 3. SET UP DIRECTORIES
base_dir = "/workspace/one-verb-a-day/romanian"
audio_dir = os.path.join(base_dir, "audio")
qr_dir = os.path.join(base_dir, "qr")
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(qr_dir, exist_ok=True)

# 4. GENERATE AUDIO & QR FOR 101-400
# We only generate missing ones to save time, but I'll just write the loop.
# Let's pre-generate them.
def generate_media(start_idx, end_idx):
    for i in range(start_idx, end_idx):
        verb = all_verbs[i]
        idx = i + 1
        ro_verb = verb[0]
        
        # Audio text
        if len(verb) == 5:
            text = f"{ro_verb}. {verb[2][0]}, {verb[2][1]}, {verb[2][2]}, {verb[2][3]}, {verb[2][4]}, {verb[2][5]}."
        else:
            text = f"{ro_verb}."
            
        f_norm = os.path.join(audio_dir, f"verb_{idx}.mp3")
        if not os.path.exists(f_norm):
            gTTS(text=text, lang="ro").save(f_norm)
            
        qr_file = os.path.join(qr_dir, f"verb_{idx}.png")
        if not os.path.exists(qr_file):
            qr = qrcode.QRCode(version=1, box_size=10, border=1)
            url = f"https://tararaidolls.github.io/romanian/one-verb-a-day/audio/verb_{idx}.mp3"
            qr.add_data(url)
            qr.make(fit=True)
            qr.make_image(fill_color="black", back_color="white").save(qr_file)

# 5. PDF CLASS
PAGE_W = 8.5 * 25.4
PAGE_H = 11 * 25.4
MARGIN = 0.5 * 25.4
CONTENT_W = PAGE_W - 2 * MARGIN

GREY = (221, 221, 221)
LIGHT_GREY = (245, 245, 245)
BLACK = (0, 0, 0)
DARK_GREY = (80, 80, 80)
TEAL = (40, 100, 100)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PRONOUNS = ["Eu", "Tu", "El/Ea", "Noi", "Voi", "Ei/Ele"]

class VolBook(FPDF):
    def __init__(self, vol_num, vol_title, verb_range):
        super().__init__('P', 'mm', (PAGE_W, PAGE_H))
        self.add_font('DS', '', FONT_PATH)
        self.add_font('DS', 'B', FONT_PATH_BOLD)
        self.set_auto_page_break(auto=True, margin=MARGIN)
        self.vol_num = vol_num
        self.vol_title = vol_title
        self.verb_range = verb_range

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
        self.cell(0, 15, f"VOLUME {self.vol_num}: {self.vol_title}", 0, 1, 'C')
        
        self.ln(10)
        self.set_font('DS', '', 14)
        self.set_text_color(*DARK_GREY)
        self.cell(0, 10, f"Verbs {self.verb_range}", 0, 1, 'C')
        
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
            f"Welcome to Volume {self.vol_num} of the Romanian Verb Challenge!\n"
            "Verbs are the engine of any language. Without them, you can't build a single sentence. "
            "This workbook is designed to help you master essential Romanian verbs.\n\n"
            "Here is your daily routine:\n"
            "1. Conjugate the Verb: The tables are empty. Fill them in yourself to test your memory!\n"
            "2. Listen to the Audio: Scan the QR code to hear the pronunciation.\n"
            "3. Write Your Own (The Magic Step!): This is where real learning happens. "
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
            "This is your foundation. Master these, and you can survive in Romania.\n\n"
            "VOLUME 2: Daily Life & Routine (Verbs 101-200)\n"
            "Once you can survive, it's time to talk about your day! Waking up, eating, cleaning, sleeping.\n\n"
            "VOLUME 3: Work, Travel & Community (Verbs 201-300)\n"
            "Verbs you need to commute, work in an office, travel, buy things, and interact with the world.\n\n"
            "VOLUME 4: Thoughts, Emotions & Abstract (Verbs 301-400)\n"
            "The final boss. Express deep feelings, argue opinions, remember the past, and explain complex ideas."
        )
        self.multi_cell(0, 7, journey)

    def question_builder(self):
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
            "Challenge: Try starting some of your daily sentences with these question words!"
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
        verb, translation = verb_info[0], verb_info[1]
        
        # Top Row
        y_top = self.get_y()
        self.set_font('DS', 'B', 16)
        self.set_text_color(*BLACK)
        self.set_xy(MARGIN, y_top + 10)
        self.cell(40, 10, f"DAY {day_num}/400", 0, 0, 'L')
        
        self.set_font('DS', '', 10)
        self.set_xy(PAGE_W - MARGIN - 40, y_top + 10)
        self.cell(40, 10, "DATE: ___/___/___", 0, 0, 'R')
        
        # QR Code Center
        qr_w = 16
        qr_x = MARGIN + (CONTENT_W - qr_w) / 2
        qr_path = f"/workspace/one-verb-a-day/romanian/qr/verb_{day_num}.png"
        if os.path.exists(qr_path):
            self.image(qr_path, x=qr_x, y=y_top, w=qr_w)
            
        self.set_y(y_top + qr_w)
        self.set_font('DS', '', 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "Scan to listen", 0, 1, 'C')
        
        self.ln(2)
        
        self.set_font('DS', 'B', 14)
        self.set_text_color(*BLACK)
        self.cell(0, 10, f"TODAY'S VERB: {verb} — {translation}", 0, 1, 'C')
        self.ln(4)
        
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
            self.cell(col_w, 8, "", 1, 0, 'L')
            self.cell(col_w, 8, "", 1, 0, 'L')
            self.cell(col_w, 8, "", 1, 1, 'L')
            
        self.ln(6)
        
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
            
            self.ln(line_spacing * 1.4)

def build_volume(vol_num, vol_title, start_idx, end_idx, themes):
    print(f"Building Volume {vol_num}...")
    generate_media(start_idx, end_idx)
    
    pdf = VolBook(vol_num, vol_title, f"{start_idx+1}-{end_idx}")
    pdf.title_page()
    pdf.intro_pages()
    pdf.question_builder()
    pdf.vocab_bank()
    
    chunk_size = 25
    part_num = 1
    for i in range(start_idx, end_idx, chunk_size):
        theme_name = themes[part_num - 1]
        v_range = f"{i+1}-{i+chunk_size}"
        pdf.draw_divider(part_num, theme_name, v_range)
        
        for j in range(i, i + chunk_size):
            if j < len(all_verbs):
                pdf.draw_verb_page(j + 1, all_verbs[j])
                
        part_num += 1
        
    out_name = f"Romanian_Vol{vol_num}_{vol_title.replace(' ', '_').replace('&', 'and')}.pdf"
    out_path = os.path.join("/workspace/one-verb-a-day", out_name)
    pdf.output(out_path)
    return out_path

# Themes
themes_vol2 = ["Morning & Schedule", "Food & Cooking", "Home & Chores", "Body & Health"]
themes_vol3 = ["Money & Shopping", "Work & Office", "Travel & Commute", "Social Interactions"]
themes_vol4 = ["Mind & Opinions", "Feelings & Expressions", "Memory & Time", "Complex Actions"]

# Generate Volumes
vol2_pdf = build_volume(2, "Daily Life & Routine", 100, 200, themes_vol2)
vol3_pdf = build_volume(3, "Work, Travel & Community", 200, 300, themes_vol3)
vol4_pdf = build_volume(4, "Thoughts, Emotions & Abstract", 300, 400, themes_vol4)

print("Done generating PDFs!")
