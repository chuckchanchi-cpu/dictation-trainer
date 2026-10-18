# -*- coding: utf-8 -*-
"""Smoke test：語法 + 詞語數量 + 例句挖空有效性"""
import py_compile, ast, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
py_compile.compile("app.py", doraise=True)
print("✅ syntax OK")

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
WORDS = None
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "WORDS":
                WORDS = ast.literal_eval(node.value)

assert WORDS is not None and len(WORDS) == 10, f"應該 10 個詞語，實際 {len(WORDS) if WORDS else 0}"
print(f"✅ WORDS: {len(WORDS)} 個詞語")

for w, m, ex in WORDS:
    assert w in ex, f"詞語「{w}」冇喺例句中出現"
print("✅ 每個詞語都喺例句中出現（挖空有效）")

ws = [w for w, _, _ in WORDS]
assert len(set(ws)) == len(ws), "詞語有重複"
print("✅ 詞語無重複")

for w, m, ex in WORDS:
    assert w.strip() and m.strip() and ex.strip()
print("✅ 詞語/解釋/例句全非空")

print("done")
