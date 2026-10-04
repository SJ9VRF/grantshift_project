from __future__ import annotations
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts'/'grantshift-github-ready-source-v1.4.0.zip'
SKIP_PARTS={'.git','.pytest_cache','__pycache__','submission/anonymous_source'}
SKIP_SUFFIX={'.pyc','.whl','.zip'}

def skip(p:Path):
    rel=p.relative_to(ROOT).as_posix()
    if rel==OUT.relative_to(ROOT).as_posix(): return True
    if rel.startswith('submission/anonymous_source/'): return True
    if rel.startswith('dist/') or rel.startswith('build/'): return True
    if any(part in {'.git','.pytest_cache','__pycache__'} for part in p.parts): return True
    if p.suffix in SKIP_SUFFIX: return True
    if p.name.startswith('grantshift-github-ready-source-') and p.suffix=='.zip': return True
    return False
if OUT.exists(): OUT.unlink()
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and not skip(p): z.write(p,p.relative_to(ROOT))
print(OUT)
