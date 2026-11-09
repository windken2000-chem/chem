# 班級名單範本（請依實際名單改寫；此處為虛構資料）
# SHEET_SEAT：答案卷 PDF 裡的順序對應的座號（names.py 拼圖對照後填入）
SHEET_SEAT = [3, 1, 2]
NAMES = {1: '王小明', 2: '李小華', 3: '陳小美', 4: '林小強'}
NO_SHEET = sorted(set(NAMES) - set(SHEET_SEAT))
# 學號可省略；有填才會印在報告上
STUDENT_ID = {1: 'S001', 2: 'S002', 3: 'S003', 4: 'S004'}
