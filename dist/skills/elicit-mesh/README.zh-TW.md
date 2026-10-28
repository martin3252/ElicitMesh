# ElicitMesh

[English](README.md) | [繁體中文](README.zh-TW.md)

**透過具體產出與審查，依協作角色萃取專業知識。**

ElicitMesh 是開源的 Agent Skill，協助開發者與領域專家將不完整的說明整理成候選工作流程、輸入／輸出規格、具體草稿及可測試的驗收規則。它**不會**假設 AI 代理就是專業領域的專家。

> 此 Skill 可獨立使用，部分靈感來自 Google 的 [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) 獨立審查模式。本專案不包含 EGM 程式碼或審查提示詞，亦未與 Google 合作或獲其背書。

## 為什麼需要 ElicitMesh

例如，軟體工程師建置法律文件工作流程時，可能先閱讀公開程序資料、繪製流程，再將流程與文件草稿交給律師審查。律師即使不撰寫技術規格，也能指出遺漏的輸入欄位及輸出品質問題。類似的協作模式，也可能出現在工料測量師與工地主管釐清施工文件範圍時。

**ElicitMesh 將這個審查循環整理為可重複使用的流程：**

1. **角色盤點：** 你是誰、與誰合作，以及要共同交付什麼？
2. **從來源到流程：** 提出候選步驟，區分有來源支持的內容與推論。
3. **輸入／輸出規格：** 找出欄位、預期產出、品質要求及尚待確認的問題。
4. **獨立檢視：** 有隔離的審查者時使用獨立審查；否則明確標示為同一脈絡中的檢視。
5. **產出審查：** 建立具體範例，供真正的專家批註。
6. **回饋轉規則：** 將經接受的修正整理為有適用範圍的候選規則及迴歸測試。

## 快速開始

### Codex

若使用支援 `codex plugin` 的新版 Codex CLI，請在終端機執行：

```sh
codex plugin marketplace add martin3252/ElicitMesh
codex plugin add elicit-mesh@elicitmesh
```

開啟新的 Codex 對話並要求它「使用 ElicitMesh」。若有技能選單，可從選單選取；以外掛安裝時也可以輸入 `$elicit-mesh:elicit-mesh`，獨立安裝技能時則使用 `$elicit-mesh`。同一份技能支援英文與繁體中文，YAML 欄位名稱維持英文。外掛只包含本機指令與資源，不需要額外的服務憑證。

若 Codex 版本尚未支援外掛指令，請下載 [skill.zip](https://github.com/martin3252/ElicitMesh/raw/refs/heads/main/dist/skill.zip)，將其中的 `elicit-mesh/` 目錄解壓縮至 `~/.agents/skills/`（個人使用）或 `<你的專案>/.agents/skills/`（專案使用），再開啟新的對話。請擇一安裝，避免重複顯示技能。手動安裝的更新方式：先保留本機修改，再以新版 ZIP 的內容取代該技能目錄。

各環境的細節請參閱官方 [Codex 技能說明](https://developers.openai.com/codex/skills)與[外掛文件](https://developers.openai.com/codex/plugins/build)。

### Claude Code

在 Claude Code 中執行：

```text
/plugin marketplace add martin3252/ElicitMesh
/plugin install elicit-mesh@elicitmesh
```

若系統提示，請重新啟動 Claude Code，接著要求它「使用 ElicitMesh」。也可以輸入 `/elicit-mesh:elicit-mesh` 並接上你的需求，直接呼叫技能。它會以你的語言回覆，支援英文與繁體中文；YAML 欄位名稱則維持英文。

日後更新時，執行 `/plugin marketplace update elicitmesh`，再執行 `/plugin update elicit-mesh@elicitmesh`。

### Claude.ai（上傳自訂技能）

下載 [skill.zip](https://github.com/martin3252/ElicitMesh/raw/refs/heads/main/dist/skill.zip)。在 Claude 的 **Settings → Capabilities → Skills（設定 → 功能 → 技能）** 中上傳為自訂技能並啟用。此功能需要支援的方案，並啟用程式碼執行與檔案建立；工作區管理員也可能限制使用。若介面不同，請參閱 Anthropic 的[最新技能使用說明](https://support.claude.com/en/articles/12512180-using-skills-in-claude)。接著開啟對話並要求 Claude 使用 ElicitMesh。

ZIP 包含技能、參考資料、範例、驗證工具及中英文 README。此安裝方式與 Claude Code 外掛不同；日後更新時，請重新上傳新版 ZIP。

### 其他相容的代理環境

解壓縮 `skill.zip`，依照所用環境的說明，將 `elicit-mesh/` 目錄加入技能庫。指令工作流程本身不需要 Python；選用的結構驗證工具需要 Python 3.10 以上與 PyYAML（見下方）。

### 試用

範例：

```text
使用 ElicitMesh。我是 AI／軟體工程師，正與律師合作開發一個
協助起草不公平解僱申請文件的系統。請盤點角色與知識缺口，
提出包含輸入／輸出規格的工作流程，並產出可供律師審查的
草稿與問題。所有未知的法律要求都必須等待專家確認。
```

另一個領域的範例：

```text
使用 ElicitMesh。我是工料測量師，正與工地主管合作。
我們需要一份可供審查的工程範圍澄清摘要，目前工程數量清單
及圖面版本不完整。請找出缺少的來源及應由誰回答的問題。
不要產生工地指示。
```

如果環境無法存取網頁或檔案，請貼上有權使用的來源摘錄或提供可讀取的本機文件。不得將未造訪的網址視為已審查的證據。

## 產出檔案

| 檔案 | 用途 |
| --- | --- |
| `role-map.yaml` / `.md` | 資訊提供、執行、審查與核准的角色分工 |
| `sources.md` | 連結、日期、章節與來源狀態 |
| `workflow.yaml` / `.md` | 候選節點、決策與交接 |
| `io-contract.yaml` | 輸入欄位、輸出格式及驗收條件 |
| `expert-questions.md` | 依角色排列優先順序的待釐清問題 |
| `sample-output.md` | 可供專家回饋、尚未核准的具體草稿 |
| `review-log.yaml` | 真實專家意見及版本參照 |
| `quality-rules.yaml` | 提議中及經明確核准的可重用規則 |
| `acceptance-criteria.md` | 測試、審查界線及發布前待解問題 |

YAML 範例請見 [references/schema.md](references/schema.md)。

## 驗證範例

建議使用 Python 3.10 以上版本。結構驗證只需要 `PyYAML`。

```sh
python -m pip install -r requirements.txt
python scripts/validate_spec.py examples/legal-unfair-dismissal
python scripts/validate_spec.py examples/construction-scope
python -m unittest discover -s tests -v
```

這些檢查可找出不一致的節點 ID、無效的角色參照、無法追溯來源的 `source_supported` 聲明，或缺少支持資料的 `approved` 狀態。它們**不會**驗證法律要求、契約、施工安全、領域事實是否正確，也不能確認人類是否真的給予核准。任何正式系統都必須另外落實真人簽核與存取控制。

## 維護者打包方式

儲存庫根目錄的技能及資源是唯一維護來源。Codex 使用 `.agents/plugins/marketplace.json` 與 `.codex-plugin/plugin.json`，載入產生的 `dist/skills/elicit-mesh/` 套件；Claude Code 使用 `.claude-plugin/marketplace.json` 的技能套件格式（`strict: false`）註冊根目錄，不需另外建立 Claude 外掛資訊檔。修改發佈內容後，請重新建立兩個納入版本控制的套件：

```sh
python scripts/build_skill.py
python -m unittest discover -s tests -v
```

請將 `dist/skill.zip`、`dist/skills/` 與來源變更一併提交。不要直接編輯產生的檔案；測試會確認它們與維護來源一致。ZIP 使用固定時間戳記，且不包含 Git 資料、本機虛擬環境、快取及市集設定。

## 選用的 EGM 整合

EGM 使用獨立脈絡的審查者檢視草稿，以避免繼承作者的假設。ElicitMesh 在支援的代理環境中可運用此**概念**，但不需要 EGM 也能運作。完整 EGM 外掛須另行安裝；同一對話中模擬的第二意見不得稱為隔離的 Goldfish 審查。

## 隱私與安全

- 不要將機密法律案件、客戶資料或施工文件上傳至未經授權的工具。
- 領域專家核准領域限制，開發者核准技術實作；最終發布權責可能屬於其他角色。
- 不要捏造必填欄位、法律結論、現場測量或安全簽核。
- 範例使用佔位內容，並將專業核准標示為待確認。
- 產出的範例不是可直接提交的文件，也不是進行現場工作的許可。

## 授權與狀態

採用 Apache License 2.0。**v0.1 原型**提供可重用的指令工作流程、範例與結構驗證工具；它不是託管式 SaaS、專業專家系統或自主提交工具。

公開發布前，應保留授權及致謝說明，在至少兩個不同的真實流程上使用適當去識別化資料進行測試，並請貢獻者回報經確認的失敗案例與專家審查結果，而不只是生成文字。
