# 學測自然模考　批改與分析工具包（mockexam_kit）

用一個班的答案卷掃描檔，產出兩份 PDF：
1. **學生個人成績分析**：每人一張 A4 雙面。正面是總分、級分、各科、單元診斷；背面是情況分析、學習建議、選擇題一覽、非選擇題批改。
2. **各科教學加強重點**：總覽 1 頁、每科 2 頁、附表 1 頁。

已在 112 E3（新竹區）與 115 中模（中區）實際批改使用。

> **公開版說明**：本工具包不含任何學生資料。`examples/` 只保留考試設定（答案、配分、單元、格子座標），`roster.py` 是虛構範本，`written/` 只有格式範例。每次批改請另外提供班級名單（座號、姓名；學號可省略），或由答案卷上的座號、姓名辨認後填入。
>
> 取得方式：`git clone --depth 1 -b mockexam-kit https://github.com/windken2000-chem/chem mockexam_src && cp -r mockexam_src/mockexam_kit .`

---

## 資料夾結構

```
mockexam_kit/
  omr/      讀卡：shifts → median → omr → thr → decode；另有核對用的 overlay、mont、zc、names、wcrop
  grade/    計分與報告：mkmc → score → report_student / report_teacher → ovf（檢查溢出）→ topdf
  examples/112E3/   範例工作資料夾（直接當模板複製）
    exam_config.py  ← 本次考試的所有專屬設定（換考試只改這個）
    roster.py       ← 名單、學號（可省略）、答案卷順序（公開版為虛構範本）
    written/w<題號>.py  ← 非選擇題批改結果 {座號: (分數, 說明)}（公開版只有 w_example.py）
    centers.json    ← 答案卷每一格的座標（112E3 新竹區版面）
```

每次考試都有一個工作資料夾 `$MOCK_BASE`，裡面有 `raw/`（掃描頁）、`work/`（設定與中間檔）、`chk/`（核對圖）。程式一律在 `$MOCK_BASE/work` 底下執行。

---

## 使用流程（建議每班開一個新對話）

需要的東西：題本＋詳解 PDF、答案卷掃描 PDF、班級名單（座號、姓名、學號）。可選：上次模考成績、學校讀卡機的選擇題資料。

**0. 準備**
```bash
export KIT=…/mockexam_kit MOCK_BASE=…/exam115E3_306
mkdir -p $MOCK_BASE/{raw,work/written,chk}
pdftoppm -r 300 -gray 答案卷.pdf $MOCK_BASE/raw/s   # 產生 s-01.pgm …
cp $KIT/examples/115C1/{exam_config.py,roster.py} $MOCK_BASE/work/   # 版面相同時再加 centers.json omr_link.json
cd $MOCK_BASE/work
```
看第 1 頁縮圖確認方向。整疊上下顛倒時要 `export MOCK_ROTATE=180`。奇數頁是正面（F），偶數頁是反面（K）；有疑慮時執行 `omr/orient.py` 檢查。

**1. 讀卡**
- 答案卷版面與 112E3 相同：`cp $KIT/examples/112E3/centers.json .`
- 版面不同（最花用量的一步，只需做一次）：先跑 shifts.py、median.py 得到 `med_F.png`、`med_K.png`（去除劃記的空白卷）。接著在 measure.py 的 `ROWS` 填各題列的概略座標，在 centers.py 改 `xa_default`、`SP`（格距）與勾選框座標，再依序跑 measure.py、centers.py。做完後把 centers.json 存回工具包，下次同版面可直接用。
- 依序執行：`python3 $KIT/omr/shifts.py`、`python3 $KIT/omr/median.py`、`python3 $KIT/omr/omr.py`、`python3 $KIT/omr/thr.py`、`python3 $KIT/omr/decode.py`
- 核對：
  - thr.py 會列出劃記最淡的頁，decode.py 會列出接近門檻的格子。
  - `overlay.py <頁> [L|K]` 畫出判讀框（紅＝判為有劃記，橘＝接近門檻）。`mont.py out.png 頁:題 …` 把指定格子拼成一張圖。
  - 判讀有疑慮就寫進 `exam_config.MC_OVERRIDES`。
  - 勾選框題（112E3 的 39、47）在 omr.py、decode.py、thr.py 裡寫死，換考試要改。

**2. 認姓名**：`names.py` 產生簽名欄拼圖，對照後把答案卷順序的座號寫進 `roster.py` 的 `SHEET_SEAT`。

**3. 非選擇題**
- 用 `wcrop.py <題號> 0.3 2 12` 產生拼圖，每張 12 人。版面不同時要改 wcrop.py 的 `BOX`。
- 依詳解的評分原則逐份給分，寫成 `written/w<題號>.py`：`W = {座號: (分數, '批改說明')}`。空白寫 `'未作答'`。
- 同一題的給分標準要一致；把邊界判斷記在說明裡。

**4. 設定與學生報告**
- 修改 `exam_config.py`：
  - 標題、`KEY`、`NOPT`（六選項題）、`FULL`、`SUBJ`、`UNITS`、`TOPIC`
  - `GRADE_UB`：題本所附原始分數與級分對照表的各級上限
  - `BENCH`：五標
  - `UNIT_ADVICE`、`WRITTEN_TIP`
- 依序執行：
  - `python3 $KIT/grade/mkmc.py`
  - `python3 $KIT/grade/score.py`：檢查總分與排名
  - `python3 $KIT/grade/report_student.py $PWD/s.html`
  - `python3 $KIT/grade/ovf.py $PWD/s.html`：要顯示 `overflow []`
  - `python3 $KIT/grade/topdf.py $PWD/s.html 學生報告.pdf`
- 有上次成績時放 `prev_totals.json`（可用上次的工作資料夾跑 score.py 產生），格式為 `{座號: [總分, 級分, {科目: 分數}]}`，報告會自動加上級分比較。

**5. 教師報告**
- 先跑 `grade/stats.py`、`grade/stats2.py`，取得各題錯誤選項人數、各科最低分學生等統計。
- 依統計撰寫 `exam_config.py` 下半部的 `PRIOR`（各科優先加強重點）、`GOOD`、`GROUPS`、`OVERVIEW_NOTES`。每個人數、百分比都要對得上統計輸出。
- 執行 `report_teacher.py`，再跑 ovf.py 確認沒有溢出，最後用 topdf.py 轉成 PDF。

---

## 115 中模（中區）版面與新增功能（115/11 加入）

`examples/115C1/` 是中區 115 中模自然的完整工作資料夾，版面與 112E3 不同（格距 96 px、格框為虛線小框）。同版面直接 `cp examples/115C1/centers.json omr_link.json` 即可讀卡。

- **反面上下顛倒**（雙面掃描常見）：`export MOCK_ROTATE_K=180`，只轉偶數頁；座標、wcrop 圖都會是正的。
- **自動量格子**：`omr/meanimg.py` 先做所有答案卷的平均影像（模板 median 會留下大家都劃的正確答案，量格子改用平均影像），再寫 `rows.json`（每題格子中心的概略 y 與 x 範圍，±25 px 即可），跑 `omr/autogrid.py rows.json` 產生 centers.json。左側 1～36 題可用「區塊起點＋列距」的線性模型補齊偵測不到的列（見 115C1 的 rows.json）。
- **字母印得淡、對位不穩的題**：`work/omr_link.json`＝`{"44": "45"}`，讓第 44 題沿用第 45 題的位移（115C1 的第 44 題需要）。
- **姓名欄**：`export MOCK_NAME_BOX=280,330,1950,980`（115C1 版面）。
- **非選擇題作答區**：寫在 exam_config.py 的 `WBOX`，wcrop.py 會優先使用。
- **報告文字**：exam_config.py 可設 `GRADE_SRC`、`BENCH_SRC`、`GRADE_NOTE`（題本沒附級分對照表時，註明改用哪一年學測級距）、`CHALLENGE_EG`。
- 115C1 題本未附級分對照表，GRADE_UB 用 115 學測自然級距 7.90533、五標 13/12/9/7/5。

## 計分規則（學測）
- 單選：全對 2 分，否則 0 分。
- 多選：n 個選項錯 k 個得 2×(n−2k)/n，最低 0 分。多選題的 k 會把選了 F 這種超出範圍的選項也算進去。
- 級分：依該次題本所附對照表，每科上限寫在 `GRADE_UB`。

## 省用量的做法
- **每班開新對話**：長對話每一步都要重讀全部內容，是主要成本。
- **已有讀卡機的選擇題資料**：直接轉成 `mc.json`（`{答案卷序號: {題號: 答案}}`），可略過步驟 1。
- **老師自己改非選擇題**：只給各題分數，同樣寫成 `written/w*.py`，可略過批改步驟。
- **改用較便宜的模型**：跑程式、產報告這類機械性步驟可用較便宜的模型；手寫辨識與批改建議用高階模型。
- **少看圖**：只看 thr / decode 列出的可疑頁與格子，不要整頁逐張看。

## 需要的環境
python3、numpy、pillow、playwright（chromium）、poppler-utils（pdftoppm）、Noto Sans CJK TC 字型。
