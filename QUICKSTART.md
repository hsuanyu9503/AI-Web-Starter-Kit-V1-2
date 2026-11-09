# 第一次啟用｜AI Web Development Starter Kit V1.2

## 1. 建立 GitHub Repository

解壓縮套件，將資料夾改成專案名稱。在 GitHub 建立一個空白 Repository，再執行：

```bash
git init -b main
git add .
git commit -m "chore: init AI web starter"
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPO.git
git push -u origin main
```

請替換 `YOUR_ACCOUNT` 和 `YOUR_REPO`。可用 GitHub Desktop 或由已取得權限的 Claude Code 協助完成。首次推送前，確認沒有私人金鑰、資料庫資料或測試個資。

若想重複建立網站，可將此 Repo 設為 GitHub Template Repository。

## 2. 啟用 GitHub 的保護與自動部署

**這是一次性人工設定，Starter Kit 本身無法代替你完成。**

- Settings → Pages → Build and deployment → Source：選 **GitHub Actions**。
- Settings → Environments → `github-pages`：限制可部署分支為 `main`（如支援），並確認 Pages 部署權限。
- Settings → Rules → Rulesets（或 Branch protection）：對 `main` 要求 PR、禁止 force push、要求 CI `validate` 通過。
- CI 首次執行成功後，才容易在保護規則選單中選到 `validate`。
- 單人 Repository 不宜設定「必須有另一名審查者核准」而沒有第二位審查者；ChatGPT 對話確認不能代替 GitHub 審查身分。

**重要：** 每次推送或合併到 `main` 都會觸發 Pages 部署；確認分支保護正確後，再允許 Claude Code 操作。

## 3. 連接 Claude Code

在你使用的 Claude Code 本機或雲端介面，授權操作此 GitHub Repository（授權方式以當前 Claude Code 介面為準）。`CLAUDE.md` 是專案規範，**不是連線憑證**。

讓 Claude Code 先閱讀 `CLAUDE.md`、`docs/SPEC.md`、`docs/DESIGN.md`、`docs/TECH.md`、`docs/HANDOFF.md`。完成需求審查後，它應在 `claude/...`、`feature/...` 或 `hotfix/...` 分支作業，建立 PR 而非直接改動 main。

## 4. 與 ChatGPT 討論功能

更新 `docs/SPEC.md` / `docs/DESIGN.md`，依 `templates/CHATGPT_TO_CLAUDE.md` 填寫交接單。美術製作使用 `templates/VISUAL_HANDOFF.md`，交接要指定目標版本／Commit。

將文件交給 Claude Code。正式決策寫回 GitHub 文件，避免聊天中不同方案混淆。

## 5. PR → 驗收 → main 自動部署

- Claude Code 編碼並執行：`npm run check`、`npm test`、`npm run build`。
- Claude 建立 PR；GitHub CI 自動測試，Claude 提供固定 Head SHA、程式差異包與交接摘要。
- 依 `docs/RISK_POLICY.md` 判級；ChatGPT 對 PR 實際差異進行獨立 Code Review（L1 簡化；L2/L3 書面審查），Claude 逐條處理問題。
- 你與 ChatGPT 檢查功能、視覺、手機平板版面。必要時修正 PR，再重新驗收。
- 你核准合併到 `main` 後，`.github/workflows/pages.yml` **自動部署**。
- 到 Actions 確認 `Pages - 合併 main 後自動部署` 成功，再打開實際網址檢查。

> 首次把範本推上 `main` 也會觸發 Pages（前提是已開啟 Pages Actions）。若不希望示範網站公開，請先確定 Repository 可見性與 Pages 設定，再推送／啟用。

## 6. 重要版本：Tag + GitHub Release + ZIP

這不是每次功能更新都要做。當你決定要發行穩定版：

1. 先在 PR 中更新 `docs/RELEASE_NOTES.md`、`docs/TEST_REPORT.md`、`docs/ACCEPTANCE.md`；**實際驗收通過、核准者簽認、核對版本後合併 main**。
2. 在 GitHub → Actions → **Release - 核准後建立 Tag + ZIP + GitHub Release** → Run workflow，選 `main` 並輸入 `v1.0.0` 等新版本號。
3. Actions 重新跑測試、建立 ZIP、驗證 SHA-256、確認版號未被使用，再由 GitHub CLI 建立 Tag 和 GitHub Release 並上傳 ZIP / 校驗檔。
4. 到 GitHub Releases 下載 ZIP 備份，確認 Tag 指向當次 main Commit。

**正式 Release 會拒絕空白或尚未驗收的模板文件。** ZIP 不包含正式資料庫備份。

## 7. 本機試跑（選用）

環境：Node.js 22+、Python 3.10+。範本不需安裝 npm 相依套件。

```bash
npm run check
npm test
npm run build
python3 scripts/package_release.py --version v0.1.0 --draft
python3 scripts/verify_release.py release/*-DRAFT.zip
```

更多說明：`docs/RELEASE_AUTOMATION.md`、`docs/WORKFLOW.md`、`docs/DATA_SAFETY.md`。
