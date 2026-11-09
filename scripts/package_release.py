#!/usr/bin/env python3
"""Safely package a static site release with a Git SHA and SHA-256 manifest.

Only explicitly permitted files are included; never packages a database dump.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
DOCS = ["INSTALL.md", "RELEASE_NOTES.md", "TEST_REPORT.md", "ACCEPTANCE.md", "DATA_SAFETY.md"]
VERSION_RE = re.compile(r"^v(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-(?:rc|beta)\.[1-9]\d*)?$")


def git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def collect_files(source: Path, destination: str) -> dict[str, bytes]:
    data = {}
    if not source.exists():
        return data
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"不可打包符號連結：{path}")
        if not path.is_file():
            continue
        parts = path.relative_to(source).parts
        if any((p.startswith(".") and not (destination == "website" and p == ".nojekyll" and len(parts) == 1)) or re.search(r"secret|credential|\.env|private|backup", p, re.I) for p in parts):
            raise ValueError(f"偵測到不允許的部署檔名：{path}")
        data[f"{destination}/{'/'.join(parts)}"] = path.read_bytes()
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="建立有 Git SHA / SHA-256 清單的網站交付 ZIP")
    parser.add_argument("--version", required=True, help="例如 v1.2.0 或 v1.2.0-rc.1")
    parser.add_argument("--output", default="release", help="輸出資料夾，預設 release")
    parser.add_argument("--draft", action="store_true", help="允許無 Git 專案，以 DRAFT 字樣標註測試包")
    args = parser.parse_args()

    if not VERSION_RE.fullmatch(args.version):
        parser.error("版本格式應為 v1.2.3 或 v1.2.3-rc.1 / v1.2.3-beta.1")

    dist = ROOT / "dist"
    if not (dist / "index.html").is_file():
        parser.error("缺少 dist/index.html。請先執行 npm run build")

    git_sha = git("rev-parse", "HEAD")
    if not args.draft:
        if not git_sha or not re.fullmatch(r"[0-9a-f]{40,64}", git_sha):
            parser.error("正式打包需要有效 Git Commit。若只是試打包，使用 --draft")
        ref = os.environ.get("GITHUB_REF", "")
        branch = git("branch", "--show-current")
        if ref and ref != "refs/heads/main":
            parser.error(f"正式打包只能從 main 執行，實際 ref：{ref}")
        if not ref and branch != "main":
            parser.error(f"正式打包只能從 main 執行，實際分支：{branch}")
        if git("status", "--porcelain"):
            parser.error("Git 工作目錄仍有未提交變更；請先提交或使用 --draft 測試")
        release_notes = (ROOT / "docs/RELEASE_NOTES.md").read_text(encoding="utf-8")
        test_report = (ROOT / "docs/TEST_REPORT.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "docs/ACCEPTANCE.md").read_text(encoding="utf-8")
        if any(marker in release_notes for marker in ("[待填]", "[內容]", "[相容性", "[連結證據]", "[實際 PR")):
            parser.error("RELEASE_NOTES.md 仍有模板佔位內容")
        if f"- 版本：`{args.version}`" not in release_notes:
            parser.error("RELEASE_NOTES.md 的版號必須與輸入版本一致")
        if any(marker in test_report for marker in ("[待填]", "[待確認", "[請填")):
            parser.error("TEST_REPORT.md 仍有模板佔位內容")
        if any(marker in acceptance for marker in ("[請填", "[專案]", "[使用者]", "[Issue /")):
            parser.error("ACCEPTANCE.md 仍有模板佔位內容")
        # 人工核准是必要條件。版本發布工作必須經 GitHub 權限與分支保護限制。
        if not re.search(r"(?mi)^\s*-\s*\[[xX]\]\s*可以合併／發布", acceptance):
            parser.error("ACCEPTANCE.md 未勾選『可以合併／發布』；需要負責人核准")
        if not re.search(r"(?m)^核准者：`(?!\[)[^`]+`", acceptance):
            parser.error("ACCEPTANCE.md 缺少明確核准者")
        def unrun_table_rows(doc: str, status_col: int) -> list[str]:
            problems = []
            for line in doc.splitlines():
                if not line.lstrip().startswith("|"):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) > status_col and "未執行" in cells[status_col] and not cells[status_col].startswith("結果"):
                    problems.append(line.strip())
            return problems

        if unrun_table_rows(test_report, 1) or unrun_table_rows(acceptance, 2):
            parser.error("驗收表仍有『未執行』的檢查項目；請完成測試或標註不適用並說明")

    project = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["name"]
    slug = re.sub(r"[^a-z0-9_-]", "-", project.lower()).strip("-") or "website"
    folder = f"{slug}-{args.version}"

    payload = collect_files(dist, "website")
    for name in DOCS:
        doc = ROOT / "docs" / name
        if not doc.is_file():
            parser.error(f"缺少必要交付文件：docs/{name}")
        payload[f"docs/{name}"] = doc.read_bytes()
    for file in sorted((ROOT / "database" / "migrations").rglob("*.sql")):
        if file.is_symlink():
            parser.error(f"不允許 SQL 符號連結：{file}")
        sub_path = file.relative_to(ROOT / "database" / "migrations")
        payload[f"database/migrations/{sub_path.as_posix()}"] = file.read_bytes()

    if not payload:
        parser.error("沒有可打包的網站內容")
    meta = {
        "project": project,
        "version": args.version,
        "source_commit": git_sha or "UNVERSIONED-DRAFT",
        "status": "DRAFT_NOT_FOR_PRODUCTION" if args.draft else "RELEASE_PACKAGE",
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "website_source": "site/ -> dist/",
        "database_backup_included": False,
        "database_migrations_auto_executed": False,
    }
    payload["VERSION.json"] = (json.dumps(meta, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    checksum = "".join(
        f"{hashlib.sha256(content).hexdigest()}  {name}\n"
        for name, content in sorted(payload.items())
    )
    payload["SHA256SUMS.txt"] = checksum.encode("utf-8")

    out_dir = (ROOT / args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{folder}-{'DRAFT' if args.draft else 'RELEASE'}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name, content in sorted(payload.items()):
            zf.writestr(f"{folder}/{name}", content)
    print(f"已建立：{target}")
    print(f"版本：{args.version}  Commit：{meta['source_commit']}  模式：{meta['status']}")
    print("注意：打包不代表已通過正式驗收，且不包含資料庫備份。")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        sys.exit(f"打包失敗：{exc}")
