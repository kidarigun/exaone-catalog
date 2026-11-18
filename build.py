"""catalog.src.json과 skills/ 폴더로 배포용 catalog.json과 dist/*.zip을 만든다.

사용법:  python build.py
- skills/<id>/ 폴더를 dist/<id>.zip으로 묶고 sha256·크기를 catalog.json에 적는다.
- 같은 내용이면 zip도 항상 같게 만든다 (파일 순서·시각 고정) → 변경이 없으면 sha256도 그대로.
- "source": {"repo", "commit", "path"}가 있는 Skill은 그 GitHub 저장소의 고정된 커밋에서 폴더를 받아 묶는다.
  원본의 LICENSE는 그대로 두고, 출처를 적은 SOURCE.md와 저장소의 THIRD_PARTY_NOTICES.md를 함께 넣는다.
"""
import datetime
import hashlib
import json
import re
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "catalog.src.json"
OUT = ROOT / "catalog.json"
DIST = ROOT / "dist"
FIXED_TIME = (2020, 1, 1, 0, 0, 0)
SKIP = {"__pycache__", ".DS_Store", "Thumbs.db"}
CACHE = ROOT / ".cache"


def fetch_source(repo: str, commit: str) -> Path:
    """GitHub 저장소를 고정된 커밋으로 받아 .cache에 풀고 그 최상위 폴더를 돌려준다."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        sys.exit(f"[오류] {repo}: commit은 40자리 커밋 해시여야 합니다.")
    dest = CACHE / f"{repo.replace('/', '__')}-{commit}"
    if not dest.exists():
        CACHE.mkdir(exist_ok=True)
        archive = CACHE / f"{dest.name}.tar.gz"
        url = f"https://codeload.github.com/{repo}/tar.gz/{commit}"
        print(f"받는 중: {url}")
        urllib.request.urlretrieve(url, archive)
        tmp = CACHE / f"{dest.name}.tmp"
        with tarfile.open(archive) as t:
            t.extractall(tmp, filter="data")
        (top,) = list(tmp.iterdir())
        top.rename(dest)
        tmp.rmdir()
        archive.unlink()
    return dest


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


def build_zip(folder: Path, name: str, extra=None) -> Path:
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
        for rel, data in sorted((extra or {}).items()):
            info = zipfile.ZipInfo(f"{name}/{rel}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    return target


def main():
    catalog = json.loads(SRC.read_text(encoding="utf-8"))
    ok = True
    for skill in catalog.get("skills", []):
        extra = {}
        src = skill.get("source")
        if src:
            repo_dir = fetch_source(src["repo"], src["commit"])
            folder = repo_dir / src["path"]
            if (folder / "LICENSE.txt").exists():
                license_file = "LICENSE.txt"
            elif (folder / "LICENSE").exists():
                license_file = "LICENSE"
            elif (repo_dir / "LICENSE").exists():
                license_file = "LICENSE"
                extra["LICENSE"] = (repo_dir / "LICENSE").read_bytes()
            elif (repo_dir / "LICENSE.txt").exists():
                license_file = "LICENSE.txt"
                extra["LICENSE.txt"] = (repo_dir / "LICENSE.txt").read_bytes()
            else:
                print(f"[오류] {skill['id']}: 원본 폴더나 저장소 루트에 LICENSE가 없어 다시 배포할 수 없습니다.")
                ok = False
                continue
            extra["SOURCE.md"] = "\n".join([
                "# 출처",
                "",
                f"이 Skill은 {src['repo']} 저장소의 `{src['path']}`를 그대로 옮긴 것입니다.",
                "",
                f"- 원본: https://github.com/{src['repo']}/tree/{src['commit']}/{src['path']}",
                f"- 라이선스: {skill.get('license', '원본 LICENSE 파일 참고')} ({license_file})",
                "- 내용은 바꾸지 않았습니다.",
                "",
            ]).encode("utf-8")
            notices = repo_dir / "THIRD_PARTY_NOTICES.md"
            if notices.exists():
                extra["THIRD_PARTY_NOTICES.md"] = notices.read_bytes()
        else:
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
        z = build_zip(folder, skill["id"], extra)
        data = z.read_bytes()
        skill["download"] = z.relative_to(ROOT).as_posix()
        skill["sha256"] = hashlib.sha256(data).hexdigest()
        skill["size"] = len(data)
        skill["files"] = sorted(
            [p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file() and not (set(p.parts) & SKIP)]
            + list(extra)
        )
        if len(skill["files"]) > 40:
            skill["fileCount"] = len(skill["files"])
            skill["files"] = skill["files"][:40]
        print(f"{skill['id']}: {len(data):,} bytes  {skill['sha256'][:12]}…")
    if not ok:
        sys.exit(1)
    catalog["updated"] = datetime.date.today().isoformat()
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog.json: MCP {len(catalog.get('mcp', []))}개, Skill {len(catalog.get('skills', []))}개")


if __name__ == "__main__":
    main()
