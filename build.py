"""catalog.src.json과 skills/ 폴더로 배포용 catalog.json과 dist/*.zip을 만든다.

사용법:  python build.py
- skills/<id>/ 폴더를 dist/<id>.zip으로 묶고 sha256·크기를 catalog.json에 적는다.
- 같은 내용이면 zip도 항상 같게 만든다 (파일 순서·시각 고정) → 변경이 없으면 sha256도 그대로.
"""
import datetime
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "catalog.src.json"
OUT = ROOT / "catalog.json"
DIST = ROOT / "dist"
FIXED_TIME = (2020, 1, 1, 0, 0, 0)
SKIP = {"__pycache__", ".DS_Store", "Thumbs.db"}


def front_matter(text):
    m = re.match(r"^﻿?---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip("'\"")
    return out


def build_zip(folder: Path, name: str) -> Path:
    DIST.mkdir(exist_ok=True)
    target = DIST / f"{name}.zip"
    files = sorted(p for p in folder.rglob("*") if p.is_file() and not (set(p.parts) & SKIP))
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            rel = p.relative_to(folder).as_posix()
            info = zipfile.ZipInfo(f"{name}/{rel}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())
    return target


def main():
    catalog = json.loads(SRC.read_text(encoding="utf-8"))
    ok = True
    for skill in catalog.get("skills", []):
        folder = ROOT / skill.pop("path")
        md = folder / "SKILL.md"
        if not md.exists():
            print(f"[오류] {folder}에 SKILL.md가 없습니다.")
            ok = False
            continue
        meta = front_matter(md.read_text(encoding="utf-8"))
        if not meta.get("name") or not meta.get("description"):
            print(f"[오류] {md}: 머리말에 name과 description이 있어야 합니다.")
            ok = False
        skill["skillName"] = meta.get("name", skill["id"])
        z = build_zip(folder, skill["id"])
        data = z.read_bytes()
        skill["download"] = z.relative_to(ROOT).as_posix()
        skill["sha256"] = hashlib.sha256(data).hexdigest()
        skill["size"] = len(data)
        skill["files"] = sorted(
            p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file() and not (set(p.parts) & SKIP)
        )
        print(f"{skill['id']}: {len(data):,} bytes  {skill['sha256'][:12]}…")
    if not ok:
        sys.exit(1)
    catalog["updated"] = datetime.date.today().isoformat()
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog.json: MCP {len(catalog.get('mcp', []))}개, Skill {len(catalog.get('skills', []))}개")


if __name__ == "__main__":
    main()
