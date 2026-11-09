# AI Web Development Starter Kit · V1.2

**你 × ChatGPT × Claude Code**｜以 GitHub 作為唯一程式碼來源，合併 `main` 後自動部署網站，重要版本才建立 GitHub Release + ZIP。

這是一份可直接上傳 GitHub 的**靜態網頁範本 + 三方協作 SOP**，包含：

- 繁體中文示範網站（`site/`），免安裝外部依賴。
- `CLAUDE.md`：Claude Code 的程式開發、PR、安全與交接守則。
- `docs/`：需求、設計、技術、驗收、交接及自動化設定文件。
- `templates/`：ChatGPT → Claude、Claude → ChatGPT、**Code Review 與修正回覆**、視覺、修錯及發布核准範本。
- `docs/CODE_REVIEW.md`／`docs/RISK_POLICY.md`：L1-L3 風險分級、獨立審查與逐項回覆。
- `scripts/export_review_packet.py`：從固定 Git Commit 匯出 PR 差異供 ChatGPT 查驗（請先人工確認資料安全）。
- `.github/workflows/ci.yml`：PR / main 的自動測試與建置。
- `.github/workflows/pages.yml`：合併 `main` 後自動部署 GitHub Pages，亦可手動重新部署。
- `.github/workflows/release.yml`：你核准後，手動啟動一次，**自動建立新 Tag、Release、ZIP 與校驗檔**。
- Node / Python 腳本：網站建置、結構檢查、ZIP 打包與完整性驗證。

> **注意：下載此套件不會自動連接 Claude Code 或你的 GitHub，不會直接發布網站。** 要先自行建立 Repository、啟用 Pages Actions 與 main 保護規則。完成設定後，才能透過 PR 合併觸發自動部署。

## 最短路徑

1. 先看 [`QUICKSTART.md`](QUICKSTART.md)，建立 GitHub Repo，開啟 GitHub Pages 的 Actions 部署。
2. 啟用 `main` 的 PR／必要 CI 檢查保護；讓 Claude Code 能在授權環境操作這個 Repo。
3. 和 ChatGPT 討論需求，更新 [`docs/SPEC.md`](docs/SPEC.md) 與 [`docs/DESIGN.md`](docs/DESIGN.md)。
4. Claude Code 依 [`CLAUDE.md`](CLAUDE.md) 實作、測試、提交分支並開 PR；提供固定 SHA 的程式差異。
5. ChatGPT 根據 [`docs/CODE_REVIEW.md`](docs/CODE_REVIEW.md) 做適當深度的獨立審查，Claude 逐項修正。
6. 你驗收並核准合併 `main`，Pages 自動建置及上線。**合併即代表允許發布**。
7. 重要穩定版本再更新 Release / Test / Acceptance 文件並啟動 Release Actions，產出 Tag + ZIP + GitHub Release。

## 本機測試

需求：Node.js 22+、Python 3.10+（打包用）、Git。

```bash
npm run check
npm test
npm run build
python3 scripts/package_release.py --version v0.1.0 --draft
python3 scripts/verify_release.py release/*-DRAFT.zip
# 在開發分支上，若有待審 PR：
python3 scripts/export_review_packet.py --base origin/main --head HEAD
```

示範網站源碼在 `site/`，建置檔在 `dist/`。程式沒有直接連接資料庫，也不儲存瀏覽器資料。

## 角色分工

| 角色 | 主要任務 |
|---|---|
| 你 | 產品決策、功能與實機驗收、PR 合併與正式 Release 核准 |
| ChatGPT | 規格、操作流程、UI/UX、視覺素材、**實際程式差異的獨立 Code Review**（資料不足則標示限制） |
| Claude Code | 程式開發、測試、Git 操作、PR、素材與 CSS 整合，依核准流程發布 |
| GitHub Actions | PR 自動測試、`main` 自動部署、核准時產生 Release 與 ZIP |

**兩個 AI 不會自動共享對話內容。** 請用文件、交接單及固定 Git Commit 交接。

## 工作流程和安全底線

- `main` 應透過 GitHub Rulesets 保護：要求 PR、必要狀態檢查 `validate`、禁止強制推送。視帳號和 Repo 支援度設定。
- Claude 不可繞過規則直接改寫 `main`；GitHub 的權限設定才是實際保護。
- 發布 ZIP **不是資料庫備份**，不得含環境金鑰、個資或正式資料匯出。
- Release 不是「每次合併就建立」；它需要人工確認及有效的驗收文件。
- 已有正式網站想導入流程，請先閱讀 [`docs/ADOPT_EXISTING.md`](docs/ADOPT_EXISTING.md)，**勿直接覆蓋既有程式**。

**Code Review：** [`docs/CODE_REVIEW.md`](docs/CODE_REVIEW.md) · [`docs/RISK_POLICY.md`](docs/RISK_POLICY.md) · [`docs/REVIEW_LOG.md`](docs/REVIEW_LOG.md)

**詳細文件：** [`docs/RELEASE_AUTOMATION.md`](docs/RELEASE_AUTOMATION.md) · [`docs/WORKFLOW.md`](docs/WORKFLOW.md) · [`docs/ONE_PAGE.md`](docs/ONE_PAGE.md) · [`docs/DATA_SAFETY.md`](docs/DATA_SAFETY.md)
