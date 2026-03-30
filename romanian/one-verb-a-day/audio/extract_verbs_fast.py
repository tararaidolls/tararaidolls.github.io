import sys
sys.path.append("/workspace/one-verb-a-day/romanian")

with open("/workspace/one-verb-a-day/romanian/dummy_fpdf.py", "w") as f:
    f.write("class FPDF: pass\nclass VerbPDF(FPDF): pass\n")

import os
os.system("sed 's/from fpdf import FPDF/from dummy_fpdf import FPDF, VerbPDF/g' /workspace/one-verb-a-day/romanian/generate_verbs.py > /workspace/one-verb-a-day/romanian/temp_gv.py")

import temp_gv

verbs_100 = temp_gv.MONTH1_VERBS + temp_gv.MONTH2_VERBS + temp_gv.MONTH3_VERBS + temp_gv.MONTH4_VERBS
import json
with open("/workspace/one-verb-a-day/romanian/verbs_100_full.json", "w", encoding="utf-8") as f:
    json.dump(verbs_100[:100], f, ensure_ascii=False, indent=2)

print(f"Extracted {len(verbs_100[:100])} verbs!")
