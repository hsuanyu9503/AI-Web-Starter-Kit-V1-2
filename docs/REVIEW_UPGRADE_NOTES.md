# V1.2 Code Review 補強導入說明

這份是從 Starter Kit V1.1 升級到 V1.2 的說明；**請勿直接把全套 V1.2 覆蓋已上線的 Repository**。

## 建議做法

1. 先完成目前正在進行的 Release 測試或記錄狀態，避免同時修改發布文件。
2. 在最新 `main` 建立 `claude/upgrade-review-v1-2`（或任意 `claude/*` 開發分支），不要直接修改 `main`。
3. 將升級包內的**新增檔案**放入同一路徑，先確認沒有同名檔要覆蓋。
4. 依 `V1.2-UPGRADE-TASK.md` 指示，讓 Claude 對現有 `CLAUDE.md`、`docs/WORKFLOW.md`、`README.md`、PR template、交接模板和 `package.json` 做**有選擇性的合併**，保留 PR #1 已改過的文字及目前 Release 工作進度。
5. 保持 `ci.yml`、`pages.yml`、`release.yml`、`scripts/package_release.py` 與 `scripts/verify_release.py` 的既有發布行為，不額外建立 GitHub 允許 AI 自動核准的機制。
6. 執行 `npm run check`、`npm test`、`npm run build`，在 PR 檢查 `validate`，再交給 ChatGPT 作第一次真實差異審查；由使用者合併。
7. 合併後檢查 Pages 正常；此 SOP 文件更新可以不建立新 Release。真正的新專案版號由使用者另定。

## 限制

- 審查文件中的「通過」需有實際證據，不可填假資料。
- ChatGPT 只有取得真實差異／程式檔案時才能做 Code Review；AI 的報告不是 GitHub 帳號的 Approve。
- 目前依然靠專案負責人遵守流程；GitHub `validate` 只負責自動技術檢查。
- 差異包可能包含原始碼，請審閱後再分享。禁止把私密資料或金鑰傳到另一個 AI。
