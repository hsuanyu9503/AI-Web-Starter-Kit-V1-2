# GitHub 自動化與正式發布制度｜Starter Kit V1.2

## 目的：讓 Claude Code 做事、讓 GitHub 執行、ChatGPT 獨立審查、讓你決策

- **Claude Code**：在授權的本機或雲端環境讀取 repository、修改程式、建立開發分支、推送並建立 Pull Request。分支命名：Claude Code 雲端工作分支 `claude/*`、一般人工功能分支 `feature/*`、緊急修復 `hotfix/*`。Claude 的操作權限由你在 Claude 與 GitHub 端設定；本範本不會替你連接帳號。
- **ChatGPT 獨立差異審查**（V1.2）：依 `docs/RISK_POLICY.md` 分級，ChatGPT 依 `docs/CODE_REVIEW.md` 審查固定 Head SHA 的實際程式差異（可用 `scripts/export_review_packet.py` 匯出）；Claude 依 `templates/CLAUDE_REVIEW_RESPONSE.md` 逐項回覆與修正。這是**人工流程關卡**，GitHub Actions 不會自動檢查或強制，也不等於 GitHub 的正式 Approve。
- **GitHub CI**（`.github/workflows/ci.yml`）：每次 PR 與 main 更新，跑 check、test、build。通過不等於完成人工驗收。
- **GitHub Pages**（`pages.yml`）：**PR 合併至 main 後自動觸發**；同一條工作流程重新做 check/test/build，成功才部署。也支援手動重新部署，僅限 `main`。
- **重要版發行**（`release.yml`）：由你確認文件、核准後，在 Actions 的 Release 工作流程手動輸入版本號；它會自動打包 ZIP、校驗 SHA、建立新 Tag 和 GitHub Release，並將 ZIP 與雜湊檔附上。**不會對每次 push 自動產生 Release**。

## 必做一次的 GitHub 設定

1. Repository → Settings → Pages → Build and deployment：**GitHub Actions**。
2. Repository → Settings → Environments → `github-pages`：限制部署分支只允許 `main`（如可用），確認 GitHub Actions 有 Pages 部署權限。
3. Repository → Settings → Rules → Rulesets（或 Branch protection）：保護 `main`、要求 PR、封鎖強制推送，將 CI 的 `validate` 設為必要狀態檢查。請先讓 CI 成功執行一次，待 GitHub 顯示該檢查項目後再設定。視帳號與 Repository 規則支援度調整。
4. **單人專案**：可要求 PR + 狀態檢查，但不要隨意要求「至少一位不同帳號審查者」，否則無第二位審查者時可能無法合併。ChatGPT 的對話確認也不是 GitHub 的 PR review。
5. Workflow Permissions：正式 Release 工作有 job-level `contents: write`，可建立 Release；其他工作僅授權所需權限。如果組織安全政策不允許，需由管理員調整或改成人工發布。
6. 如有個資、金鑰、SQL service role，不能放到 `site/`、Git 或 ZIP；正式資料庫不在此 Actions 中部署。

## 日常 PR 到自動部署

```text
ChatGPT 產出 SPEC / DESIGN + 交接單
   ↓
Claude Code 建立 claude/*（或 feature/*、hotfix/*）→ commit → push → PR（附 L1／L2／L3 初評、Base／Head SHA）
   ↓
CI 自動測試（validate）
   ↓
Claude 匯出固定 Head SHA 的審查證據包 → ChatGPT 獨立差異審查（REV-001…）
   ↓
審查無問題 → 只記錄結果，不需要額外修改或新增 Commit
有問題 → Claude 逐項回覆並修正 → 新 Commit 重跑測試 → ChatGPT 針對新 Head SHA 複驗
（若為記錄審查結果另行提交 Commit，也要檢查新增差異與最新 CI）
   ↓
你和 ChatGPT 看畫面／截圖驗收；審查結果記入 REVIEW_LOG
   ↓
你在 PR 確認通過（必要時更新 ACCEPTANCE）
   ↓
合併 main ＝ 授權自動部署（需要在合併前確認）
   ↓
Pages 自動建置、部署；至 Actions 確認成功及實際網站
```

**風險提醒：** `main` push 是自動部署的觸發器，任何能繞過 PR 直接寫入 main 的人／AI 都可能造成上線。保護 main 是上線前必做的工作，**只寫在 `CLAUDE.md` 並不能技術上阻止誤推送**。

## 重要版 Tag + Release + ZIP

1. 在正式版所在 `main` 上，完成 `docs/RELEASE_NOTES.md`、`docs/TEST_REPORT.md`、`docs/ACCEPTANCE.md`：包含已執行測試的證據、驗收結果、核准者。
2. **必須先把上述文件以 PR 合併至 main**，同一個 main Commit 必須包含已核准文件及要發布的程式碼。不可只在聊天中口頭核准。該 PR 與一般 PR 相同，需依風險等級完成 ChatGPT 差異審查及 Claude 回覆。審查紀錄對應**合併前最新的 PR Head SHA**；審查後若再新增修改，需重新檢查受影響差異與 CI。合併後另行記錄 main Commit SHA 及其對應的 PR；不要求 PR Head SHA 與合併產生的 main Commit SHA 相同。
3. 由你在 Actions → **Release - 核准後建立 Tag + ZIP + GitHub Release** → Run workflow → 選 `main` → 填 `v1.2.0`。工作會再次測試。
4. 若版本已存在、驗收文件未完成、SHA 不符或 Git 工作樹不乾淨，流程必須失敗；不覆蓋舊 Tag 或舊 Release。
5. 自動產生 Tag 和 Release，附件包含 `*-RELEASE.zip` 與 `ZIP-SHA256SUMS.txt`；內部 ZIP 另有 `VERSION.json`／`SHA256SUMS.txt`。
6. 在 GitHub Releases 頁面確認版本、Commit、ZIP，下載作離線備份。**ZIP 不包含 Git 歷史、機密及資料庫正式備份。**

### 哪些動作不是自動的？

- ChatGPT 和 Claude 的對話不會自動互通；以 `docs/`、PR、交接單及指定 Commit 溝通。
- Claude Code 是否能修改 GitHub 依你授權的連線／權限與執行環境而定。
- `main` 合併需你核准；GitHub Rulesets 需要你手動設定。
- 重要版 GitHub Release 需要你手動啟動；一般自動部署不會每次都建立 ZIP。
- 資料庫遷移、備份、還原、正式站實機驗收需要分別規劃。

## 失敗時

- **CI 失敗**：禁止合併，Claude 在原分支修復並重新提交。
- **審查發現 BLOCKER／HIGH**：禁止合併；Claude 在原分支修正、重跑測試，並由 ChatGPT 針對新 Head SHA 複驗。
- **Pages 失敗**：先在 Actions 讀取錯誤；不要用新的未驗收功能「順便修」。若必要以 `hotfix/*` 修復。
- **Release 失敗**：保留現場紀錄，確認是否建立 Tag 或 Release，再檢查原因；**不要直接重跑同版本造成重複或覆蓋**。
- **需要回退**：由 main 建立回復 PR（或核准 hotfix），部署新提交。Tag 不會把 GitHub Pages 自動倒轉；若牽涉 Supabase，需另行檢查資料庫相容性及備份。

## 官方資訊

- GitHub Pages Actions：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- 分支 Rulesets：https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub CLI Release：https://cli.github.com/manual/gh_release_create
