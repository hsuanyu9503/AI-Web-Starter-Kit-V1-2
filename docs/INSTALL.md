# 交付包安裝／部署說明

此文件會包含於正式 ZIP 中。每個專案正式發布前請由 Claude Code 更新成當前專案的真實操作步驟。

## ZIP 內容

- `website/`：可部署的靜態網站建置結果；含 `.nojekyll`。
- `docs/`：部署、測試、驗收及版本文件。
- `database/migrations/`：若有 SQL 遷移，只是檔案附錄，**不會自動執行**。
- `VERSION.json`：原始 Git Commit、版號、是否含資料庫備份（固定為否）。
- `SHA256SUMS.txt`：ZIP 內每個附加檔案的 SHA-256 清單。

## GitHub Pages（建議）

本專案標準部署方式是：**驗收 PR → 合併 main → GitHub Actions 自動 build / test / deploy**，不是從 ZIP 解壓後手動覆蓋 GitHub Pages。

1. 確保 Settings → Pages → Source = GitHub Actions。
2. 合併 main 後，至 Actions 檢查 `Pages - 合併 main 後自動部署` 成功。
3. 在真實網址測試主要操作及手機／平板畫面。
4. 若 Actions 需要重新執行，可從 main 手動執行同一個工作流程。

## 一般靜態主機

將 `website/` 資料夾內的**內容**放到網頁伺服器對應目錄；注意子路徑、快取和瀏覽器重新整理路由。

## 版本確認與資料安全

- 請以 `VERSION.json` 中的 Commit SHA 對應 GitHub Tag 與 Release。
- ZIP 只保存部署檔，不含 Git 歷史、私人金鑰或正式資料庫備份。
- 資料庫遷移必須另外核准、備份及測試；還原網頁 ZIP 不代表能還原 Supabase 資料。
