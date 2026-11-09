#!/usr/bin/env python3
"""Verify SHA-256 manifest and basic structural integrity of release ZIP."""
import argparse
import hashlib
from pathlib import Path
import sys
import zipfile
import json


def main(path: Path, expected_version: str | None = None, expected_commit: str | None = None) -> None:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        roots = {n.split("/")[0] for n in names}
        assert len(roots) == 1, "ZIP 必須只有一個專案根資料夾"
        root = next(iter(roots))
        names_set = set(names)
        assert all(".." not in n.split("/") for n in names), "偵測到不安全的路徑"
        manifest = z.read(f"{root}/SHA256SUMS.txt").decode("utf-8")
        metadata = json.loads(z.read(f"{root}/VERSION.json"))
        assert len(names_set) == len(names), "ZIP 內有重複檔名"
        assert all(not n.startswith("/") and "\\" not in n for n in names), "不安全的路徑"
        assert f"{root}/website/index.html" in names_set, "缺少首頁"
        if expected_version is not None:
            assert metadata["version"] == expected_version, "版本號與預期不一致"
        if expected_commit is not None:
            assert metadata["source_commit"] == expected_commit, "Commit 與預期不一致"
        assert metadata["database_backup_included"] is False, "ZIP 中不能宣稱含資料庫備份"
        checked = set()
        for line in manifest.splitlines():
            digest, sep, filename = line.partition("  ")
            assert sep and filename, f"校驗清單格式錯誤：{line}"
            actual = hashlib.sha256(z.read(f"{root}/{filename}")).hexdigest()
            assert digest == actual, f"雜湊不一致：{filename}"
            checked.add(f"{root}/{filename}")
        expected = set(names) - {f"{root}/SHA256SUMS.txt"}
        assert checked == expected, "ZIP 有未列入 checksum 的檔案或 checksum 指向不存在的檔案"
        print(f"驗證通過：{path.name}，{len(checked)} 個檔案，版本 {metadata['version']}，Commit {metadata['source_commit']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="驗證 ZIP 與 SHA-256、版號和 Commit")
    parser.add_argument("zip_file")
    parser.add_argument("--expected-version")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    try:
        main(Path(args.zip_file), args.expected_version, args.expected_commit)
    except (AssertionError, KeyError, OSError, zipfile.BadZipFile, ValueError) as e:
        sys.exit(f"驗證失敗：{e}")
