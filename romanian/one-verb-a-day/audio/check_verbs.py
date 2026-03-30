import re
import json

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
        all_verbs.extend(loc[key])

print(f"Total verbs found: {len(all_verbs)}")
