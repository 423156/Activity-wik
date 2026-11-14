# 真實執行與檢查紀錄

## 最後驗收結果

以下記錄使用者要求的三次最後驗收，與下方先前製作階段的修正歷史分開。最後驗收只檢查既有成果，沒有修改 Wiki、evidence、draft 或 HTML；本次交件整理只更新本檔與 submission.md。

| 驗收階段 | 檢查方式 | 實際結果 | PASS / FAIL | 是否需要退回節點 | 是否有修改 |
| --- | --- | --- | --- | --- | --- |
| 程式 validation | 用既有 bundled Python 實際執行 checks/validate.py，直接讀取 JSON 輸出與退出碼 | 11 PASS／0 FAIL；退出碼 0 | PASS | 否 | 無 |
| 獨立 reviewer | 新的獨立 context，唯讀 wiki/、evidence.md、draft.md、deck.html；逐頁檢查忠實度、來源、無依據主張、覆蓋與教學性 | 14 頁全部 PASS；忠實度 14 PASS、來源 14 PASS、教學性 14 PASS；合計 42 PASS／0 REVIEW／0 FAIL；全稿覆蓋 PASS | PASS | 否 | 無 |
| HTML desktop/mobile 實際渲染 | Edge 157.0.4341.46 實際開啟本機 deck.html；逐頁檢視 Desktop 1280×800 與 Mobile 390×844 的原尺寸截圖 | 電腦與手機各 14 張，共 28 個頁面畫面；按頁彙總 14 PASS／0 FAIL | PASS | 否 | 無；只產生工作區驗收截圖與測試輸出 |
| HTML 導覽與執行 | 電腦與手機各測全部向前／向後切換，另測方向鍵、Home／End、選頁、深連結與首末頁按鈕狀態 | 各 26 次、合計 52 次前後頁切換正常；其他導覽測試通過；無 JavaScript 執行錯誤 | PASS | 否 | 無 |

所有檢查通過，沒有觸發退回節點，也沒有因驗收結果重新生成內容。

上述結論限於這次最後驗收；不能解讀為先前製作過程從未發現問題。先前真實發生的擷取遺漏與 draft 局部修正仍保留在下方，不刪除也不計入本次最後驗收的 FAIL。

程式的 11 項為：必要檔案、可讀來源數、來源清單、原檔指紋、source ID 有效性、HTML 結構、頁數、頁 ID 唯一性、空白頁、頁面來源、draft／HTML 內容一致性。此次重跑的實際結果為 9 份可讀來源、14 頁簡報，無缺檔、無無效來源、無內容差異。

新的獨立 reviewer 未繼承原作者對話，只依指定資料審查；來源 PASS 表示與 Wiki／evidence 的映射一致，不表示這次另行核對 raw。無依據主張納入忠實度，覆蓋率另外確認，未發現重要 Wiki 內容的實質遺漏。

視覺驗收逐頁結果：01–14 頁均 PASS。標題、內文與來源可讀，無 overflow、clipping、重疊或無法操作。電腦版留白較多但不影響閱讀；手機第 13 頁文件高 846px、視窗高 844px，可自然捲動且無裁切，不判 FAIL。另有 768×1024 平板尺寸的幾何檢查，未混入上述 28 張電腦／手機逐頁截圖數量。

本機驗收截圖位於工作區 work/html-qa/desktop-01.png 至 desktop-14.png，以及 mobile-01.png 至 mobile-14.png。最新 browser-results.json 與本次工具執行輸出保留瀏覽器結果；早先的 work/validation-results.json 為製作階段輸出，本次 validation 重跑直接回傳結果，沒有另寫新檔。

## 先前製作階段紀錄（保留歷史）

本次續作日期：2026-11-12。Round 0 為先前缺資料的停止，不計為修正輪；本次 Round 1 為首輪產出及檢查。每個問題最多 2 次修正、整體最多 3 輪。來源本身的疑義與生成錯誤分開記錄。

| Round | Check | Result | 問題 | 退回節點 | 修改 |
| --- | --- | --- | --- | --- | --- |
| 0 | 前次 Gate A | STOP | raw 為 0 份 | 資料 | 停止，使用者本次補入資料 |
| 1 | 本次 Gate A | PASS | 9 個可讀檔案；手冊雙格式不是兩份獨立證據 | 無 | 排除一份手冊仍有 8 份，不靠重複格式湊數 |
| 1 | ingest 文字擷取完整性 | FAIL → 修正後 PASS（主題範圍） | S05 投影片 2、3、8 的工作期限、流程、財務資料在圖片內，純文字擷取遺漏；首次在 ingest 圖片盤點發現 | ingest | 補讀圖片並寫入 W02、W05、W06、W07；局部修正 1 次，未重做其他來源；在 Wiki 生成前加入圖片盤點 |
| 1 | 閱讀工具可用性 | FALLBACK | fitz 未安裝，圖片檢查腳本首次執行失敗 | 讀取工具 | 改用已存在的 Poppler 渲染 S03 p.7–9；未安裝套件，不影響來源內容 |
| 1 | 來源衝突核對 | PASS（已標記） | S06／S07 日期、地點、學期及費率不一致；S03 預算／人數口徑／時長有疑義 | Wiki | W04–W06 並列待確認，未擅自更改來源；此為原始資料問題，不是生成錯誤 |
| 1 | Wiki → evidence | PASS | 無 | 無 | E01–E17 均對應 W01–W09，未引入外部主張 |
| 1 | Outline 順序、覆蓋與來源 | PASS | 無 | 無 | 14 頁涵蓋必要主題及限制，未重寫 |
| 1 → 2 | 獨立 reviewer 初審 | FAIL | draft 第 07 頁自行把保險數量寫成人數；第 14 頁會議日期未進入 Wiki／evidence，超出該階段允許輸入 | draft | 局部修正 1 次：改回「保險數量 155」及「兩次系學會會議資料」，其餘通過內容不重寫 |
| 1 → 2 | S08 空白文字頁結構複核 | FAIL | 第 6 頁其實有群組內文字，先前錯判只有標題；首次在檢查 shape type 時發現 | ingest → Wiki／evidence → draft 第 13 頁 | 擷取完整性第 2 次修正：遞迴讀群組，補勘場、雨備、護理站說明；不改其餘已通過頁面 |
| 2 | 獨立 reviewer 局部複查 | PASS | 無殘留必要修正 | 無 | 第 07、13、14 頁通過；合併前次已通過部分，draft 語意審查 PASS |
| 2 | HTML 生成 | DONE | 無 | 無 | 只讀通過的 draft 生成 14 頁，未重寫教學內容 |
| 2 | 瀏覽器啟動 | RETRY → PASS | 沙箱內 Edge 啟動遭 EPERM | 瀏覽器啟動 | 以允許的權限啟動本機無介面 Edge，未安裝套件；此為環境重試，不是內容修正 |
| 2 | 瀏覽器幾何與導覽檢查 | PASS | 無明顯 overflow／clipping；無 JavaScript 錯誤 | 無 | Edge 157.0.4341.46；1280×800、768×1024、390×844，各 14 頁共 42 頁面狀態通過；9 項導覽／列印可見性測試通過 |
| 2 | 版面目視檢查 | PASS（已檢視範圍） | 無明顯裁切或重疊 | 無 | 檢視桌面／手機各 14 頁截圖總覽，另原尺寸檢視桌面第 08 頁與手機第 13 頁；未因此修改 HTML |
| 2 | checks/validate.py 實際執行 | PASS：11 項、0 FAIL，退出碼 0 | 無 | 無 | 9 份資料可讀；11 個必要檔案存在；S01–S09 與原檔指紋一致；14 頁結構完整、頁 ID 唯一、無空白頁、每頁有來源；draft 與 HTML 全部內容逐欄相同 |

## 檢查提前的實際決定

純文字擷取遺漏圖片資訊已在 ingest 階段實際發生，群組文字漏讀則在 draft 審查期間的來源結構複核發現。故把「圖片盤點／群組遞迴讀取／空白文字頁複核」放入 Wiki 生成前的小 Loop，並同步寫入 AGENTS.md。維持已確認 Graph 的主要節點，不新增獨立大節點。發現原始資料衝突時先在 Wiki 標記，後續 draft 沿用，不等 HTML 才補救。

## 獨立審查證據

使用全新 context 的 reviewer 子代理，未繼承主流程聊天；僅提供 Wiki/index.md、evidence.md、draft.md 及目標讀者／審查要求，不提供 raw。初審忠實度及無根據主張 FAIL，覆蓋率及讀者適切性 PASS；具體問題為第 07 頁保險單位推定、第 14 頁不在 Wiki 中的會議日期。局部修正後，以相同獨立 reviewer 複查第 07、13、14 頁，結果 PASS。它無法發現 Wiki 與 evidence 同步漏掉的原始資料，因此來源擷取完整性必須在上游另查。

## 可重跑的客觀驗證

從專案根執行 `python checks/validate.py`（需要現有 pypdf）。程式僅讀檔，輸出 JSON 與退出碼，來源指紋可查出原檔是否改變；可讀檔案數不等於已完整讀取圖片。source ID 存在檢查也不等於語意忠實度檢查。

本次使用已提供的 bundled Python 實際執行，結果：`passed=11, failed=0`。檢查名稱為 required_files、raw_readable_count、source_manifest、source_hashes、all_source_ids_exist、html_structure、slide_count、unique_slide_ids、no_blank_slides、content_slide_sources、draft_html_exact_content。原始 JSON 保留在工作區 work/validation-results.json；沒有把尚未完成的人工審查算成 PASS。

瀏覽器測試涵蓋水平溢出、文字容器寬度、祖先裁切、前後頁、方向鍵、Home／End、選頁、深連結及列印時全部 14 頁可見。手機第 13 頁文件高度 846px，視窗 844px，允許自然捲動且無裁切；沒有用隱藏內容消除溢出。測試腳本與截圖保留在工作區 work/html-qa 與 work/browser_check.cjs，並非新增的交付文件。

## 交件狀態與成果範圍

程式客觀驗證、新獨立 reviewer 逐頁審查與 desktop/mobile 實際渲染均已通過，使用者已要求進入紀錄與交件整理。可以進入交件階段，沒有待修正的驗收 FAIL。未執行真人學習成效測試，不將 AI 審查視為此類測試。資料沒有完整申請／核准、核銷操作、應變程序或完整事後檢討，故「能獨立完成所有類型活動」仍不在可證明範圍。

製作階段共 2 輪，擷取完整性修正 2 次，draft 語意問題各修正 1 次，HTML 生成 1 次、無內容或排版重生。最後驗收沒有新增修正輪，也未因仍有額度而重做已通過內容。公開 GitHub／Wiki／HTML 網址尚未提供；交件檔先保留實際本機相對路徑，若老師要求公開連結或截圖，由使用者補上。
