# CHANGELOG｜範本與專案更新紀錄

## [Unreleased]

- 專案未發布的內容依 PR 更新；不得把 Starter Kit 版本視為已部署網站版本。

## [1.2.0] - 2026-11-09（Starter Kit 範本修訂）

### Added
- 三級風險審查、ChatGPT 獨立 Code Review、Claude 逐條修正與回覆制度。
- 新增 REVIEW_LOG、審查／修正範本與固定 SHA 差異包匯出工具。
- PR 模板增加風險、證據、審查結果、使用者合併決策欄位。

### Unchanged
- GitHub `validate`、main 自動 Pages 部署及手動 Release／ZIP 流程保持 V1.1 行為。



## [1.1.0] - 2026-11-08（Starter Kit 範本修訂）

### Changed
- 改為 Claude Code 以 feature/hotfix PR 交付程式，合併 `main` 自動部署 GitHub Pages。
- 用人工啟動的 Release 工作流程，自動建立 Tag、GitHub Release 與可驗證 ZIP。
- 正式打包強制檢查實際驗收與核准者紀錄。
- 更新三方交接與版本管理文件。

> 以上為 Starter Kit 範本自身的變更紀錄，**不是新建立網站的已上線版本**。使用者的新專案發布時應重新撰寫自身的 CHANGELOG。
