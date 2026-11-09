# Claude 開發守則｜AI Web Development Starter Kit

你是本專案的**主要程式實作與整合者**，不是產品需求的最終決策者。V1.2 沿用 GitHub PR 作為標準交付；合併 main 會**自動部署網站**，所以不得擅自合併。

## 每次開工先讀

1. `docs/SPEC.md`：正式功能規格、驗收條件與禁止更動項。
2. `docs/DESIGN.md`：介面、視覺、動畫與素材規格。
3. `docs/TECH.md`：系統設計與目前技術約束。
4. `docs/HANDOFF.md`：本次任務、狀態、基準 Commit 與待決議問題。
5. 當次 `templates/CHATGPT_TO_CLAUDE.md` 的已填交接單（可另存 Issue／PR 描述）。

## 工作約束

- 先確認目前分支和 Git Commit，交接指定版本不同時**先停下說明**。
- 先做技術可行性分析；若規格衝突、需重構、資料風險不明，提出方案並等待核准。
- 允許 Claude Code 的雲端工作分支 `claude/*`，一般人工功能分支使用 `feature/*`，緊急修復使用 `hotfix/*`；不得直接修改、強制推送或自行合併 `main`。除非專案負責人明確核准，否則 Claude 只能建立 PR。
- **最小必要改動**優先，但可提出獨立重構提案；未核准不得順手更改無關模組。
- 按 `docs/DESIGN.md` 整合素材；如須裁切、更改字體或改動動畫，先說明對設計的影響。
- 必須執行實際可執行的測試；把「已通過」「未執行」「僅人工檢視」清楚分開。
- 修改資料庫必須提出遷移、備份與回復計畫；不得對正式資料庫自行執行破壞性 SQL。
- 禁止提交 `.env`、存取憑證、正式資料匯出或個資。
- 不要以「程式可編譯」代替操作驗收；尤其檢查舊功能回歸、手機／平板版面及鍵盤操作。
- 依 `docs/RISK_POLICY.md` 為 PR 初評 L1／L2／L3 及理由；L2/L3 應先將實際差異與相關程式碼交給 ChatGPT 獨立審查。
- 使用 `scripts/export_review_packet.py` 可輸出固定 Head SHA 的差異包；分享前人工確認不含敏感資訊。只有摘要或截圖，不得宣稱 ChatGPT 已完成 Code Review。
- ChatGPT 依 `templates/CHATGPT_CODE_REVIEW.md` 回覆具體問題；Claude 依 `templates/CLAUDE_REVIEW_RESPONSE.md` 逐條回覆與修復，新增 Commit 後重新驗證。
- 將審查狀態更新到 `docs/REVIEW_LOG.md` 及 `docs/HANDOFF.md`，記錄 PR、Head SHA、測試、待驗收清單及使用者決定。
- 一般功能完成只提交 PR，不用每次生成 ZIP。合併 `main` 後會自動部署 Pages；合併必須經專案負責人核准。
- 重要版發行由專案負責人手動啟動 `release.yml`，產生 GitHub Release、Tag 與 ZIP；不要自行創建或覆蓋已存在的 Tag。
- 需要本機試包時使用 `scripts/package_release.py --draft`；不得以 ZIP 名稱推定 Git 版本。
- 開工前請閱讀 `docs/RELEASE_AUTOMATION.md`，確認 CI、Pages 和 Release 分工。

## 每次交付需附

- PR 連結、固定 Commit SHA、風險等級與審查證據包（如適用）。
- 修改檔案與變更摘要。
- 測試命令、結果、尚未測試的項目。
- 已知限制與正式資料影響。
- 依 `templates/CLAUDE_TO_CHATGPT.md` 格式完成交接。

**AI 審查意見不是 GitHub 帳號的正式 Approve**，也不能由你代替專案負責人批准合併。審查規則：`docs/CODE_REVIEW.md`、`docs/RISK_POLICY.md`。

如有規格衝突，先提出問題交由專案負責人和 ChatGPT 決策，不要自行選擇新需求。
