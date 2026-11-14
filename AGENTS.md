# 1. Goal
主題：第一次辦活動：從企劃到執行與檢討。對象為想舉辦大學活動的人，包含初次籌辦者。以中文、親切清楚的學長姊教學風格，讓讀者知道各階段該做什麼，支持獨立作業。涵蓋迎新等大學活動的共通流程，特殊要求僅依資料呈現。

# 2. Source rules
只使用 raw/，至少 5 份可讀資料，類型不限，一批 ingest。逐份編列唯一 ID（S01、S02……），在 workflow/sources.md 記錄 ID、檔名或來源名稱、主要內容及 ingest 是否成功；保留可取得的頁碼或段落位置。不得用模型知識補足。
矛盾說法並列並標示適用情境；無法釐清時標記「待確認」，不自行選擇答案。

# 3. Wiki rules
依資料與活動階段安排實際章節，不預設固定章節。重要內容須可追溯 source ID。wiki/index.md 為入口，每份 ingest 寫入 wiki/log.md。workflow/evidence.md 只整理 Wiki 已有內容，以 Claim、Source ID、Evidence / Summary、用途為欄位。

# 4. HTML rules
教學簡報為 10–15 頁（含封面與來源頁），提供上一頁／下一頁、鍵盤導覽、響應式版面與清楚視覺層級。主要教學內容標示 source ID。
outline 只依 Wiki 與 evidence；draft 只依通過的 outline 與對應 evidence；deck.html 只依通過的 draft，僅作排版，不新增或改變事實。

# 5. Workflow
資料 → Wiki → 檢查關卡 → 教學內容 → 檢查關卡 → HTML → 檢查 → 完成。
Gate A 先確認資料數與可讀性；Wiki 檢查追溯與衝突處理後整理 evidence；outline 檢查順序與必要重點後產生 draft；獨立 reviewer 審查 draft 後製作 HTML。
本次實測後提前的檢查：ingest 在 Wiki 生成前盤點圖片、遞迴讀取群組物件，複核僅擷取到標題的頁面；不能以頂層文字擷取結果推論原頁空白。
漏讀或誤讀退回對應 Wiki；evidence 錯誤只修 evidence；缺主題檢查 Wiki／evidence；順序問題只修 outline；draft 問題只修對應段落，根源在上游才退回上游；HTML 內容或版面問題只修對應頁面。
workflow/report.md 以 Round、Check、Result、問題、退回節點、修改記錄真實結果、問題首次發現位置及是否提前檢查。submission.md 整理主題、Wiki 與 ingest 數、HTML、Mermaid Graph 與節點輸入輸出／退回設計、實際檢查、依事實撰寫的反思。

# 6. Validation
checks/validate.py 檢查 raw 可讀資料數至少 5、必要檔案存在、使用的 source ID 有效、HTML 頁數 10–15、主要內容頁來源、基本結構與非空白頁。比對 HTML 與通過的 draft，避免排版改變內容。
使用獨立新 context reviewer，只提供 Wiki／evidence 與 draft 或 HTML，審查忠實度、來源覆蓋、無根據內容及讀者適切性；讀者與教學目標隨審查要求提供。無法使用時標記「需人工 / 新對話審查」並提供最短 reviewer prompt。
有現成瀏覽器或 rendering 工具則檢查 overflow／clipping；否則記錄「需人工檢查：HTML overflow」，不安裝大型套件。人工確認實際可用性；未完成檢查列為待辦，不宣稱通過。

# 7. Retry / stop rules
每輪：產出 → Validation → 只修 FAIL → 再檢查。PASS 不重寫；每個問題／局部 Loop 最多修正 2 次，整體最多 3 輪；達上限停止並記錄。無法驗證不得猜測，不虛構執行或刻意製造錯誤。不建立無用途檔案。
Gate A 少於 5 份可讀資料立即停止，只回報「資料不足：目前 X 份，還需要 X 份。」
