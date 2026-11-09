import os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'score.py'), encoding='utf-8').read().split("if __name__ == '__main__':")[0])
import json as _j
_pp = os.path.join(WORK, 'prev_totals.json')
E2 = {int(k): v for k, v in _j.load(open(_pp)).items()} if os.path.exists(_pp) else {}
P1_FULL = sum(PTS[q] for q in P1_QS); P2_FULL = TOTAL_FULL - P1_FULL; WR_FULL = sum(FULL.values())
_g = globals()
GRADE_SRC = _g.get('GRADE_SRC', '依題本所附級分對照表')
BENCH_SRC = _g.get('BENCH_SRC', '題本所附全國五標')
GRADE_NOTE = _g.get('GRADE_NOTE', '級分僅供參考：依該次模考全國考生之原始分數對照表換算')
CHALLENGE_EG = _g.get('CHALLENGE_EG', '如本次第 55～60 題的毛藻研究')
SIXNOTE = ''.join(f'（第 {q} 題六個選項，每錯一個扣 0.67 分）' for q in sorted(KEY) if NOPT[q] == 6 and q in MULTI)

def f1(x):
    return f'{x:.1f}'.rstrip('0').rstrip('.') if abs(x - round(x)) > 1e-9 else str(int(round(x)))
def pct(x): return f'{round(x*100)}%'
E = html.escape

def bench_text(lv):
    for nm, v in BENCH.items():
        if lv >= v: return f'達全國{nm}（{v}級）'
    return f'未達全國底標（{BENCH["底標"]}級）'

def analysis(x):
    out = []; adv = []
    diff = round(x['total'] - CLASS['avg'], 1)
    rel = f'高於班平均 {f1(diff)} 分' if diff > 0 else (f'低於班平均 {f1(-diff)} 分' if diff < 0 else '與班平均相同')
    out.append(f'總分 <b>{f1(x["total"])}／{TOTAL_FULL}</b>，約 <b>{x["level"]} 級分</b>，班排 {x["rank"]}／{CLASS["n"]}，{rel}；{bench_text(x["level"])}。')
    e2 = E2.get(x['seat'])
    if e2:
        dl = x['level'] - e2[1]
        tr = f'進步 {dl} 級' if dl > 0 else (f'退步 {-dl} 級' if dl < 0 else '級分持平')
        out[-1] = out[-1][:-1] + f'；上次 {PREV_SHORT} 為 {f1(e2[0])} 分（{e2[1]} 級），本次{tr}。'
    else:
        out[-1] = out[-1][:-1] + (f'；{PREV_SHORT} 無作答卷，無法比較。' if E2 else '。')

    if x['total'] >= TOTAL_FULL - 1e-9:
        out.append(f'四科、{len(UNITS)} 個單元全部滿分：選擇題 {len(KEY)} 題全對，非選擇題 {len(FULL)} 題都寫出評分要點（{WR_FULL}／{WR_FULL}）。')
        adv = ['<b>維持手感</b>：每週固定寫一回完整的自然模擬試題，維持 110 分鐘的作答節奏與檢查習慣。',
               '<b>非選擇題表達</b>：本次各題都寫到評分要點，繼續保持「先寫結論、再寫依據（數據或原理）」的寫法。',
               f'<b>延伸挑戰</b>：多練探究與實作題組和跨科閱讀素材（{CHALLENGE_EG}），保持對新情境的熟悉度。']
        return out, adv
    rates = {sb: x['subj'][sb] / SUBJ_FULL for sb in SUBJECTS}
    best = max(SUBJECTS, key=lambda s: rates[s]); worst = min(SUBJECTS, key=lambda s: rates[s])
    if rates[best] - rates[worst] < 0.08:
        out.append(f'四科表現平均（{pct(rates[worst])}～{pct(rates[best])}），沒有特別偏弱的科目。')
    else:
        d = x['subj'][worst] - CLASS['subj'][worst]
        out.append(f'四科中<b>{best}</b>最穩（{pct(rates[best])}），<b>{worst}</b>最弱（{pct(rates[worst])}，'
                   f'{"比班平均少 " + f1(-d) + " 分" if d < 0 else "仍高於班平均"}）。')
    us = [(u[3] / u[4], u) for u in x['units']]
    weak = sorted([t for t in us if t[0] < 0.6 and t[1][4] >= 4], key=lambda t: -(t[1][4] - t[1][3]))
    strong = sorted([t for t in us if t[0] >= 0.85 and t[1][4] >= 6], key=lambda t: -t[0])
    if strong:
        out.append('強項單元：' + '、'.join(f'{u[1]}（{pct(r)}）' for r, u in strong[:3]) + '。')
    if weak:
        parts = []
        for r, u in weak[:3]:
            missed = [q for q in u[2] if x['item'][q]['pts'] < PTS[q]]
            parts.append(f'{u[1]}（{pct(r)}；失分題 {"、".join(str(q) for q in missed[:6])}）')
        out.append('<b>失分集中</b>在：' + '；'.join(parts) + '。')
    elif x['total'] < TOTAL_FULL:
        lost = [q for q in QS if x['item'][q]['pts'] < PTS[q]]
        out.append('沒有得分率低於 60% 的單元；失分題為 ' + '、'.join(str(q) for q in lost[:10]) + '。')
    habits = []
    nb = len(x['blanks'])
    if nb >= 4: habits.append(f'有 <b>{nb} 題未作答</b>（' + '、'.join(str(q) for q in x['blanks'][:10]) + (' 等' if nb > 10 else '') + '）')
    elif nb: habits.append(f'未作答 {nb} 題（' + '、'.join(str(q) for q in x['blanks']) + '）')
    mp = x['multi_partial']
    if len(mp) >= 5: habits.append(f'多選題有 {len(mp)} 題只拿部分分數，選項判斷不夠確定')
    wr = x['written']
    habits.append(f'非選擇題得 {f1(wr)}／{WR_FULL}（班平均 {f1(CLASS["written"])}）')
    out.append('作答情形：' + '；'.join(habits) + '。')

    # 建議
    for r, u in weak[:2]:
        missed = [q for q in u[2] if x['item'][q]['pts'] < PTS[q]]
        adv.append(f'<b>{u[1]}</b>：{UNIT_ADVICE[u[1]]}重做第 {"、".join(str(q) for q in missed[:5])} 題。')
    if not weak:
        lost_units = sorted(us, key=lambda t: t[0])[:1]
        for r, u in lost_units:
            if r < 1:
                missed = [q for q in u[2] if x['item'][q]['pts'] < PTS[q]]
                adv.append(f'<b>{u[1]}</b>是相對最弱的單元（{pct(r)}）：{UNIT_ADVICE[u[1]]}重做第 {"、".join(str(q) for q in missed[:5])} 題。')
    if nb >= 10:
        adv.insert(0, '<b>時間分配（最優先）</b>：本次有大量題目空白，先完成有把握的題組，非選擇題至少寫出列式或關鍵字，就能拿到部分分數。')
    elif nb >= 4:
        adv.append('<b>時間分配</b>：先完成有把握的題組，非選擇題至少寫出列式或關鍵字，就能拿到部分分數，不要整題空白。')
    if len(mp) >= 5:
        adv.append('<b>多選題</b>：錯一個選項就只剩 1.2 分；作答時逐項標記「確定對／確定錯／不確定」，不確定的回題幹找證據。')
    lost_w = [q for q in FULL if x['item'][q]['pts'] < FULL[q] and not W[x['idx']][q][1].startswith(B)]
    lost_w.sort(key=lambda q: -(FULL[q] - x['item'][q]['pts']))
    tips = [WRITTEN_TIP[q] for q in lost_w[:2]]
    if tips:
        adv.append('<b>非選擇題提醒</b>：' + ' '.join(tips))
    if x['total'] >= 110 and len(adv) < 3:
        adv.append('<b>維持與突破</b>：整體已達頂標水準，剩下的失分多是細節；考前把錯題的關鍵字與單位再檢查一次即可。')
    if len(adv) < 3:
        adv.append('<b>錯題整理</b>：把本次錯題依單元整理，一週後不看解答重做一次，確認能說出每個選項對錯的理由。')
    return out, adv[:4]

CSS = r'''
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK TC', 'Noto Sans TC', sans-serif; color: #1d2433; font-size: 10pt; line-height: 1.5;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 11mm 12mm 9mm; position: relative; overflow: hidden; page-break-after: always; }
.page:last-child { page-break-after: auto; }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.2px solid #1f3a5f; padding-bottom: 5px; }
.top .t1 { font-size: 15pt; font-weight: 700; color: #1f3a5f; letter-spacing: .5px; }
.top .t2 { font-size: 8.6pt; color: #5b6475; margin-top: 2px; }
.who { text-align: right; }
.who .nm { font-size: 15pt; font-weight: 700; }
.who .seat { font-size: 9pt; color: #5b6475; }
.side { position: absolute; top: 4mm; right: 12mm; font-size: 7.5pt; color: #8a93a3; }
.kpis { display: grid; grid-template-columns: 1.25fr 1fr 1fr 1.6fr; gap: 6px; margin: 9px 0 8px; }
.kpi { border: 1px solid #d6dce6; border-radius: 6px; padding: 6px 9px; background: #f7f9fc; }
.kpi .l { font-size: 8pt; color: #5b6475; }
.kpi .v { font-size: 20pt; font-weight: 700; color: #1f3a5f; line-height: 1.15; }
.kpi .v small { font-size: 10pt; color: #5b6475; font-weight: 500; }
.kpi .s { font-size: 7.8pt; color: #5b6475; }
.parts div { display: flex; justify-content: space-between; font-size: 8.8pt; padding: 1px 0; }
.parts b { color: #1f3a5f; }
h3 { font-size: 11pt; color: #1f3a5f; margin: 11px 0 5px; padding-left: 7px; border-left: 4px solid #2f6fb2; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #d6dce6; padding: 3.4px 5px; }
th { background: #1f3a5f; color: #fff; font-weight: 600; font-size: 8.4pt; }
td { font-size: 9.2pt; }
.c { text-align: center; } .r { text-align: right; }
.bar { position: relative; height: 11px; background: #eef1f6; border-radius: 3px; }
.bar .f { position: absolute; left: 0; top: 0; bottom: 0; background: #2f6fb2; border-radius: 3px; }
.bar .m { position: absolute; top: -3px; bottom: -3px; width: 2px; background: #e0892b; }
.legend { font-size: 7.6pt; color: #5b6475; margin-top: 3px; }
.legend i { display: inline-block; width: 10px; height: 8px; vertical-align: middle; margin: 0 3px 0 8px; }
.tag { display: inline-block; padding: 0 6px; border-radius: 8px; font-size: 7.8pt; font-weight: 600; }
.ok { background: #e3f3e8; color: #1e7a3c; } .mid { background: #fff3d6; color: #9a6400; } .bad { background: #fde4e1; color: #b3261e; }
.scale { position: relative; height: 34px; margin: 6px 6px 2px; }
.scale .line { position: absolute; left: 0; right: 0; top: 15px; height: 6px; background: linear-gradient(90deg,#fde4e1,#fff3d6 40%,#e3f3e8); border-radius: 3px; }
.scale .tk { position: absolute; top: 22px; font-size: 7.4pt; color: #5b6475; transform: translateX(-50%); white-space: nowrap; }
.scale .tk::before { content: ''; position: absolute; left: 50%; top: -9px; width: 1px; height: 8px; background: #8a93a3; }
.scale .me { position: absolute; top: 0; transform: translateX(-50%); font-size: 8pt; font-weight: 700; color: #b3261e; white-space: nowrap; }
.scale .me::after { content: '▼'; display: block; text-align: center; font-size: 8pt; line-height: 1; }
.scale .cls { position: absolute; top: 0; transform: translateX(-50%); font-size: 7.4pt; color: #9a6400; white-space: nowrap; }
ul.an, ol.ad { margin: 2px 0 0; padding-left: 18px; }
ul.an li, ol.ad li { margin: 3px 0; font-size: 9.8pt; }
.grid { display: grid; grid-template-columns: repeat(13, 1fr); gap: 2px; }
.cell { border: 1px solid #d6dce6; border-radius: 3px; text-align: center; padding: 1px 0 2px; line-height: 1.2; }
.cell .q { font-size: 7pt; color: #5b6475; }
.cell .a { font-size: 8.6pt; font-weight: 700; }
.cell .k { font-size: 6.9pt; color: #b3261e; }
.cell.full { background: #f2f9f4; border-color: #cfe7d6; }
.cell.full .a { color: #1e7a3c; }
.cell.part { background: #fff6e0; border-color: #f0d9a2; }
.cell.zero { background: #fdecea; border-color: #f2c4bf; }
.cell.zero .a { color: #b3261e; }
.note { font-size: 7.6pt; color: #5b6475; margin-top: 3px; }
td.cm { font-size: 8.9pt; }
.p2 h3 { margin: 8px 0 4px; }
.p2 ul.an li, .p2 ol.ad li { font-size: 9.4pt; margin: 2px 0; line-height: 1.45; }
.p2 td { font-size: 8.5pt; padding: 2.4px 5px; line-height: 1.35; }
.p2 td.cm { font-size: 8.4pt; }
.foot { position: absolute; bottom: 5mm; left: 12mm; right: 12mm; font-size: 7.2pt; color: #8a93a3; display: flex; justify-content: space-between; }
'''

def unit_status(r):
    if r >= 0.8: return '<span class="tag ok">穩定</span>'
    if r >= 0.6: return '<span class="tag mid">可再加強</span>'
    return '<span class="tag bad">優先補強</span>'

def page1(x):
    seat = f'座號 {x["seat"]:02d}' + (f'　學號 {STUDENT_ID[x["seat"]]}' if STUDENT_ID.get(x['seat']) else '')
    h = [f'<div class="page"><div class="side">正面 1／2</div>']
    h.append(f'''<div class="top"><div><div class="t1">{CLASS_NAME}　自然科模擬考 個人成績分析</div>
<div class="t2">{EXAM_TITLE}　滿分 {TOTAL_FULL} 分</div></div>
<div class="who"><div class="nm">{E(x["name"])}</div><div class="seat">{seat}</div></div></div>''')
    diff = x['total'] - CLASS['avg']
    h.append(f'''<div class="kpis">
<div class="kpi"><div class="l">總分</div><div class="v">{f1(x["total"])}<small>／{TOTAL_FULL}</small></div><div class="s">班平均 {f1(CLASS["avg"])}（{"+" if diff>=0 else "−"}{f1(abs(diff))}）</div></div>
<div class="kpi"><div class="l">換算級分</div><div class="v">{x["level"]}<small> 級</small></div><div class="s">{GRADE_SRC}</div></div>
<div class="kpi"><div class="l">班級排名</div><div class="v">{x["rank"]}<small>／{CLASS["n"]}</small></div><div class="s">全班中位數 {f1(CLASS["median"])}</div></div>
<div class="kpi parts"><div class="l">各部分得分</div>
<div><span>第壹部分 選擇題</span><span><b>{f1(x["p1"])}</b>／{P1_FULL}　<span style="color:#8a93a3">班 {f1(CLASS["p1"])}</span></span></div>
<div><span>第貳部分 混合題</span><span><b>{f1(x["p2"])}</b>／{P2_FULL}　<span style="color:#8a93a3">班 {f1(CLASS["p2"])}</span></span></div>
<div><span>　其中非選擇題</span><span><b>{f1(x["written"])}</b>／{WR_FULL}　<span style="color:#8a93a3">班 {f1(CLASS["written"])}</span></span></div>
</div></div>''')
    # level scale
    def pos(lv): return f'{lv/15*100:.2f}%'
    ticks = ''.join(f'<div class="tk" style="left:{pos(v)}">{nm} {v}</div>' for nm, v in BENCH.items())
    h.append(f'''<h3>級分落點（{BENCH_SRC}）</h3>
<div class="scale"><div class="line"></div>{ticks}
<div class="tk" style="left:0%">0</div><div class="tk" style="left:100%">15</div>
<div class="me" style="left:{min(max(x["level"]/15*100, 2.5), 96.5):.2f}%">你 {x["level"]}</div></div>''')
    # subjects
    rows = ''
    for sb in SUBJECTS:
        v = x['subj'][sb]; c = CLASS['subj'][sb]; d = v - c
        rows += (f'<tr><td class="c"><b>{sb}</b></td><td class="r">{f1(v)}／{SUBJ_FULL}</td><td class="c">{pct(v/SUBJ_FULL)}</td>'
                 f'<td><div class="bar"><div class="f" style="width:{v/SUBJ_FULL*100:.1f}%"></div><div class="m" style="left:{c/SUBJ_FULL*100:.1f}%"></div></div></td>'
                 f'<td class="r">{f1(c)}</td><td class="r" style="color:{"#1e7a3c" if d>=0 else "#b3261e"}">{"+" if d>=0 else "−"}{f1(abs(d))}</td></tr>')
    h.append(f'''<h3>各科得分（每科 32 分）</h3>
<table><tr><th style="width:12%">科目</th><th style="width:13%">得分</th><th style="width:9%">得分率</th><th>得分率圖</th><th style="width:11%">班平均</th><th style="width:10%">與班差</th></tr>{rows}</table>
<div class="legend"><i style="background:#2f6fb2"></i>你的得分率<i style="background:#e0892b;width:2px"></i>班平均</div>''')
    # units
    rows = ''
    for sb, nm, qs, v, full in x['units']:
        r = v / full; cr = CLASS['unit'][nm]
        rows += (f'<tr><td class="c">{sb}</td><td>{nm}</td><td class="c" style="font-size:7.8pt;color:#5b6475">{"、".join(str(q) for q in qs)}</td>'
                 f'<td class="r">{f1(v)}／{full}</td>'
                 f'<td><div class="bar"><div class="f" style="width:{r*100:.1f}%"></div><div class="m" style="left:{cr*100:.1f}%"></div></div></td>'
                 f'<td class="c">{pct(r)}</td><td class="c" style="color:#5b6475">{pct(cr)}</td><td class="c">{unit_status(r)}</td></tr>')
    h.append(f'''<h3>單元診斷</h3>
<table><tr><th style="width:8%">科目</th><th style="width:25%">單元</th><th style="width:15%">題號</th><th style="width:10%">得分</th><th>得分率</th><th style="width:7%">你</th><th style="width:7%">班</th><th style="width:12%">判讀</th></tr>{rows}</table>
<div class="legend">判讀標準：得分率 ≥80% 穩定、60–79% 可再加強、&lt;60% 優先補強。橘線為班平均得分率。</div>''')
    h.append(f'<div class="foot"><span>{CLASS_NAME} 自然科　{E(x["name"])}</span><span>{GRADE_NOTE}</span></div></div>')
    return ''.join(h)

def page2(x):
    an, ad = analysis(x)
    h = [f'<div class="page p2"><div class="side">背面 2／2</div>']
    seat = f'座號 {x["seat"]:02d}' + (f'　學號 {STUDENT_ID[x["seat"]]}' if STUDENT_ID.get(x['seat']) else '')
    h.append(f'''<div class="top"><div><div class="t1" style="font-size:13pt">情況分析與學習建議</div>
<div class="t2">{EXAM_SHORT} 自然考科</div></div><div class="who"><div class="nm" style="font-size:12.5pt">{E(x["name"])}</div><div class="seat">{seat}</div></div></div>''')
    h.append('<h3>情況分析</h3><ul class="an">' + ''.join(f'<li>{t}</li>' for t in an) + '</ul>')
    h.append('<h3>學習建議</h3><ol class="ad">' + ''.join(f'<li>{t}</li>' for t in ad) + '</ol>')
    # MC grid
    cells = ''
    for q in [q for q in QS if q in KEY]:
        it = x['item'][q]; p = it['pts']
        cls = 'full' if p >= 2 else ('part' if p > 0 else 'zero')
        k = '' if p >= 2 else f'<div class="k">答 {KEY[q]}</div>'
        ptxt = '' if p >= 2 else f'<div class="k" style="color:#5b6475">{f1(p)}分</div>'
        cells += f'<div class="cell {cls}"><div class="q">{q}</div><div class="a">{it["ans"]}</div>{k}{ptxt}</div>'
    nfull = sum(1 for q in KEY if x['item'][q]['pts'] >= 2)
    h.append(f'<h3>選擇題作答一覽（{len(KEY)} 題，全對 {nfull} 題）</h3><div class="grid">{cells}</div>'
             f'<div class="note">綠色＝全對；黃色＝多選題部分得分；紅色＝0 分（「—」為未作答）。多選題每錯一個選項扣 0.8 分{SIXNOTE}。</div>')
    rows = ''
    for q in FULL:
        p = x['item'][q]['pts']; full = FULL[q]
        cls = 'ok' if p >= full else ('mid' if p > 0 else 'bad')
        rows += (f'<tr><td class="c">{q}</td><td>{TOPIC[q]}</td><td class="c"><span class="tag {cls}">{f1(p)}／{full}</span></td>'
                 f'<td class="cm">{E(W[x["idx"]][q][1])}</td></tr>')
    h.append(f'''<h3>非選擇題批改（{f1(x["written"])}／{WR_FULL}）</h3>
<table><tr><th style="width:6%">題號</th><th style="width:19%">考點</th><th style="width:10%">得分</th><th>批改說明</th></tr>{rows}</table>''')
    h.append(f'<div class="foot"><span>{CLASS_NAME} 自然科　{E(x["name"])}</span><span>批改依 {EXAM_SHORT} 詳解評分原則</span></div></div>')
    return ''.join(h)

def build(out):
    order = sorted(STUDENTS, key=lambda x: (x['seat'] if x['seat'] is not None else 99, x['name']))
    body = ''.join(page1(x) + page2(x) for x in order)
    doc = f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>{CLASS_NAME} 自然模考（{EXAM_SHORT}）個人分析</title><style>{CSS}</style></head><body>{body}</body></html>'
    open(out, 'w', encoding='utf-8').write(doc)
    return order

if __name__ == '__main__':
    order = build(sys.argv[1])
    print('students', len(order))
