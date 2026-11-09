#!/usr/bin/env python3
"""匯出 GitHub PR 式三點比較的審查文件。無第三方依賴；不會修改 Git 版本。

輸出可能包含機密：即使通過基礎敏感資訊檢查，仍必須人工審閱後才分享。
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 512 * 1024
SENSITIVE_PATH = re.compile(r"(?i)(^|/)(\.env(?:\.|$)|secrets?(?:/|\.|$)|credentials?(?:/|\.|$)|private(?:/|\.|$)|backups?(?:/|\.|$))|\.(?:pem|p12|pfx|key|sqlite3?|db)$")
SENSITIVE_CONTENT = [
    re.compile(r"(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{18,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:service[_-]?role[_-]?key|password|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]

def git(*args: str) -> str:
    p = subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode:
        raise RuntimeError(f"git {' '.join(args)} 失敗：{p.stderr.strip()}")
    return p.stdout.strip('\n')

def fence(value: str) -> str:
    lengths = [len(m.group(0)) for m in re.finditer(r'`+',value)]
    return '`' * max(4, max(lengths, default=0)+1)

def main() -> int:
    parser=argparse.ArgumentParser(description='匯出固定 Commit 的 PR 差異供 ChatGPT 獨立 Code Review')
    parser.add_argument('--base',default=None,help='PR 目標分支，例如 origin/main 或 main')
    parser.add_argument('--head',default='HEAD',help='PR 開發分支，例如 HEAD')
    parser.add_argument('--output',default=None,help='輸出 Markdown；預設 .review-packets/PR_REVIEW_PACKET-HEADSHA.md')
    parser.add_argument('--path',action='append',default=[],help='僅選定子目錄／檔案，可重複指定，供大型 PR 分批審查')
    args=parser.parse_args()
    try:
        git('rev-parse','--is-inside-work-tree')
        if args.base:
            base=args.base
        else:
            base='origin/main' if subprocess.run(['git','rev-parse','--verify','origin/main'],capture_output=True).returncode==0 else 'main'
        base_sha=git('rev-parse',f'{base}^{{commit}}')
        head_sha=git('rev-parse',f'{args.head}^{{commit}}')
        git('merge-base',base_sha,head_sha)
        revision=f'{base_sha}...{head_sha}'
        common=['--no-ext-diff','--no-textconv',revision]
        path_args=['--',*args.path] if args.path else []
        names=git('diff','--name-only','--diff-filter=ACDMRTUXB',*common,*path_args)
        selected=[n for n in names.splitlines() if n]
        blocked=[f for f in selected if SENSITIVE_PATH.search(f)]
        if blocked:
            raise RuntimeError('偵測到可能含機密的路徑，停止輸出：'+', '.join(blocked[:10]))
        stat=git('diff','--stat',*common,*path_args)
        diff=git('diff','--no-color','--find-renames','--unified=3',*common,*path_args)
        if not diff:
            raise RuntimeError('沒有可供審查的差異；請確認開發分支、base，或是否已合併 main。')
        if len(diff.encode('utf8')) > MAX_BYTES:
            raise RuntimeError(f'差異超過 {MAX_BYTES//1024} KiB；請用多個 --path 分批匯出，並提供相關完整檔案。')
        if any(regex.search(diff) for regex in SENSITIVE_CONTENT):
            raise RuntimeError('差異中疑似包含存取憑證，停止輸出；請先檢查與移除機密。')
        title=f'# PR Code Review 證據包（未審查）\n\n'
        title+=f'- Base：`{base}`（`{base_sha}`）\n- Head：`{args.head}`（`{head_sha}`）\n'
        title+=f'- 比較：`git diff {base_sha}...{head_sha}`（三點比較）\n'
        title+='- 注意：此文件**不是** ChatGPT 審查完成證明，也不包含完整程式碼庫；不能取代測試與實機驗收。\n'
        title+='- **分享前請人工檢查差異內容是否有機密、個資或不可公開的程式碼。**\n'
        title+='- CI 結果、規格來源、風險等級與 PR URL：**請另外補入**，不得假定通過。\n\n'
        f1=fence(stat); f2=fence(diff)
        title+=f'## 修改摘要\n\n{f1}text\n{stat}\n{f1}\n\n## 統一差異\n\n{f2}diff\n{diff}\n{f2}\n'
        out=Path(args.output) if args.output else Path('.review-packets')/f'PR_REVIEW_PACKET-{head_sha[:12]}.md'
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(title,encoding='utf8')
        print(f'審查證據包：{out}；Head={head_sha[:12]}；涉及 {len(selected)} 個路徑。')
        print('這不是審查報告。分享前務必人工查看是否包含機密或個資。')
        return 0
    except (RuntimeError,OSError) as e:
        print(f'無法產生審查包：{e}',file=sys.stderr)
        return 2

if __name__=='__main__':
    sys.exit(main())
