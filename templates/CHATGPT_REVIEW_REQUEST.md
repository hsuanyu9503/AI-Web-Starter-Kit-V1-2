# 給 ChatGPT 的 PR 獨立審查請求（直接複製）

請對此 PR 進行獨立 Code Review，而非只重述 Claude 的開發報告。

- Repository／PR：`[URL]`
- Base SHA：`[SHA]`
- Head SHA：`[SHA]`
- 風險初評：`L1／L2／L3`；對照 `docs/RISK_POLICY.md`。
- 需求／設計依據：`[SPEC 與 DESIGN 節點或附件]`
- 可提供的程式：`[GitHub 讀取權限／實際程式檔／review-packet 附件]`
- CI／測試：`[連結或實際輸出]`

請先確認是否有足夠證據做真正的程式碼審查。如只有摘要、圖片或口頭報告，請說明僅能提供有限度審查，並指出需要補充哪些檔案。

有足夠證據時，依 `templates/CHATGPT_CODE_REVIEW.md` 給出檔案位置、具體問題、嚴重程度、重現或反例、建議修正及需要回歸的測試。不需要為了提出問題而捏造問題。對不確定事項請註明未驗證。

先提供審查報告，**不要直接編輯正式程式碼，也不要合併 PR**。
