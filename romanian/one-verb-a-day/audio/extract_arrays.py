import re

with open('/workspace/one-verb-a-day/romanian/generate_verbs.py', 'r') as f:
    content = f.read()

verbs = []
# Find all the lists of verbs
lists = re.findall(r'MONTH\d+_VERBS\s*=\s*\[(.*?)\]', content, re.DOTALL)
for lst in lists:
    matches = re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,', lst)
    verbs.extend(matches)

with open('/workspace/one-verb-a-day/romanian/100_verbs.txt', 'w') as f:
    for i, v in enumerate(verbs[:100]):
        f.write(f"{i+1}. {v[0]} - {v[1]}\n")

print(len(verbs[:100]))
