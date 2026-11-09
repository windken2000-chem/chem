# mockexam-kit（學測自然模考批改工具包）

這個分支只放 `mockexam_kit/`：學測自然模考答案卷讀卡、非選擇題批改紀錄、個人成績分析與教師報告 PDF 的產生程式。

- 不含任何學生資料（名單、學號、成績、作答）。範例資料夾只有考試設定與答案卷格子座標，`roster.py` 為虛構範本。
- 使用說明見 `mockexam_kit/README.md`。

```bash
git clone --depth 1 -b mockexam-kit https://github.com/windken2000-chem/chem mockexam_src
cp -r mockexam_src/mockexam_kit .
```
