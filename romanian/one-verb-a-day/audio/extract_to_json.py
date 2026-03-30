import re
import json

with open("/workspace/one-verb-a-day/romanian/generate_verbs.py", "r", encoding="utf-8") as f:
    text = f.read()

# I will extract ALL 400 verbs now to ensure we have enough data to fill the empty chapters.
matches = re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*\[(.*?)\]\s*,\s*\[(.*?)\]\s*\)', text, re.DOTALL)

verbs_all = []
for m in matches:
    verb = m[0]
    translation = m[1]
    present = [x.strip().strip('"').strip("'") for x in m[2].split(',')]
    past = [x.strip().strip('"').strip("'") for x in m[3].split(',')]
    future = [x.strip().strip('"').strip("'") for x in m[4].split(',')]
    verbs_all.append((verb, translation, present, past, future))

# But wait, in original `generate_verbs.py`, MONTH2 to MONTH12 ONLY HAD `(verb, translation)` without conjugations!
# Let me check if there are 100 verbs with conjugations.
print(f"Found {len(verbs_all)} verbs with full conjugations.")
