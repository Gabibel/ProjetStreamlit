"""
Normalize whitespace: replace tab characters immediately after commas or parentheses
with a single space. Works recursively over .py files in the workspace folder.

Run: python scripts\normalize_whitespace.py
"""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
py_files = list(root.rglob('*.py'))

pattern_comma = re.compile(r',\t+')
pattern_open = re.compile(r'\(\t+')
pattern_close = re.compile(r'\t+\)')

modified = []
for p in py_files:
    text = p.read_text(encoding='utf-8')
    new = pattern_comma.sub(', ', text)
    new = pattern_open.sub('( ', new)
    new = pattern_close.sub(' )', new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        modified.append(str(p))

print('Files modified:')
for m in modified:
    print(m)
if not modified:
    print('No changes made')
