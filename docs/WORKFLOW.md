# 三方網站開發 SOP｜V1.2

## 基本約定

- **GitHub main Commit 是正式程式碼依據**；設計與需求決策寫入 `SPEC.md` 和 `DESIGN.md`。
- **ChatGPT**：討論與規劃、視覺素材和設計審查；**Claude Code**：正式程式修改與 Git 操作；**你**：驗收、核准 PR 和正式 Release。
- **合併 main ＝ 同意網站自動發布**；重要版 Tag 和 ZIP 由你確認後另行啟動 Release Actions。
- 三方沒有自動共享對話：使用文件、交接單、固定 Commit SHA 傳遞正確資訊。
- 依 `docs/RISK_POLICY.md` 分級 L1／L2／L3；L2/L3 在人工合併前必須執行 **ChatGPT 對實際差異的獨立審查**，並有 Claude 逐項回覆。GitHub CI 無法替代這個關卡。

## 六階段合作 + 三道關卡

| 階段 | 負責 | 產物 | 必要決策 |
|---|---|---|---|
| 1 需求與初步美術 | 你＋ChatGPT | SPEC、DESIGN、交接單 A | 功能、不可變更項、初版視覺方向 |
| 2 技術預審 | Claude Code | TECH、依賴／風險清單 | **關卡 A**：你確認可開工 |
| 3 核心功能 | Claude Code | feature 分支、測試、PR | 需通過 CI 和基本功能測試 |
| 4 獨立審查＋功能驗收 | ChatGPT 獨立審查、Claude 修正、你確認 | REVIEW_LOG、TEST_REPORT、驗收證據 | **關卡 B**：重大問題解除後才做正式視覺整合 |
| 5 美術整合 | ChatGPT 設計、Claude Code 實作 | 正式素材、CSS、動畫、PR | 不得擅改已核准的設計意圖 |
| 6 最終驗收與部署 | 三方 | ACCEPTANCE、合併 main、Pages | **關卡 C**：你同意合併即自動部署 |

小修改可簡化表單；資料庫／登入權限／正式資料操作無論多小都需安全審查。

## 分支與 PR

- `main` 是正式部署來源：使用 GitHub Rulesets 限制直接寫入，至少要求 PR 和 `validate` 成功。
- `claude/<slug>` Claude Code 雲端分支、`feature/<slug>` 人工功能與視覺分支、`hotfix/<slug>` 緊急修復。
- Claude Code 只能對授權 Repository 操作；先檢查 HEAD 與預期基準 Commit。不得以聊天記憶替代指定 SHA。
- PR 應附需求對應、**風險等級**、變更摘要、測試、截圖（若適用）與風險。新 Commit 需重新校對受影響功能。
- **Review Gate**：Claude 提供固定 Base／Head SHA 與修改證據；ChatGPT 按 `docs/CODE_REVIEW.md` 審查，指出未驗證項目；Claude 逐項回應並重跑測試；你確認合併。L1 可用簡化版，L2/L3 需書面紀錄。
- AI 報告不是 GitHub 審查核准，也不會自動成為 GitHub 必要狀態檢查；不能假裝技術上已強制限制。
- 若 PR 不符合要求，改狀態 `需修正`；不可硬推 main 或繞過 GitHub 保護。

## Release 與 ZIP

- `pages.yml` 於 main push 自動部署；`ci.yml` 於 PR/main 檢查。
- `release.yml` 由你手動啟動，它會自動建立 Tag、GitHub Release、ZIP 和外層 SHA-256 清單。
- Tag 對應主分支的 Git SHA；ZIP 裡 `VERSION.json` 有相同 SHA，`SHA256SUMS.txt` 校驗包內各檔。
- 正式 Release 要先完成 `RELEASE_NOTES.md`、`TEST_REPORT.md`、`ACCEPTANCE.md` 並合併 main。完整規範見 [`RELEASE_AUTOMATION.md`](RELEASE_AUTOMATION.md)。
- GitHub 的 Commit、Tag 與 Release 支援可追溯的程式回復；資料庫備份和復原是另一件事。

## 發生異常怎麼做？

- CI 失敗：在 PR 分支修復，不合併。
- Pages 失敗：查 Actions 記錄，必要時開 hotfix；部署成功仍需人工查看實際網頁。
- 版本或文件 SHA 不一致：停止並重新確認 Commit。
- 需求與技術衝突：Claude 說明替代方案、ChatGPT 評估使用與設計、你決策後更新規格。
- 資料庫事故：停止變更、保留紀錄，依專屬備份和復原計畫處理；不要假設 ZIP 可以回復。

## 狀態

`規劃中 → 待開發 → 開發中 → 待驗收 → 可合併 → 已部署`；有問題則進入 `需修正`。重要版可再標 `已建立 Release`。
