import re
import json

with open("/workspace/one-verb-a-day/romanian/generate_verbs.py", "r", encoding="utf-8") as f:
    text = f.read()

# I need to extract all tuples from MONTH1 to MONTH4
# The tuples can have 5 elements (verb, trans, pres, past, fut) OR 2 elements (verb, trans).
# Let's extract the string blocks of MONTH1..MONTH4
matches = re.findall(r'(MONTH[1-4]_VERBS\s*=\s*\[.*?\])', text, re.DOTALL)

code = ""
for m in matches:
    code += m + "\n"

loc = {}
exec(code, {}, loc)

all_verbs = loc['MONTH1_VERBS'] + loc['MONTH2_VERBS'] + loc['MONTH3_VERBS'] + loc['MONTH4_VERBS']

with open("/workspace/one-verb-a-day/romanian/verbs_100_full.json", "w", encoding="utf-8") as f:
    json.dump(all_verbs[:100], f, ensure_ascii=False, indent=2)

print(f"Extracted {len(all_verbs[:100])} verbs!")
