#!/usr/bin/env python3
"""Generate KDP interior PDF: ONE VERB A DAY - 365 Days of Romanian Verb Mastery."""

#from dummy_fpdf import FPDF
import os

# --- Constants ---
PAGE_W = 8.5 * 25.4  # mm
PAGE_H = 11 * 25.4   # mm
MARGIN = 0.5 * 25.4   # 12.7 mm
CONTENT_W = PAGE_W - 2 * MARGIN
GREY = (221, 221, 221)
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
DARK_GREY = (80, 80, 80)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PRONOUNS = ["Eu", "Tu", "El/Ea", "Noi", "Voi", "Ei/Ele"]
TENSES = ["Prezent", "Perfect Compus", "Viitor"]

MONTH_THEMES = {
    1: "Daily Life",
    2: "Movement & Social",
    3: "Emotions & Thinking",
    4: "Home & Routine",
    5: "Work & Study",
    6: "Nature & Weather",
    7: "Health & Body",
    8: "Food & Shopping",
    9: "Technology & Modern Life",
    10: "Travel & Culture",
    11: "Advanced Actions",
    12: "Abstract & Mastery",
}

# Month 1 verbs with full conjugations (pre-filled)
MONTH1_VERBS = [
    ("a fi", "to be",
     ["sunt", "ești", "este", "suntem", "sunteți", "sunt"],
     ["am fost", "ai fost", "a fost", "am fost", "ați fost", "au fost"],
     ["voi fi", "vei fi", "va fi", "vom fi", "veți fi", "vor fi"]),
    ("a avea", "to have",
     ["am", "ai", "are", "avem", "aveți", "au"],
     ["am avut", "ai avut", "a avut", "am avut", "ați avut", "au avut"],
     ["voi avea", "vei avea", "va avea", "vom avea", "veți avea", "vor avea"]),
    ("a merge", "to go",
     ["merg", "mergi", "merge", "mergem", "mergeți", "merg"],
     ["am mers", "ai mers", "a mers", "am mers", "ați mers", "au mers"],
     ["voi merge", "vei merge", "va merge", "vom merge", "veți merge", "vor merge"]),
    ("a veni", "to come",
     ["vin", "vii", "vine", "venim", "veniți", "vin"],
     ["am venit", "ai venit", "a venit", "am venit", "ați venit", "au venit"],
     ["voi veni", "vei veni", "va veni", "vom veni", "veți veni", "vor veni"]),
    ("a face", "to do/make",
     ["fac", "faci", "face", "facem", "faceți", "fac"],
     ["am făcut", "ai făcut", "a făcut", "am făcut", "ați făcut", "au făcut"],
     ["voi face", "vei face", "va face", "vom face", "veți face", "vor face"]),
    ("a mânca", "to eat",
     ["mănânc", "mănânci", "mănâncă", "mâncăm", "mâncați", "mănâncă"],
     ["am mâncat", "ai mâncat", "a mâncat", "am mâncat", "ați mâncat", "au mâncat"],
     ["voi mânca", "vei mânca", "va mânca", "vom mânca", "veți mânca", "vor mânca"]),
    ("a bea", "to drink",
     ["beau", "bei", "bea", "bem", "beți", "beau"],
     ["am băut", "ai băut", "a băut", "am băut", "ați băut", "au băut"],
     ["voi bea", "vei bea", "va bea", "vom bea", "veți bea", "vor bea"]),
    ("a dormi", "to sleep",
     ["dorm", "dormi", "doarme", "dormim", "dormiți", "dorm"],
     ["am dormit", "ai dormit", "a dormit", "am dormit", "ați dormit", "au dormit"],
     ["voi dormi", "vei dormi", "va dormi", "vom dormi", "veți dormi", "vor dormi"]),
    ("a se trezi", "to wake up",
     ["mă trezesc", "te trezești", "se trezește", "ne trezim", "vă treziți", "se trezesc"],
     ["m-am trezit", "te-ai trezit", "s-a trezit", "ne-am trezit", "v-ați trezit", "s-au trezit"],
     ["mă voi trezi", "te vei trezi", "se va trezi", "ne vom trezi", "vă veți trezi", "se vor trezi"]),
    ("a lucra", "to work",
     ["lucrez", "lucrezi", "lucrează", "lucrăm", "lucrați", "lucrează"],
     ["am lucrat", "ai lucrat", "a lucrat", "am lucrat", "ați lucrat", "au lucrat"],
     ["voi lucra", "vei lucra", "va lucra", "vom lucra", "veți lucra", "vor lucra"]),
    ("a cumpăra", "to buy",
     ["cumpăr", "cumperi", "cumpără", "cumpărăm", "cumpărați", "cumpără"],
     ["am cumpărat", "ai cumpărat", "a cumpărat", "am cumpărat", "ați cumpărat", "au cumpărat"],
     ["voi cumpăra", "vei cumpăra", "va cumpăra", "vom cumpăra", "veți cumpăra", "vor cumpăra"]),
    ("a găti", "to cook",
     ["gătesc", "gătești", "gătește", "gătim", "gătiți", "gătesc"],
     ["am gătit", "ai gătit", "a gătit", "am gătit", "ați gătit", "au gătit"],
     ["voi găti", "vei găti", "va găti", "vom găti", "veți găti", "vor găti"]),
    ("a curăța", "to clean",
     ["curăț", "curăți", "curăță", "curățăm", "curățați", "curăță"],
     ["am curățat", "ai curățat", "a curățat", "am curățat", "ați curățat", "au curățat"],
     ["voi curăța", "vei curăța", "va curăța", "vom curăța", "veți curăța", "vor curăța"]),
    ("a citi", "to read",
     ["citesc", "citești", "citește", "citim", "citiți", "citesc"],
     ["am citit", "ai citit", "a citit", "am citit", "ați citit", "au citit"],
     ["voi citi", "vei citi", "va citi", "vom citi", "veți citi", "vor citi"]),
    ("a scrie", "to write",
     ["scriu", "scrii", "scrie", "scriem", "scrieți", "scriu"],
     ["am scris", "ai scris", "a scris", "am scris", "ați scris", "au scris"],
     ["voi scrie", "vei scrie", "va scrie", "vom scrie", "veți scrie", "vor scrie"]),
    ("a vedea", "to see",
     ["văd", "vezi", "vede", "vedem", "vedeți", "văd"],
     ["am văzut", "ai văzut", "a văzut", "am văzut", "ați văzut", "au văzut"],
     ["voi vedea", "vei vedea", "va vedea", "vom vedea", "veți vedea", "vor vedea"]),
    ("a auzi", "to hear",
     ["aud", "auzi", "aude", "auzim", "auziți", "aud"],
     ["am auzit", "ai auzit", "a auzit", "am auzit", "ați auzit", "au auzit"],
     ["voi auzi", "vei auzi", "va auzi", "vom auzi", "veți auzi", "vor auzi"]),
    ("a vorbi", "to speak/talk",
     ["vorbesc", "vorbești", "vorbește", "vorbim", "vorbiți", "vorbesc"],
     ["am vorbit", "ai vorbit", "a vorbit", "am vorbit", "ați vorbit", "au vorbit"],
     ["voi vorbi", "vei vorbi", "va vorbi", "vom vorbi", "veți vorbi", "vor vorbi"]),
    ("a asculta", "to listen",
     ["ascult", "asculți", "ascultă", "ascultăm", "ascultați", "ascultă"],
     ["am ascultat", "ai ascultat", "a ascultat", "am ascultat", "ați ascultat", "au ascultat"],
     ["voi asculta", "vei asculta", "va asculta", "vom asculta", "veți asculta", "vor asculta"]),
    ("a da", "to give",
     ["dau", "dai", "dă", "dăm", "dați", "dau"],
     ["am dat", "ai dat", "a dat", "am dat", "ați dat", "au dat"],
     ["voi da", "vei da", "va da", "vom da", "veți da", "vor da"]),
    ("a lua", "to take",
     ["iau", "iei", "ia", "luăm", "luați", "iau"],
     ["am luat", "ai luat", "a luat", "am luat", "ați luat", "au luat"],
     ["voi lua", "vei lua", "va lua", "vom lua", "veți lua", "vor lua"]),
    ("a ști", "to know",
     ["știu", "știi", "știe", "știm", "știți", "știu"],
     ["am știut", "ai știut", "a știut", "am știut", "ați știut", "au știut"],
     ["voi ști", "vei ști", "va ști", "vom ști", "veți ști", "vor ști"]),
    ("a putea", "to be able",
     ["pot", "poți", "poate", "putem", "puteți", "pot"],
     ["am putut", "ai putut", "a putut", "am putut", "ați putut", "au putut"],
     ["voi putea", "vei putea", "va putea", "vom putea", "veți putea", "vor putea"]),
    ("a vrea", "to want",
     ["vreau", "vrei", "vrea", "vrem", "vreți", "vor"],
     ["am vrut", "ai vrut", "a vrut", "am vrut", "ați vrut", "au vrut"],
     ["voi vrea", "vei vrea", "va vrea", "vom vrea", "veți vrea", "vor vrea"]),
    ("a trebui", "to must/need",
     ["trebuie", "trebuie", "trebuie", "trebuie", "trebuie", "trebuie"],
     ["a trebuit", "a trebuit", "a trebuit", "a trebuit", "a trebuit", "a trebuit"],
     ["va trebui", "va trebui", "va trebui", "va trebui", "va trebui", "va trebui"]),
    ("a plăcea", "to like",
     ["îmi place", "îți place", "îi place", "ne place", "vă place", "le place"],
     ["mi-a plăcut", "ți-a plăcut", "i-a plăcut", "ne-a plăcut", "v-a plăcut", "le-a plăcut"],
     ["îmi va plăcea", "îți va plăcea", "îi va plăcea", "ne va plăcea", "vă va plăcea", "le va plăcea"]),
    ("a iubi", "to love",
     ["iubesc", "iubești", "iubește", "iubim", "iubiți", "iubesc"],
     ["am iubit", "ai iubit", "a iubit", "am iubit", "ați iubit", "au iubit"],
     ["voi iubi", "vei iubi", "va iubi", "vom iubi", "veți iubi", "vor iubi"]),
    ("a se spăla", "to wash oneself",
     ["mă spăl", "te speli", "se spală", "ne spălăm", "vă spălați", "se spală"],
     ["m-am spălat", "te-ai spălat", "s-a spălat", "ne-am spălat", "v-ați spălat", "s-au spălat"],
     ["mă voi spăla", "te vei spăla", "se va spăla", "ne vom spăla", "vă veți spăla", "se vor spăla"]),
    ("a pleca", "to leave",
     ["plec", "pleci", "pleacă", "plecăm", "plecați", "pleacă"],
     ["am plecat", "ai plecat", "a plecat", "am plecat", "ați plecat", "au plecat"],
     ["voi pleca", "vei pleca", "va pleca", "vom pleca", "veți pleca", "vor pleca"]),
    ("a rămâne", "to stay",
     ["rămân", "rămâi", "rămâne", "rămânem", "rămâneți", "rămân"],
     ["am rămas", "ai rămas", "a rămas", "am rămas", "ați rămas", "au rămas"],
     ["voi rămâne", "vei rămâne", "va rămâne", "vom rămâne", "veți rămâne", "vor rămâne"]),
]

# Months 2-12: verb name + meaning only (blank conjugation tables)
MONTH2_VERBS = [
    ("a ajunge", "to arrive"), ("a călători", "to travel"), ("a conduce", "to drive"),
    ("a alerga", "to run"), ("a înota", "to swim"), ("a zbura", "to fly"),
    ("a dansa", "to dance"), ("a cânta", "to sing"), ("a juca", "to play"),
    ("a desena", "to draw"), ("a fotografia", "to photograph"), ("a suna", "to call"),
    ("a trimite", "to send"), ("a primi", "to receive"), ("a invita", "to invite"),
    ("a ajuta", "to help"), ("a mulțumi", "to thank"), ("a cere", "to ask for"),
    ("a răspunde", "to answer"), ("a explica", "to explain"), ("a înțelege", "to understand"),
    ("a crede", "to believe"), ("a spune", "to say/tell"), ("a întâlni", "to meet"),
    ("a saluta", "to greet"), ("a îmbrățișa", "to hug"), ("a săruta", "to kiss"),
    ("a râde", "to laugh"), ("a plânge", "to cry"), ("a zâmbi", "to smile"),
]

MONTH3_VERBS = [
    ("a gândi", "to think"), ("a simți", "to feel"), ("a visa", "to dream"),
    ("a uita", "to forget"), ("a aminti", "to remember"), ("a spera", "to hope"),
    ("a dori", "to wish"), ("a ura", "to hate"), ("a suferi", "to suffer"),
    ("a se bucura", "to rejoice"), ("a se teme", "to fear"), ("a se supăra", "to be upset"),
    ("a se relaxa", "to relax"), ("a se plictisi", "to be bored"), ("a se mira", "to wonder"),
    ("a admira", "to admire"), ("a aprecia", "to appreciate"), ("a respecta", "to respect"),
    ("a ignora", "to ignore"), ("a prefera", "to prefer"), ("a accepta", "to accept"),
    ("a refuza", "to refuse"), ("a regreta", "to regret"), ("a se îndoi", "to doubt"),
    ("a compara", "to compare"), ("a judeca", "to judge"), ("a decide", "to decide"),
    ("a alege", "to choose"), ("a se concentra", "to concentrate"), ("a medita", "to meditate"),
]

MONTH4_VERBS = [
    ("a locui", "to live/reside"), ("a se muta", "to move house"), ("a deschide", "to open"),
    ("a închide", "to close"), ("a aprinde", "to turn on/light"), ("a stinge", "to turn off"),
    ("a spăla", "to wash"), ("a călca", "to iron"), ("a coase", "to sew"),
    ("a repara", "to repair"), ("a construi", "to build"), ("a vopsi", "to paint"),
    ("a mătura", "to sweep"), ("a aspira", "to vacuum"), ("a aranja", "to arrange"),
    ("a decora", "to decorate"), ("a tăia", "to cut"), ("a lipi", "to glue"),
    ("a încuia", "to lock"), ("a descuia", "to unlock"), ("a suna la ușă", "to ring doorbell"),
    ("a primi oaspeți", "to receive guests"), ("a se îmbrăca", "to get dressed"),
    ("a se dezbrăca", "to undress"), ("a se pieptăna", "to comb hair"),
    ("a se bărbieri", "to shave"), ("a se machina", "to put on makeup"),
    ("a se uita", "to look/watch"), ("a se odihni", "to rest"), ("a se culca", "to go to bed"),
]

MONTH5_VERBS = [
    ("a studia", "to study"), ("a învăța", "to learn"), ("a preda", "to teach"),
    ("a cerceta", "to research"), ("a analiza", "to analyze"), ("a prezenta", "to present"),
    ("a planifica", "to plan"), ("a organiza", "to organize"), ("a programa", "to schedule"),
    ("a colabora", "to collaborate"), ("a comunica", "to communicate"), ("a negocia", "to negotiate"),
    ("a semna", "to sign"), ("a tipări", "to print"), ("a copia", "to copy"),
    ("a șterge", "to delete/erase"), ("a salva", "to save"), ("a verifica", "to verify"),
    ("a corecta", "to correct"), ("a evalua", "to evaluate"), ("a promova", "to promote"),
    ("a demisiona", "to resign"), ("a angaja", "to hire"), ("a concedia", "to fire"),
    ("a câștiga", "to earn/win"), ("a cheltui", "to spend"), ("a economisi", "to save money"),
    ("a investi", "to invest"), ("a administra", "to manage"), ("a reuși", "to succeed"),
]

MONTH6_VERBS = [
    ("a ploua", "to rain"), ("a ninge", "to snow"), ("a sufla", "to blow"),
    ("a străluci", "to shine"), ("a crește", "to grow"), ("a înflori", "to bloom"),
    ("a planta", "to plant"), ("a uda", "to water"), ("a recolta", "to harvest"),
    ("a pescui", "to fish"), ("a vâna", "to hunt"), ("a explora", "to explore"),
    ("a escalada", "to climb"), ("a naviga", "to navigate/sail"), ("a campa", "to camp"),
    ("a observa", "to observe"), ("a fotografía", "to photograph"), ("a colecta", "to collect"),
    ("a proteja", "to protect"), ("a polua", "to pollute"), ("a recicla", "to recycle"),
    ("a se bronza", "to sunbathe"), ("a se scufunda", "to dive"), ("a patina", "to skate"),
    ("a schia", "to ski"), ("a se plimba", "to take a walk"), ("a hrăni", "to feed"),
    ("a îngriji", "to care for"), ("a semăna", "to sow"), ("a usca", "to dry"),
]

MONTH7_VERBS = [
    ("a respira", "to breathe"), ("a tușí", "to cough"), ("a strănuta", "to sneeze"),
    ("a transpira", "to sweat"), ("a tremura", "to tremble"), ("a leșina", "to faint"),
    ("a vindeca", "to heal"), ("a consulta", "to consult"), ("a examina", "to examine"),
    ("a prescrie", "to prescribe"), ("a opera", "to operate"), ("a bandaja", "to bandage"),
    ("a injecta", "to inject"), ("a se antena", "to exercise"), ("a alerga", "to jog"),
    ("a se întinde", "to stretch"), ("a ridica", "to lift"), ("a împinge", "to push"),
    ("a trage", "to pull"), ("a se apleca", "to bend"), ("a sări", "to jump"),
    ("a se ghemui", "to squat"), ("a se hrăni sănătos", "to eat healthy"),
    ("a slăbi", "to lose weight"), ("a se îngrășa", "to gain weight"),
    ("a dormi bine", "to sleep well"), ("a medita", "to meditate"),
    ("a se calma", "to calm down"), ("a se recupera", "to recover"),
    ("a preveni", "to prevent"),
]

MONTH8_VERBS = [
    ("a comanda", "to order"), ("a servi", "to serve"), ("a degusta", "to taste"),
    ("a amesteca", "to mix"), ("a fierbe", "to boil"), ("a prăji", "to fry"),
    ("a coace", "to bake"), ("a grătar", "to grill"), ("a condimenta", "to season"),
    ("a toca", "to chop"), ("a rădea", "to grate"), ("a stoarce", "to squeeze"),
    ("a conserva", "to preserve"), ("a congela", "to freeze"), ("a dezgheța", "to thaw"),
    ("a cântări", "to weigh"), ("a măsura", "to measure"), ("a negocia prețul", "to haggle"),
    ("a plăti", "to pay"), ("a returna", "to return"), ("a schimba", "to exchange"),
    ("a încerca", "to try on"), ("a alege", "to select"), ("a compara prețuri", "to compare prices"),
    ("a face cumpărături", "to go shopping"), ("a livra", "to deliver"),
    ("a împacheta", "to wrap"), ("a despacheta", "to unwrap"),
    ("a garanta", "to guarantee"), ("a recomanda", "to recommend"),
]

MONTH9_VERBS = [
    ("a conecta", "to connect"), ("a deconecta", "to disconnect"), ("a descărca", "to download"),
    ("a încărca", "to upload/charge"), ("a instala", "to install"), ("a actualiza", "to update"),
    ("a programa", "to program"), ("a naviga online", "to browse online"),
    ("a căuta", "to search"), ("a posta", "to post"), ("a distribui", "to share"),
    ("a comenta", "to comment"), ("a aprecia online", "to like online"),
    ("a urmări", "to follow"), ("a bloca", "to block"), ("a raporta", "to report"),
    ("a cripta", "to encrypt"), ("a hackui", "to hack"), ("a scana", "to scan"),
    ("a imprima", "to print"), ("a fotocopia", "to photocopy"),
    ("a filma", "to film/record"), ("a edita", "to edit"), ("a transmite", "to stream"),
    ("a podcast", "to podcast"), ("a automatiza", "to automate"),
    ("a sincroniza", "to sync"), ("a salva backup", "to backup"),
    ("a restaura", "to restore"), ("a depana", "to troubleshoot"),
]

MONTH10_VERBS = [
    ("a vizita", "to visit"), ("a rezerva", "to book/reserve"), ("a decola", "to take off"),
    ("a ateriza", "to land"), ("a îmbarca", "to board"), ("a debarca", "to disembark"),
    ("a cazа", "to accommodate"), ("a ghida", "to guide"), ("a traduce", "to translate"),
    ("a interpreta", "to interpret"), ("a degusta vin", "to taste wine"),
    ("a dansa tradițional", "to traditional dance"), ("a asista", "to attend"),
    ("a participa", "to participate"), ("a celebra", "to celebrate"),
    ("a sărbători", "to feast"), ("a comemora", "to commemorate"),
    ("a documenta", "to document"), ("a experimenta", "to experience"),
    ("a descoperi", "to discover"), ("a naviga cu barca", "to sail"),
    ("a face autostopul", "to hitchhike"), ("a se adapta", "to adapt"),
    ("a respecta cultura", "to respect culture"), ("a învăța limbi", "to learn languages"),
    ("a se orienta", "to orient oneself"), ("a face poze", "to take photos"),
    ("a negocia", "to bargain"), ("a schimba valută", "to exchange currency"),
    ("a se întoarce", "to return home"),
]

MONTH11_VERBS = [
    ("a influența", "to influence"), ("a motiva", "to motivate"), ("a inspira", "to inspire"),
    ("a convinge", "to convince"), ("a demonstra", "to demonstrate"), ("a argumenta", "to argue"),
    ("a contrazice", "to contradict"), ("a reconcilia", "to reconcile"),
    ("a media", "to mediate"), ("a arbitra", "to arbitrate"), ("a susține", "to support"),
    ("a abandona", "to abandon"), ("a persevera", "to persevere"), ("a sacrifica", "to sacrifice"),
    ("a risca", "to risk"), ("a inova", "to innovate"), ("a transforma", "to transform"),
    ("a revoluționa", "to revolutionize"), ("a perfecționa", "to perfect"),
    ("a optimiza", "to optimize"), ("a simplifica", "to simplify"),
    ("a complica", "to complicate"), ("a accelera", "to accelerate"),
    ("a întârzia", "to delay"), ("a anticipa", "to anticipate"), ("a previziona", "to forecast"),
    ("a estima", "to estimate"), ("a calcula", "to calculate"),
    ("a implementa", "to implement"), ("a finaliza", "to finalize"),
]

MONTH12_VERBS = [
    ("a exista", "to exist"), ("a deveni", "to become"), ("a aparține", "to belong"),
    ("a depinde", "to depend"), ("a însemna", "to mean"), ("a reprezenta", "to represent"),
    ("a simboliza", "to symbolize"), ("a reflecta", "to reflect"), ("a contempla", "to contemplate"),
    ("a filozofa", "to philosophize"), ("a crea", "to create"), ("a imagina", "to imagine"),
    ("a inventa", "to invent"), ("a evolua", "to evolve"), ("a progresa", "to progress"),
    ("a transcende", "to transcend"), ("a unifica", "to unify"), ("a armoniza", "to harmonize"),
    ("a echilibra", "to balance"), ("a integra", "to integrate"),
    ("a sintetiza", "to synthesize"), ("a abstractiza", "to abstract"),
    ("a generaliza", "to generalize"), ("a specializa", "to specialize"),
    ("a manifesta", "to manifest"), ("a realiza", "to realize/achieve"),
    ("a împlini", "to fulfill"), ("a consacra", "to consecrate"),
    ("a triumfa", "to triumph"), ("a maestru", "to master"),
]

ALL_MONTHS_BLANK = [
    MONTH2_VERBS, MONTH3_VERBS, MONTH4_VERBS, MONTH5_VERBS,
    MONTH6_VERBS, MONTH7_VERBS, MONTH8_VERBS, MONTH9_VERBS,
    MONTH10_VERBS, MONTH11_VERBS, MONTH12_VERBS,
]


def get_all_verbs():
    """Build list of (day, month, verb, meaning, conjugations_or_None)."""
    verbs = []
    day = 1
    # Month 1 - pre-filled
    for v in MONTH1_VERBS:
        verbs.append((day, 1, v[0], v[1], v[2], v[3], v[4]))
        day += 1
    # Months 2-12 - blank
    for mi, month_verbs in enumerate(ALL_MONTHS_BLANK, start=2):
        for vt in month_verbs:
            if day > 365:
                break
            verbs.append((day, mi, vt[0], vt[1], None, None, None))
            day += 1
    # Fill remaining days if any
    extra_verbs = [
        ("a continua", "to continue"), ("a termina", "to finish"),
        ("a începe", "to begin"), ("a repeta", "to repeat"), ("a practica", "to practice"),
    ]
    ei = 0
    while day <= 365:
        v = extra_verbs[ei % len(extra_verbs)]
        verbs.append((day, 12, v[0], v[1], None, None, None))
        day += 1
        ei += 1
    return verbs


class VerbPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format=(PAGE_W, PAGE_H))
        self.set_auto_page_break(auto=False)
        # Add Unicode fonts
        self.add_font("DS", "", FONT_PATH, uni=True)
        self.add_font("DS", "B", FONT_PATH_BOLD, uni=True)

    def _set_font(self, style="", size=10):
        self.set_font("DS", style, size)

    def _grey_line(self, x1, y1, x2, y2):
        self.set_draw_color(*GREY)
        self.line(x1, y1, x2, y2)

    def _centered_text(self, y, text, size=12, bold=False):
        self._set_font("B" if bold else "", size)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W, size * 0.5, text, align='C')

    def add_title_page(self):
        self.add_page()
        y = 60
        self._centered_text(y, "ONE VERB A DAY", 28, bold=True)
        y += 18
        self._centered_text(y, "365 Days of Romanian Verb Mastery", 14)
        y += 30
        self._set_font("", 10)
        self.set_draw_color(*GREY)
        self.set_xy(MARGIN + 30, y)
        self.cell(30, 8, "Name: ")
        self.cell(100, 8, "_" * 50)
        y += 15
        self.set_xy(MARGIN + 30, y)
        self.cell(30, 8, "Start Date: ")
        self.cell(100, 8, "_" * 50)
        y += 30
        self._centered_text(y, "Your journey to fluency begins now.", 11)

    def add_how_to_use(self):
        self.add_page()
        y = MARGIN
        self._centered_text(y, "How to Use This Book", 16, bold=True)
        y += 14
        self._set_font("", 9)
        instructions = [
            "Welcome to ONE VERB A DAY! This workbook is designed to help you master",
            "Romanian verbs through daily, structured practice over 365 days.",
            "",
            "DAILY ROUTINE (15-20 minutes):",
            "",
            "1. READ the verb of the day and its English meaning.",
            "2. STUDY the conjugation table. For Month 1, conjugations are pre-filled",
            "   as a reference. From Month 2 onward, fill in the table yourself.",
            "3. WRITE six sentences using the verb in different contexts:",
            "   - Present tense (about today)",
            "   - Past tense (about yesterday)",
            "   - Future tense (about tomorrow)",
            "   - Negative form (what you don't do)",
            "   - Question form (ask someone)",
            "   - Personal (about your own life)",
            "4. EXPLORE related words and idioms in the bonus section.",
            "5. LOG your progress: time spent, difficulty, and confidence level.",
            "",
            "TIPS FOR SUCCESS:",
            "- Be consistent. Even 10 minutes daily beats 2 hours once a week.",
            "- Say conjugations OUT LOUD. Your mouth needs practice too.",
            "- Use the progress tracker to visualize your streak.",
            "- Review verbs marked 'Review again' at the end of each week.",
            "- Don't worry about perfection. Mistakes are part of learning!",
            "",
            "MONTHLY THEMES help you build vocabulary in related areas,",
            "making it easier to form natural sentences.",
            "",
            "By Day 365, you will know the most important Romanian verbs",
            "and be able to express yourself confidently in any tense.",
        ]
        for line in instructions:
            self.set_xy(MARGIN + 5, y)
            self.cell(CONTENT_W - 10, 6, line)
            y += 6

    def add_pronoun_reference(self):
        self.add_page()
        y = MARGIN
        self._centered_text(y, "Romanian Pronoun Reference", 16, bold=True)
        y += 16
        pronouns_data = [
            ("Eu", "I", "1st person singular"),
            ("Tu", "You", "2nd person singular (informal)"),
            ("El", "He", "3rd person singular masculine"),
            ("Ea", "She", "3rd person singular feminine"),
            ("Noi", "We", "1st person plural"),
            ("Voi", "You", "2nd person plural / formal singular"),
            ("Ei", "They", "3rd person plural masculine"),
            ("Ele", "They", "3rd person plural feminine"),
        ]
        # Table header
        self._set_font("B", 10)
        self.set_xy(MARGIN + 10, y)
        self.cell(35, 8, "Pronume", border=1, align='C')
        self.cell(35, 8, "English", border=1, align='C')
        self.cell(90, 8, "Description", border=1, align='C')
        y += 8
        self._set_font("", 9)
        for rom, eng, desc in pronouns_data:
            self.set_xy(MARGIN + 10, y)
            self.cell(35, 8, rom, border=1, align='C')
            self.cell(35, 8, eng, border=1, align='C')
            self.cell(90, 8, desc, border=1)
            y += 8
        y += 15
        self._centered_text(y, "Note on El/Ea and Ei/Ele", 12, bold=True)
        y += 10
        self._set_font("", 9)
        notes = [
            "In conjugation tables, El/Ea share the same verb form (3rd person singular).",
            "Similarly, Ei/Ele share the same form (3rd person plural).",
            "This is why you'll see them grouped together throughout this book.",
        ]
        for n in notes:
            self.set_xy(MARGIN + 10, y)
            self.cell(CONTENT_W - 20, 6, n)
            y += 7

    def add_tense_reference(self):
        self.add_page()
        y = MARGIN
        self._centered_text(y, "Romanian Tense Reference", 16, bold=True)
        y += 16
        tenses_info = [
            ("PREZENT (Present Tense)", "Describes actions happening now or habitually.",
             "Eu merg la școală. (I go to school.)"),
            ("PERFECT COMPUS (Past Tense)", "Describes completed past actions. Formed with auxiliary 'a avea' + past participle.",
             "Eu am mers la școală. (I went to school.)"),
            ("VIITOR (Future Tense)", "Describes future actions. Formed with 'voi/vei/va/vom/veți/vor' + infinitive.",
             "Eu voi merge la școală. (I will go to school.)"),
        ]
        for title, desc, example in tenses_info:
            self._set_font("B", 11)
            self.set_xy(MARGIN + 5, y)
            self.cell(CONTENT_W - 10, 7, title)
            y += 8
            self._set_font("", 9)
            self.set_xy(MARGIN + 10, y)
            self.cell(CONTENT_W - 20, 6, desc)
            y += 7
            self._set_font("", 9)
            self.set_xy(MARGIN + 10, y)
            self.cell(CONTENT_W - 20, 6, f"Example: {example}")
            y += 12

        y += 5
        self._centered_text(y, "Future Tense Auxiliaries", 12, bold=True)
        y += 10
        aux = [("Eu", "voi"), ("Tu", "vei"), ("El/Ea", "va"),
               ("Noi", "vom"), ("Voi", "veți"), ("Ei/Ele", "vor")]
        self._set_font("B", 10)
        self.set_xy(MARGIN + 40, y)
        self.cell(40, 7, "Pronoun", border=1, align='C')
        self.cell(40, 7, "Auxiliary", border=1, align='C')
        y += 7
        self._set_font("", 9)
        for pron, a in aux:
            self.set_xy(MARGIN + 40, y)
            self.cell(40, 7, pron, border=1, align='C')
            self.cell(40, 7, a, border=1, align='C')
            y += 7

    def add_conjugation_groups(self):
        self.add_page()
        y = MARGIN
        self._centered_text(y, "4 Conjugation Groups in Romanian", 16, bold=True)
        y += 16
        groups = [
            ("Group I: -a verbs", "a lucra (to work), a cânta (to sing), a da (to give)",
             "Most common group. Present tense endings: -ez, -ezi, -ează, -ăm, -ați, -ează (or -Ø, -i, -ă, -ăm, -ați, -ă)"),
            ("Group II: -ea verbs", "a vedea (to see), a putea (to be able), a plăcea (to like)",
             "Present endings vary. Often: -Ø, -i, -e, -em, -eți, -Ø"),
            ("Group III: -e verbs", "a merge (to go), a face (to do), a scrie (to write)",
             "Present endings: -Ø, -i, -e, -em, -eți, -Ø. Many irregular verbs in this group."),
            ("Group IV: -i / -î verbs", "a dormi (to sleep), a veni (to come), a coborî (to descend)",
             "Present endings: -Ø/-esc, -i/-ești, -e/-ește, -im, -iți, -Ø/-esc"),
        ]
        for title, examples, pattern in groups:
            self._set_font("B", 11)
            self.set_xy(MARGIN + 5, y)
            self.cell(CONTENT_W - 10, 7, title)
            y += 8
            self._set_font("", 9)
            self.set_xy(MARGIN + 10, y)
            self.cell(CONTENT_W - 20, 6, f"Examples: {examples}")
            y += 7
            self.set_xy(MARGIN + 10, y)
            self.multi_cell(CONTENT_W - 20, 5, f"Pattern: {pattern}")
            y += 14

    def add_goal_page(self):
        self.add_page()
        y = MARGIN + 20
        self._centered_text(y, "Your Goal", 18, bold=True)
        y += 20
        self._centered_text(y, "By Day 365, I will...", 12)
        y += 15
        # Lines for writing
        for _ in range(10):
            self._grey_line(MARGIN + 20, y, PAGE_W - MARGIN - 20, y)
            y += 10
        y += 15
        self._centered_text(y, "Why this matters to me:", 11, bold=True)
        y += 12
        for _ in range(6):
            self._grey_line(MARGIN + 20, y, PAGE_W - MARGIN - 20, y)
            y += 10

    def add_progress_tracker(self):
        """Two pages with 365 small numbered squares."""
        for page_num in range(2):
            self.add_page()
            y = MARGIN
            if page_num == 0:
                self._centered_text(y, "Progress Tracker", 16, bold=True)
                y += 12
                self._set_font("", 8)
                self.set_xy(MARGIN, y)
                self.cell(CONTENT_W, 5, "Color in each square as you complete a day!", align='C')
                y += 10
                start_day = 1
                end_day = 200
            else:
                self._centered_text(y, "Progress Tracker (continued)", 14, bold=True)
                y += 12
                start_day = 201
                end_day = 365

            sq_size = 8
            cols = int(CONTENT_W // sq_size)
            self._set_font("", 5)
            self.set_draw_color(*GREY)
            x_start = MARGIN + (CONTENT_W - cols * sq_size) / 2
            d = start_day
            while d <= end_day:
                x = x_start
                for c in range(cols):
                    if d > end_day:
                        break
                    self.rect(x, y, sq_size, sq_size)
                    self.set_xy(x, y + 1)
                    self.cell(sq_size, sq_size - 2, str(d), align='C')
                    x += sq_size
                    d += 1
                y += sq_size
                if y > PAGE_H - MARGIN - 5:
                    break

    def add_monthly_overview(self):
        """4 pages with 3 months each showing verb themes."""
        all_verbs = get_all_verbs()
        pages = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]
        for page_months in pages:
            self.add_page()
            y = MARGIN
            self._centered_text(y, "Monthly Overview", 14, bold=True)
            y += 12
            for m in page_months:
                theme = MONTH_THEMES[m]
                self._set_font("B", 10)
                self.set_xy(MARGIN + 5, y)
                self.cell(CONTENT_W - 10, 6, f"Month {m}: {theme}")
                y += 7
                self._set_font("", 7)
                # Get verbs for this month
                month_verbs = [v for v in all_verbs if v[1] == m]
                # Show them in rows of 3
                for i in range(0, len(month_verbs), 3):
                    chunk = month_verbs[i:i+3]
                    text = "  |  ".join([f"Day {v[0]}: {v[2]} ({v[3]})" for v in chunk])
                    self.set_xy(MARGIN + 8, y)
                    self.cell(CONTENT_W - 16, 4.5, text)
                    y += 4.5
                y += 5
                if y > PAGE_H - MARGIN - 20:
                    break

    def add_daily_page(self, day, month, verb, meaning, prezent, perfect, viitor):
        """Add a single daily verb page."""
        self.add_page()
        theme = MONTH_THEMES[month]
        prefilled = prezent is not None

        y = MARGIN

        # Header
        self._set_font("B", 14)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W * 0.4, 7, f"DAY {day}/365")
        self._set_font("", 9)
        self.cell(CONTENT_W * 0.3, 7, "DATE: ___/___/___", align='C')
        self._set_font("B", 9)
        self.cell(CONTENT_W * 0.3, 7, f"MONTH {month}: {theme}", align='R')
        y += 9

        # Separator
        self._grey_line(MARGIN, y, PAGE_W - MARGIN, y)
        y += 4

        # Verb title
        self._set_font("B", 12)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W, 7, f"TODAY'S VERB:  {verb}  —  {meaning}", align='C')
        y += 10

        # Conjugation table
        self._set_font("B", 8)
        col_w_label = 28
        col_w = (CONTENT_W - col_w_label) / 3

        # Header row
        self.set_draw_color(*GREY)
        self.set_fill_color(*LIGHT_GREY)
        self.set_xy(MARGIN, y)
        self.cell(col_w_label, 7, "", border=1, fill=True)
        for t in TENSES:
            self.cell(col_w, 7, t, border=1, align='C', fill=True)
        y += 7

        # Data rows
        self._set_font("", 7)
        for i, pron in enumerate(PRONOUNS):
            self.set_xy(MARGIN, y)
            self._set_font("B", 7)
            self.cell(col_w_label, 7, f"  {pron}", border=1)
            self._set_font("", 7)
            if prefilled:
                self.cell(col_w, 7, f"  {prezent[i]}", border=1)
                self.cell(col_w, 7, f"  {perfect[i]}", border=1)
                self.cell(col_w, 7, f"  {viitor[i]}", border=1)
            else:
                for _ in range(3):
                    self.cell(col_w, 7, "", border=1)
            y += 7
        y += 5

        # USE IT section
        self._set_font("B", 10)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W, 6, "USE IT — 6 Sentences")
        y += 8

        sentences = [
            ("PREZENT", "Write about TODAY:"),
            ("PERFECT COMPUS", "Write about YESTERDAY:"),
            ("VIITOR", "Write about TOMORROW:"),
            ("NEGATIV", "Write what you DON'T do:"),
            ("ÎNTREBARE", "Ask someone a question:"),
            ("VIAȚA TA", "Use this verb about YOUR life:"),
        ]
        self._set_font("", 8)
        for label, prompt in sentences:
            self.set_xy(MARGIN, y)
            self._set_font("B", 8)
            self.cell(35, 5, f"{label}")
            self._set_font("", 8)
            self.cell(10, 5, "— ")
            self.cell(CONTENT_W - 45, 5, prompt)
            y += 6
            # Writing line
            self._grey_line(MARGIN + 5, y + 3, PAGE_W - MARGIN - 5, y + 3)
            y += 8

        y += 2

        # BONUS section
        self._set_font("B", 9)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W, 5, "BONUS")
        y += 6
        self._set_font("", 8)
        self.set_xy(MARGIN + 3, y)
        self.cell(CONTENT_W - 6, 5, "Related words/phrases:  1.____________  2.____________  3.____________")
        y += 7
        self.set_xy(MARGIN + 3, y)
        self.cell(CONTENT_W - 6, 5, "Idiom or expression: ____________________  Meaning: ____________________")
        y += 9

        # TODAY'S LOG
        self._set_font("B", 9)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W, 5, "TODAY'S LOG")
        y += 6
        self.set_draw_color(*GREY)
        self.rect(MARGIN, y, CONTENT_W, 10)
        self._set_font("", 7)
        self.set_xy(MARGIN + 3, y + 1.5)
        self.cell(CONTENT_W - 6, 7,
                  "Time spent: ___ min  |  Difficulty:  ○ Easy  ○ Medium  ○ Hard  |  Confidence: 1  2  3  4  5  |  Review again?  □ Yes  □ No")

    def add_back_matter(self, all_verbs):
        """Add verb index, redo list, reflections, certificate."""
        # --- Verb Index (multiple pages as needed) ---
        sorted_verbs = sorted(all_verbs, key=lambda v: v[2].lower().replace("a ", "").replace("a se ", ""))
        
        self.add_page()
        y = MARGIN
        self._centered_text(y, "Verb Index", 16, bold=True)
        y += 12

        self._set_font("B", 8)
        self.set_xy(MARGIN, y)
        self.cell(55, 6, "Verb", border=1, align='C')
        self.cell(55, 6, "English", border=1, align='C')
        self.cell(20, 6, "Day", border=1, align='C')
        self.cell(25, 6, "Month", border=1, align='C')
        y += 6

        self._set_font("", 7)
        for v in sorted_verbs:
            if y > PAGE_H - MARGIN - 8:
                self.add_page()
                y = MARGIN
                self._centered_text(y, "Verb Index (continued)", 14, bold=True)
                y += 10
                self._set_font("B", 8)
                self.set_xy(MARGIN, y)
                self.cell(55, 6, "Verb", border=1, align='C')
                self.cell(55, 6, "English", border=1, align='C')
                self.cell(20, 6, "Day", border=1, align='C')
                self.cell(25, 6, "Month", border=1, align='C')
                y += 6
                self._set_font("", 7)
            self.set_xy(MARGIN, y)
            self.cell(55, 5, f"  {v[2]}", border=1)
            self.cell(55, 5, f"  {v[3]}", border=1)
            self.cell(20, 5, str(v[0]), border=1, align='C')
            self.cell(25, 5, str(v[1]), border=1, align='C')
            y += 5

        # --- Verbs I Need to Redo ---
        self.add_page()
        y = MARGIN
        self._centered_text(y, "Verbs I Need to Redo", 16, bold=True)
        y += 14
        self._set_font("", 9)
        self.set_xy(MARGIN, y)
        self.cell(CONTENT_W, 6, "Write down any verbs you want to practice again:", align='C')
        y += 12
        for i in range(1, 31):
            self.set_xy(MARGIN + 10, y)
            self._set_font("", 8)
            self.cell(8, 6, f"{i}.")
            self._grey_line(MARGIN + 20, y + 5, MARGIN + 85, y + 5)
            if i <= 30:
                self.set_xy(MARGIN + 90, y)
                j = i + 30
                if j <= 60:
                    self.cell(8, 6, f"{j}.")
                    self._grey_line(MARGIN + 100, y + 5, MARGIN + 165, y + 5)
            y += 7.5
            if y > PAGE_H - MARGIN - 10:
                break

        # --- Monthly Reflections (condensed: 4 months per page, 3 pages) ---
        months_per_page = 4
        for page_start in range(0, 12, months_per_page):
            self.add_page()
            y = MARGIN
            self._centered_text(y, "Monthly Reflections", 14, bold=True)
            y += 12
            for m in range(page_start + 1, min(page_start + months_per_page + 1, 13)):
                theme = MONTH_THEMES[m]
                self._set_font("B", 10)
                self.set_xy(MARGIN + 5, y)
                self.cell(CONTENT_W - 10, 6, f"Month {m}: {theme}")
                y += 7
                self._set_font("", 8)
                prompts = [
                    "Favorite verb this month: ________________________________",
                    "Hardest verb: ________________________________",
                    "What I can now say: ________________________________",
                    "Goal for next month: ________________________________",
                ]
                for p in prompts:
                    self.set_xy(MARGIN + 10, y)
                    self.cell(CONTENT_W - 20, 5.5, p)
                    y += 6
                y += 5

        # --- Certificate of Completion ---
        self.add_page()
        y = 50
        # Decorative border
        self.set_draw_color(100, 100, 100)
        self.set_line_width(1)
        self.rect(MARGIN + 10, 30, CONTENT_W - 20, PAGE_H - 80)
        self.set_line_width(0.3)
        self.rect(MARGIN + 13, 33, CONTENT_W - 26, PAGE_H - 86)
        self.set_line_width(0.2)

        y = 55
        self._centered_text(y, "Certificate of Completion", 22, bold=True)
        y += 20
        self._centered_text(y, "This certifies that", 12)
        y += 15
        self._grey_line(MARGIN + 50, y, PAGE_W - MARGIN - 50, y)
        y += 3
        self._centered_text(y, "(Your Name)", 8)
        y += 15
        self._centered_text(y, "has successfully completed", 12)
        y += 12
        self._centered_text(y, "ONE VERB A DAY", 18, bold=True)
        y += 10
        self._centered_text(y, "365 Days of Romanian Verb Mastery", 13)
        y += 20
        self._centered_text(y, "mastering 365 Romanian verbs across 12 thematic months,", 10)
        y += 7
        self._centered_text(y, "building fluency one verb at a time.", 10)
        y += 25
        self._set_font("", 10)
        self.set_xy(MARGIN + 30, y)
        self.cell(60, 8, "Start Date: ___________")
        self.cell(60, 8, "End Date: ___________")
        y += 20
        self._centered_text(y, "Felicitări! Congratulations!", 14, bold=True)


def main():
    print("Building verb data...")
    all_verbs = get_all_verbs()
    print(f"Total verbs: {len(all_verbs)}")

    pdf = VerbPDF()
    pdf.set_title("ONE VERB A DAY: 365 Days of Romanian Verb Mastery")
    pdf.set_author("ONE VERB A DAY Series")

    # Front matter
    print("Adding front matter...")
    pdf.add_title_page()           # Page 1
    pdf.add_how_to_use()           # Page 2
    pdf.add_pronoun_reference()    # Page 3
    pdf.add_tense_reference()      # Page 4
    pdf.add_conjugation_groups()   # Page 5
    pdf.add_goal_page()            # Page 6
    pdf.add_progress_tracker()     # Pages 7-8
    pdf.add_monthly_overview()     # Pages 9-12

    # Daily pages
    print("Adding 365 daily pages...")
    for i, v in enumerate(all_verbs):
        day, month, verb, meaning = v[0], v[1], v[2], v[3]
        prezent, perfect, viitor = v[4], v[5], v[6]
        pdf.add_daily_page(day, month, verb, meaning, prezent, perfect, viitor)
        if (i + 1) % 50 == 0:
            print(f"  Day {i + 1}/365 done...")

    # Back matter
    print("Adding back matter...")
    pdf.add_back_matter(all_verbs)

    out_path = "/workspace/one-verb-a-day/romanian/one-verb-a-day-romanian.pdf"
    print(f"Saving PDF to {out_path}...")
    pdf.output(out_path)
    
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Done! PDF saved: {out_path} ({size_mb:.1f} MB, {pdf.pages_count} pages)")


if __name__ == "__main__":
    main()
