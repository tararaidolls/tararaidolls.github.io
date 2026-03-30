import re
import json

with open("/workspace/one-verb-a-day/romanian/generate_verbs.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.split("class VerbPDF(FPDF):")[0]
lines = [l for l in text.split('\n') if not l.startswith('from ') and not l.startswith('import ')]
code = '\n'.join(lines)

loc = {}
exec(code, {}, loc)

all_verbs = loc['MONTH1_VERBS'] + loc['MONTH2_VERBS'] + loc['MONTH3_VERBS'] + loc['MONTH4_VERBS']
verbs_100 = all_verbs[:100]

with open("/workspace/one-verb-a-day/romanian/verbs_100_full.json", "w", encoding="utf-8") as f:
    json.dump(verbs_100, f, ensure_ascii=False, indent=2)

print(f"Success! {len(verbs_100)} verbs")
