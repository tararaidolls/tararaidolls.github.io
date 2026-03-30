import re
with open('/workspace/one-verb-a-day/romanian/generate_verbs.py', 'r') as f:
    text = f.read()
# Just get the whole file content, and parse the tuples manually.
import ast
# To parse, let's just use regex to extract the first element of each tuple.
matches = re.findall(r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,', text)
for i, m in enumerate(matches[:100]):
    print(f"{i+1}. {m[0]} - {m[1]}")
