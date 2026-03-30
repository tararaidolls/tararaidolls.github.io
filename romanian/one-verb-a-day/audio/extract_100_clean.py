import re
with open('/workspace/one-verb-a-day/romanian/generate_verbs.py', 'r') as f:
    lines = f.readlines()

verbs = []
for line in lines:
    m = re.match(r'\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,', line)
    if m:
        verbs.append(m.groups())

for i, v in enumerate(verbs[:100]):
    print(f"{i+1}. {v[0]} - {v[1]}")
