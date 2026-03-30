import re

with open("/workspace/one-verb-a-day/romanian/generate_verbs.py", "r") as f:
    text = f.read()

# I will use a simple regex to extract the (verb, translation, present, past, future) tuples.
# This pattern: `\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*\[([^\]]+)\]\s*,\s*\[([^\]]+)\]\s*,\s*\[([^\]]+)\]\s*\)`
matches = re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*\[(.*?)\]\s*,\s*\[(.*?)\]\s*,\s*\[(.*?)\]\s*\)', text, re.DOTALL)

verbs_100 = []
for m in matches[:100]:
    verb = m[0]
    translation = m[1]
    present = [x.strip().strip('"').strip("'") for x in m[2].split(',')]
    past = [x.strip().strip('"').strip("'") for x in m[3].split(',')]
    future = [x.strip().strip('"').strip("'") for x in m[4].split(',')]
    verbs_100.append((verb, translation, present, past, future))

with open('/workspace/one-verb-a-day/romanian/extract_import.py', 'w') as f:
    f.write("verbs_100 = [\n")
    for v in verbs_100:
        f.write(f"    {v},\n")
    f.write("]\n")

print(f"Extracted {len(verbs_100)} full verbs!")
