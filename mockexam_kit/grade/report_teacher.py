import os, sys, json, html, statistics as st
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'score.py'), encoding='utf-8').read().split("if __name__ == '__main__':")[0])
_pp = os.path.join(WORK, 'prev_totals.json')
E2 = json.load(open(_pp)) if os.path.exists(_pp) else {}
WR_FULL = sum(FULL.values()); PS = PREV_SHORT.replace(' ', ''); ES = EXAM_SHORT.replace(' ', '')
E = html.escape
def f1(x): return f'{x:.1f}'.rstrip('0').rstrip('.') if abs(x - round(x)) > 1e-9 else str(int(round(x)))
def pct(x): return f'{round(x*100)}%'
N = len(STUDENTS)

def subj_stats(sb):
    vals = [x['subj'][sb] for x in STUDENTS]
    mcq = [q for q in KEY if SUBJ[q] == sb]; wq = WR[sb]
    mc = st.mean(sum(x['item'][q]['pts'] for q in mcq) for x in STUDENTS) / (2 * len(mcq))
    wr = st.mean(sum(x['item'][q]['pts'] for q in wq) for x in STUDENTS) / sum(FULL[q] for q in wq)
    same = [x for x in STUDENTS if str(x['seat']) in E2]
    return dict(avg=st.mean(vals), med=st.median(vals), mx=max(vals), mn=min(vals),
                hi=sum(v >= 24 for v in vals), mid=sum(16 <= v < 24 for v in vals), lo=sum(v < 16 for v in vals),
                mc=mc, wr=wr, n2=len(same), e3s=st.mean(x['subj'][sb] for x in same), e2s=st.mean(E2[str(x['seat'])][2][sb] for x in same))

def common_err(q):
    xs = [x['item'][q] for x in STUDENTS]
    if q in FULL:
        d = Counter(it['pts'] for it in xs); nb = sum(1 for x in STUDENTS if W[x['idx']][q][1].startswith(B))
        return f'滿分 {d.get(float(FULL[q]), 0)} 人；0 分 {d.get(0.0, 0)} 人（空白 {nb}）'
    key = KEY[q]
    if q in MULTI:
        L = 'ABCDEF'[:NOPT[q]]
        miss = [(o, sum(1 for it in xs if it['ans'] != '—' and o not in it['ans'])) for o in L if o in key]
        extra = [(o, sum(1 for it in xs if it['ans'] != '—' and o in it['ans'])) for o in L if o not in key]
        parts = [f'漏 {o} {n}' for o, n in sorted(miss, key=lambda t: -t[1]) if n >= 5][:2] + \
                [f'誤選 {o} {n}' for o, n in sorted(extra, key=lambda t: -t[1]) if n >= 5][:2]
        nb = sum(1 for it in xs if it['ans'] == '—')
        if nb >= 3: parts.append(f'空白 {nb}')
        return '、'.join(parts) or '—'
    c = Counter(it['ans'] for it in xs)
    parts = [f'{"空白" if a == "—" else "選 " + a} {n}' for a, n in c.most_common() if a != key and n >= 3][:3]
    return '、'.join(parts) or '—'

def full_n(q): return sum(1 for x in STUDENTS if x['item'][q]['pts'] >= PTS[q] - 1e-9)

def bottom(sb, k=8):
    s = sorted(STUDENTS, key=lambda x: x['subj'][sb]); cut = s[k - 1]['subj'][sb]
    return [x for x in s if x['subj'][sb] <= cut + 1e-9]

CSS = r'''
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK TC', 'Noto Sans TC', sans-serif; color: #1d2433; font-size: 9.2pt; line-height: 1.5;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 10mm 12mm 9mm; position: relative; overflow: hidden; page-break-after: always; }
.page:last-child { page-break-after: auto; }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.2px solid #1f3a5f; padding-bottom: 4px; }
.t1 { font-size: 15pt; font-weight: 700; color: #1f3a5f; }
.t2 { font-size: 8.4pt; color: #5b6475; margin-top: 1px; }
.badge { font-size: 13pt; font-weight: 700; color: #fff; background: #1f3a5f; padding: 2px 12px; border-radius: 5px; }
.kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; margin: 6px 0 2px; }
.kpi { border: 1px solid #d6dce6; border-radius: 5px; padding: 4px 8px; background: #f7f9fc; }
.kpi .l { font-size: 7.6pt; color: #5b6475; }
.kpi .v { font-size: 16pt; font-weight: 700; color: #1f3a5f; line-height: 1.15; }
.kpi .v small { font-size: 8.6pt; color: #5b6475; font-weight: 500; }
.kpi .s { font-size: 7.4pt; color: #5b6475; }
h3 { font-size: 10.2pt; color: #1f3a5f; margin: 6px 0 3px; padding-left: 7px; border-left: 4px solid #2f6fb2; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #d6dce6; padding: 2.4px 5px; }
th { background: #1f3a5f; color: #fff; font-weight: 600; font-size: 8pt; }
td { font-size: 8.5pt; }
.c { text-align: center; } .r { text-align: right; }
.bar { position: relative; height: 9px; background: #eef1f6; border-radius: 3px; }
.bar .f { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 3px; }
.note { font-size: 7.4pt; color: #5b6475; margin-top: 2px; }
.pri { border: 1px solid #d6dce6; border-left: 4px solid #b3261e; border-radius: 4px; padding: 4px 8px 4px 9px; margin: 0 0 5px; background: #fff; }
.pri .h { font-weight: 700; font-size: 9.6pt; color: #1d2433; }
.pri .h .n { display: inline-block; width: 17px; height: 17px; line-height: 17px; text-align: center; border-radius: 50%; background: #b3261e; color: #fff; font-size: 8pt; margin-right: 5px; }
.pri .h .q { font-weight: 500; font-size: 8pt; color: #5b6475; margin-left: 6px; }
.pri .e { font-size: 8.7pt; margin: 2px 0 1px; }
.pri .t { font-size: 8.5pt; color: #1e5b2f; }
.pri .t b { color: #1e7a3c; }
.good { font-size: 8.6pt; background: #f2f9f4; border: 1px solid #cfe7d6; border-radius: 4px; padding: 4px 8px; }
.lo { color: #b3261e; font-weight: 700; } .hi { color: #1e7a3c; font-weight: 700; }
.cg { background: #e3f3e8; } .cy { background: #fff3d6; } .cr { background: #fde4e1; color: #b3261e; font-weight: 700; }
ul.ov { margin: 2px 0 0; padding-left: 17px; } ul.ov li { margin: 2px 0; font-size: 9pt; }
.foot { position: absolute; bottom: 5mm; left: 12mm; right: 12mm; font-size: 7.2pt; color: #8a93a3; display: flex; justify-content: space-between; }
.heat td.hm, .heat th.hm { padding: 0 2px; font-size: 7.3pt; line-height: 1.18; text-align: center; height: 13.6px; }
.it td { padding: 1.2px 5px; font-size: 8pt; line-height: 1.3; }
.it th { padding: 1.6px 5px; }
.heat th.hm { font-size: 7.6pt; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
'''
COLOR = {'物理': '#2f6fb2', '化學': '#7a4fb3', '生物': '#2e8b57', '地科': '#c0702a'}

def rate_cls(r): return 'cg' if r >= 0.75 else ('cy' if r >= 0.5 else 'cr')

def page_overview():
    h = ['<div class="page">']
    h.append(f'''<div class="top"><div><div class="t1">{CLASS_NAME}　{EXAM_SHORT} 自然考科　各科教學加強重點</div>
<div class="t2">{EXAM_TITLE}　滿分 {TOTAL_FULL} 分（物理、化學、生物、地科各 {SUBJ_FULL} 分）</div></div>
<div class="badge">總覽</div></div>''')
    mc_all = st.mean(sum(x['item'][q]['pts'] for q in KEY) for x in STUDENTS) / (2 * len(KEY))
    same = [x for x in STUDENTS if str(x['seat']) in E2]
    h.append(f'''<div class="kpis">
<div class="kpi"><div class="l">到考人數</div><div class="v">{N}<small>／{len(NAMES)}</small></div><div class="s">無答案卷：{"、".join(f"{q:02d}" for q in NO_SHEET) or "無"}</div></div>
<div class="kpi"><div class="l">全班平均</div><div class="v">{f1(CLASS["avg"])}<small>／{TOTAL_FULL}</small></div><div class="s">中位數 {f1(CLASS["median"])}、標準差 {f1(CLASS["sd"])}</div></div>
<div class="kpi"><div class="l">平均級分</div><div class="v">{f1(CLASS["level_avg"])}<small> 級</small></div><div class="s">全國均標 {BENCH["均標"]}、前標 {BENCH["前標"]}、頂標 {BENCH["頂標"]}</div></div>
<div class="kpi"><div class="l">選擇題得分率</div><div class="v">{pct(mc_all)}</div><div class="s">{len(KEY)} 題，共 {2*len(KEY)} 分</div></div>
<div class="kpi"><div class="l">非選擇題得分率</div><div class="v" style="color:#b3261e">{pct(CLASS["written"]/WR_FULL)}</div><div class="s">平均 {f1(CLASS["written"])}／{WR_FULL}</div></div>
</div>''')
    rows = ''
    for sb in SUBJECTS:
        s = subj_stats(sb)
        r = s['avg'] / SUBJ_FULL
        rows += (f'<tr><td class="c"><b style="color:{COLOR[sb]}">{sb}</b></td><td class="r"><b>{f1(round(s["avg"],1))}</b></td>'
                 f'<td><div class="bar"><div class="f" style="width:{r*100:.1f}%;background:{COLOR[sb]}"></div></div></td><td class="c">{pct(r)}</td>'
                 f'<td class="c">{f1(s["med"])}</td><td class="c">{f1(round(s["mn"],1))}～{f1(s["mx"])}</td>'
                 f'<td class="c">{s["hi"]}</td><td class="c">{s["mid"]}</td><td class="c {"cr" if s["lo"]>=5 else ""}">{s["lo"]}</td>'
                 f'<td class="c">{pct(s["mc"])}</td><td class="c {rate_cls(s["wr"])}">{pct(s["wr"])}</td>'
                 f'<td class="c" style="color:#5b6475">{f1(round(s["e2s"],1))} → {f1(round(s["e3s"],1))}</td></tr>')
    h.append(f'''<h3>四科比較</h3>
<table><tr><th style="width:7%">科目</th><th style="width:7%">平均</th><th>得分率</th><th style="width:6%"></th><th style="width:7%">中位數</th><th style="width:10%">最低～最高</th>
<th style="width:7%">≥24 分</th><th style="width:7%">16～24</th><th style="width:7%">＜16 分</th><th style="width:7%">選擇題</th><th style="width:7%">非選擇題</th><th style="width:13%">同 {same and len(same)} 人 {PS}→{ES}</th></tr>{rows}</table>
<div class="note">人數欄為各科得分落在該區間的人數（＜16 分即該科得分率不到 50%）。{PS}→{ES} 為兩次都有作答的 {len(same)} 人該科平均；兩份試卷難度不同，僅供參考（同批 {len(same)} 人總分 {PS} {f1(round(st.mean(E2[str(x["seat"])][0] for x in same),1))} → {ES} {f1(round(st.mean(x["total"] for x in same),1))}，平均級分 {f1(round(st.mean(E2[str(x["seat"])][1] for x in same),1))} → {f1(round(st.mean(x["level"] for x in same),1))}）。</div>''')
    # group rates
    grow = ''
    for nm, qs, sb in GROUPS:
        tot = sum(PTS[q] for q in qs); r = st.mean(sum(x['item'][q]['pts'] for q in qs) for x in STUDENTS) / tot
        grow += f'<tr><td>{nm}</td><td class="c">{sb}</td><td class="c">{tot}</td><td class="c {rate_cls(r)}">{pct(r)}</td></tr>'
    nbl = {q: sum(1 for x in STUDENTS if W[x['idx']][q][1].startswith(B)) for q in FULL}
    brow = ''.join(f'<tr><td class="c">{q}</td><td>{TOPIC[q]}</td><td class="c">{SUBJ[q]}</td><td class="c {rate_cls(CLASS["q"][q])}">{pct(CLASS["q"][q])}</td><td class="c {"cr" if nbl[q]>=8 else ""}">{nbl[q]}</td></tr>' for q in FULL)
    h.append(f'''<div class="two"><div><h3>題組得分率</h3><table><tr><th>題組</th><th style="width:20%">科目</th><th style="width:12%">配分</th><th style="width:15%">得分率</th></tr>{grow}</table></div>
<div><h3>非選擇題得分率與空白人數</h3><table><tr><th style="width:10%">題號</th><th>考點</th><th style="width:13%">科目</th><th style="width:15%">得分率</th><th style="width:13%">空白</th></tr>{brow}</table></div></div>''')
    h.append(f'''<h3>跨科共同問題（建議各科一起提醒）</h3><ul class="ov">
{''.join(OVERVIEW_NOTES)}
</ul>''')
    weak = sorted(QS, key=lambda q: CLASS['q'][q])[:10]
    wrow = ''.join(f'<tr><td class="c">{q}</td><td class="c" style="color:{COLOR[SUBJ[q]]};font-weight:700">{SUBJ[q]}</td><td>{TOPIC[q]}</td><td class="c">{"非選" if q in FULL else ("多選" if q in MULTI else "單選")}</td><td class="c {rate_cls(CLASS["q"][q])}">{pct(CLASS["q"][q])}</td><td class="c">{full_n(q)}</td><td>{common_err(q)}</td></tr>' for q in weak)
    h.append(f'''<h3>全班得分率最低的 10 題</h3><table><tr><th style="width:6%">題號</th><th style="width:7%">科目</th><th style="width:26%">考點</th><th style="width:7%">題型</th><th style="width:8%">得分率</th><th style="width:8%">全對人數</th><th>主要錯誤（人數）</th></tr>{wrow}</table>''')
    h.append(f'<div class="foot"><span>{CLASS_NAME} 自然科　{EXAM_SHORT} 各科教學加強重點</span><span>第 1 頁｜資料：本班 {N} 份答案卷讀卡與非選擇題批改結果</span></div></div>')
    return ''.join(h)

def page_subject(sb, pno):
    s = subj_stats(sb)
    col = COLOR[sb]
    h = [f'<div class="page">']
    h.append(f'''<div class="top"><div><div class="t1">{sb}科　教學加強重點與分析</div>
<div class="t2">{CLASS_NAME}　{EXAM_SHORT} 自然考科（{sb} {SUBJ_FULL} 分：選擇題 {sum(1 for q in KEY if SUBJ[q]==sb)} 題、非選擇題第 {"、".join(str(q) for q in WR[sb])} 題）</div></div>
<div class="badge" style="background:{col}">{sb}</div></div>''')
    h.append(f'''<div class="kpis">
<div class="kpi"><div class="l">班平均</div><div class="v">{f1(round(s["avg"],1))}<small>／{SUBJ_FULL}</small></div><div class="s">得分率 {pct(s["avg"]/SUBJ_FULL)}・中位數 {f1(s["med"])}</div></div>
<div class="kpi"><div class="l">分布</div><div class="v" style="font-size:12.5pt">{s["hi"]}／{s["mid"]}／<span style="color:#b3261e">{s["lo"]}</span></div><div class="s">≥24 分／16～24／＜16 分（人）</div></div>
<div class="kpi"><div class="l">最低～最高</div><div class="v" style="font-size:13pt">{f1(round(s["mn"],1))}～{f1(s["mx"])}</div><div class="s">滿分 {sum(1 for x in STUDENTS if x["subj"][sb]>=32)} 人</div></div>
<div class="kpi"><div class="l">選擇題／非選擇題</div><div class="v" style="font-size:13pt">{pct(s["mc"])}／<span style="color:{"#b3261e" if s["wr"]<0.5 else "#1f3a5f"}">{pct(s["wr"])}</span></div><div class="s">得分率</div></div>
<div class="kpi"><div class="l">同 {s["n2"]} 人 {PS} → {ES}</div><div class="v" style="font-size:13pt">{f1(round(s["e2s"],1))} → {f1(round(s["e3s"],1))}</div><div class="s">不同試卷，僅供參考</div></div>
</div>''')
    h.append('<h3>優先加強重點</h3>')
    for i, (title, qs, ev, tip) in enumerate(PRIOR[sb], 1):
        qtxt = '、'.join(f'第 {q} 題 {pct(CLASS["q"][q])}' for q in qs)
        h.append(f'<div class="pri"><div class="h"><span class="n">{i}</span>{title}<span class="q">{qtxt}</span></div>'
                 f'<div class="e">{ev}</div><div class="t"><b>教學建議：</b>{tip}</div></div>')
    # bottom students (page A), two columns
    bl = bottom(sb)
    def brow(x):
        lost = [q for q in QS if SUBJ[q] == sb and x['item'][q]['pts'] < PTS[q] - 1e-9]
        nb = [q for q in lost if q in x['blanks']]
        ls = '、'.join((f'<u>{q}</u>' if q in nb else str(q)) for q in lost)
        return (f'<tr><td class="c">{x["seat"]:02d}</td><td class="c">{E(x["name"])}</td><td class="c lo">{f1(round(x["subj"][sb],1))}</td>'
                f'<td style="font-size:7.8pt">{ls}</td></tr>')
    half = (len(bl) + 1) // 2
    th = f'<tr><th style="width:12%">座號</th><th style="width:19%">姓名</th><th style="width:15%">本科</th><th>失分題號</th></tr>'
    h.append(f'''<h3>需個別關注：本科得分最低 {len(bl)} 人</h3>
<div class="two"><table>{th}{''.join(brow(x) for x in bl[:half])}</table><table>{th}{''.join(brow(x) for x in bl[half:])}</table></div>
<div class="note">失分題號中加底線者為未作答。各生完整作答見下一頁。</div>''')
    h.append(f'<div class="good" style="margin-top:6px"><b>表現穩定：</b>{GOOD[sb]}</div>')
    h.append(f'<div class="foot"><span>{CLASS_NAME} 自然科　{EXAM_SHORT} 各科教學加強重點｜{sb}（1／2）</span><span>第 {pno} 頁</span></div></div>')
    # page B
    h.append(f'''<div class="page"><div class="top"><div><div class="t1">{sb}科　各題分析與個別學生作答</div>
<div class="t2">{CLASS_NAME}　{EXAM_SHORT} 自然考科</div></div><div class="badge" style="background:{col}">{sb}</div></div>''')
    # item table
    qs = sorted([q for q in QS if SUBJ[q] == sb], key=lambda q: CLASS['q'][q])
    rows = ''
    for q in qs:
        r = CLASS['q'][q]
        rows += (f'<tr><td class="c">{q}</td><td>{TOPIC[q]}</td><td class="c">{"非選 " + str(FULL[q]) + " 分" if q in FULL else ("多選" if q in MULTI else "單選")}</td>'
                 f'<td class="c">{KEY.get(q, "—")}</td><td><div class="bar"><div class="f" style="width:{r*100:.1f}%;background:{col}"></div></div></td>'
                 f'<td class="c {rate_cls(r)}">{pct(r)}</td><td class="c">{full_n(q)}</td><td style="font-size:8pt">{common_err(q)}</td></tr>')
    h.append(f'''<h3>各題得分率（由低到高）</h3>
<table class="it"><tr><th style="width:6%">題號</th><th style="width:25%">考點</th><th style="width:10%">題型</th><th style="width:7%">答案</th><th style="width:13%">得分率</th><th style="width:6%"></th><th style="width:7%">全對</th><th>主要錯誤（人數）</th></tr>{rows}</table>
<div class="note">「漏 X」＝正確選項 X 沒選的人數；「誤選 X」＝選了錯誤選項 X 的人數；只列 5 人以上（單選題列 3 人以上）的錯誤。</div>''')
    # heatmap
    qn = sorted([q for q in QS if SUBJ[q] == sb])
    hd = ''.join(f'<th class="hm">{q}<br><span style="font-weight:400;font-size:6.6pt">{"非" if q in FULL else ("多" if q in MULTI else "單")}{FULL.get(q, 2)}</span></th>' for q in qn)
    rr = ''
    for x in sorted(STUDENTS, key=lambda x: x['seat']):
        cs = ''
        for q in qn:
            it = x['item'][q]; p = it['pts']; full = PTS[q]
            blank = q in x['blanks']
            cls = 'cg' if p >= full - 1e-9 else ('cy' if p > 0 else 'cr')
            txt = '—' if blank else f1(round(p, 1))
            cs += f'<td class="hm {cls}">{txt}</td>'
        rr += f'<tr><td class="c hm">{x["seat"]:02d}</td><td class="c hm">{E(x["name"])}</td><td class="c hm"><b>{f1(round(x["subj"][sb],1))}</b></td>{cs}</tr>'
    rate = ''.join(f'<td class="hm c" style="font-weight:700">{pct(CLASS["q"][q])}</td>' for q in qn)
    h.append(f'''<h3>個別學生各題得分（依座號）</h3>
<table class="heat"><tr><th class="hm" style="width:6%">座號</th><th class="hm" style="width:10%">姓名</th><th class="hm" style="width:7%">本科</th>{hd}</tr>{rr}
<tr><td class="c hm" colspan="3"><b>全班得分率</b></td>{rate}</tr></table>
<div class="note">格內為該題得分；綠＝全對、黃＝部分得分、紅＝0 分，「—」為未作答。題號下方為題型與配分（單＝單選、多＝多選、非＝非選擇題）。</div>''')
    h.append(f'<div class="foot"><span>{CLASS_NAME} 自然科　{EXAM_SHORT} 各科教學加強重點｜{sb}（2／2）</span><span>第 {pno + 1} 頁</span></div></div>')
    return ''.join(h)

def page_matrix(pno):
    h = ['<div class="page">']
    h.append(f'''<div class="top"><div><div class="t1">學生各科得分一覽</div>
<div class="t2">{CLASS_NAME}　{EXAM_SHORT} 自然考科（依座號排列；每科 {SUBJ_FULL} 分）</div></div><div class="badge">附表</div></div>''')
    order = sorted(STUDENTS, key=lambda x: x['seat'])
    rows = ''
    for x in order:
        cells = ''
        for sb in SUBJECTS:
            v = x['subj'][sb]; r = v / SUBJ_FULL
            cells += f'<td class="c {rate_cls(r)}">{f1(round(v,1))}</td>'
        rates = {sb: x['subj'][sb] / SUBJ_FULL for sb in SUBJECTS}
        worst = min(SUBJECTS, key=lambda s: rates[s])
        weak_note = '四科皆滿分' if x['total'] >= TOTAL_FULL else (f'{worst}（{pct(rates[worst])}）' if max(rates.values()) - rates[worst] >= 0.1 else ('四科皆未滿 50%' if max(rates.values()) < 0.5 else '四科平均'))
        rows += (f'<tr><td class="c">{x["seat"]:02d}</td><td class="c">{E(x["name"])}</td><td class="c"><b>{f1(x["total"])}</b></td><td class="c">{x["level"]}</td><td class="c">{x["rank"]}</td>'
                 f'{cells}<td class="c">{f1(x["written"])}</td><td class="c">{weak_note}</td></tr>')
    avg = ''.join(f'<td class="c"><b>{f1(CLASS["subj"][sb])}</b></td>' for sb in SUBJECTS)
    h.append(f'''<table style="margin-top:8px"><tr><th style="width:7%">座號</th><th style="width:11%">姓名</th><th style="width:9%">總分</th><th style="width:7%">級分</th><th style="width:7%">班排</th>
<th style="width:9%">物理</th><th style="width:9%">化學</th><th style="width:9%">生物</th><th style="width:9%">地科</th><th style="width:9%">非選／{WR_FULL}</th><th>相對最弱科</th></tr>{rows}
<tr><td class="c" colspan="2"><b>全班平均</b></td><td class="c"><b>{f1(CLASS["avg"])}</b></td><td class="c">{f1(CLASS["level_avg"])}</td><td></td>{avg}<td class="c"><b>{f1(CLASS["written"])}</b></td><td></td></tr></table>
<div class="note">底色：綠＝該科得分率 ≥75%（24 分以上）、黃＝50～75%、紅＝＜50%（未滿 16 分）。「相對最弱科」為該生四科中得分率最低者（與最強科差距 10 個百分點以上才列出）。無答案卷：{"、".join(f"{q:02d} {NAMES[q]}" for q in NO_SHEET) or "無"}。</div>''')
    h.append(f'<div class="foot"><span>{CLASS_NAME} 自然科　{EXAM_SHORT} 各科教學加強重點｜附表</span><span>第 {pno} 頁</span></div></div>')
    return ''.join(h)

def build(out):
    body = page_overview() + ''.join(page_subject(sb, 2 * i + 2) for i, sb in enumerate(SUBJECTS)) + page_matrix(10)
    doc = f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>{CLASS_NAME} {ES} 自然 各科教學加強重點</title><style>{CSS}</style></head><body>{body}</body></html>'
    open(out, 'w', encoding='utf-8').write(doc)

if __name__ == '__main__':
    build(sys.argv[1])
