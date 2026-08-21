"""Fail when a relative Markdown link points to a missing local path."""
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
errors=[]
for document in sorted(ROOT.rglob("*.md")):
    if any(part.startswith(".") for part in document.relative_to(ROOT).parts): continue
    for number,line in enumerate(document.read_text(encoding="utf-8").splitlines(),1):
        for raw in LINK.findall(line):
            target=raw.split("#",1)[0]
            if not target or "://" in target or target.startswith("mailto:"): continue
            resolved=(document.parent/target).resolve()
            if not resolved.exists(): errors.append(f"{document.relative_to(ROOT)}:{number}: {raw}")
if errors:
    print("Broken local Markdown links:\n"+"\n".join(errors)); sys.exit(1)
print("All local Markdown links resolve.")
