# RELEASE NOTES｜交付版本摘要範本

- 版本：`[待填]`
- Git Commit：`[由正式打包腳本寫入 VERSION.json]`
- 日期：`YYYY-MM-DD`
- 正式驗收證據：`[實際 PR 或 Issue／紀錄連結]`

## 本次新增／修改／修復

- `[內容]`

## 升級注意事項

- `[相容性、SQL、需要的人工作業]`

## 已知限制

- `[內容]`

## 重要提醒

請確認正式發布前已將本範本改為真實內容，並核對 `docs/TEST_REPORT.md`；`VERSION.json` 的 Git SHA 才是 ZIP 的技術版本依據。

> V1.1：正式 Release 不會因 main 自動部署而自動建立。需先完成驗收、核准並合併 main，再人工啟動 GitHub Actions `release.yml`。
