"""Local, self-contained HTML report and a quantitative SVG mass figure."""
import csv
import html
import os
from pathlib import Path

def esc(x):
    return html.escape(str(x))

def table(rows, headers):
    return '<div class="table"><table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def render_report(output,summary,inventory,checks):
    output=Path(output)
    ordered=sorted(inventory,key=lambda r:float(r['finished_mass_g']),reverse=True)
    bars=[]
    for i,r in enumerate(ordered):
        y=84+i*43; m=float(r['finished_mass_g']); color='#215d64' if r['scope']=='Kettle' else '#c18841'
        bars.append(f'<text x="12" y="{y+19}" font-size="13">{esc(r["material"])}</text><rect x="340" y="{y}" width="{m/400*475:.3f}" height="27" rx="3" fill="{color}"/><text x="{350+m/400*475:.3f}" y="{y+19}" font-size="14">{m:g} g</text>')
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 635" role="img" aria-labelledby="title desc"><title id="title">Finished mass by material</title><desc id="desc">Mass contribution only. This is not greenhouse gas contribution.</desc><rect width="900" height="635" fill="#fff"/><g font-family="Arial, sans-serif" fill="#1c3539"><text x="12" y="30" font-size="22" font-weight="bold">Finished mass by material</text><text x="12" y="56" font-size="13">One packaged kettle · 860.8 g · Material mass, not GWP100</text>'+''.join(bars)+'<text x="12" y="620" font-size="13">Teal: kettle (723 g) · Ochre: packaging (137.8 g) · Source: supplied BOM</text></g></svg>'
    (output/'mass_breakdown.svg').write_text(svg,encoding='utf-8')
    mapping=[]
    if (output/'mapping.csv').exists():
        with (output/'mapping.csv').open(encoding='utf-8-sig',newline='') as f:
            mapping=list(csv.DictReader(f))
    translations={'material_candidate_only':'재료 후보 / 계산 미승인','monetary_bridge_not_accepted':'금액 기반 연결 / 미채택','unresolved':'미해결'}
    map_table=table([(r['input'],translations.get(r['decision'],r['decision']),r.get('dataset_name','unknown'),r['rationale']) for r in mapping],['투입물','판정','데이터셋','선정 근거 및 제한']) if mapping else '<p>배경자료 미감사: 원본 ZIP을 지정해 다시 실행하세요.</p>'
    check_table=table([(c['check'],c['status'],c['detail']) for c in checks],['검증','결과','근거'])
    edges=summary.get('unique_provider_edge_statuses',{})
    unresolved=sum(n for k,n in edges.items() if k not in ('explicit_provider','unique_reference_flow_candidate'))
    readme_link=os.path.relpath(Path(__file__).resolve().parents[1]/'README.md',output).replace('\\','/')
    navigation=f'<a href="{esc(readme_link)}">10개 항목 README</a>'
    if mapping:
        navigation+='<a href="mapping.csv">전체 매칭표 CSV</a><a href="supplier_links.csv">공급 공정 연결 CSV</a>'
    navigation+='<a href="summary.json">기계 판독 결과 JSON</a>'
    document=f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BC1 전기주전자 · LCA 데이터 감사</title>
<style>
:root{{--ink:#1b3337;--muted:#5e7074;--teal:#215d64;--line:#d9e3e2;--paper:#f5f7f4;--amber:#805420}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.7 "Malgun Gothic",Arial,sans-serif}}main{{max-width:1180px;margin:auto;padding:48px 32px 64px}}a{{color:var(--teal);text-underline-offset:3px}}.eyebrow{{font-size:12px;font-weight:700;letter-spacing:2px;color:var(--teal)}}h1{{font-size:36px;line-height:1.3;margin:13px 0 16px}}h2{{font-size:24px;margin:42px 0 16px}}p{{max-width:920px}}.intro{{font-size:17px;color:var(--muted)}}.meta{{color:var(--muted);font-size:13px}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:28px 0}}.card{{background:white;border:1px solid var(--line);border-radius:10px;padding:22px}}.value{{font-size:31px;font-weight:700;margin-top:7px}}.unit{{font-size:15px;font-weight:400}}.status{{border-left:5px solid #b97b2f;background:#fff5e6;padding:20px 24px;margin:25px 0}}.status strong{{display:block;font-size:21px;color:var(--amber)}}.table{{overflow-x:auto;background:white;border:1px solid var(--line);border-radius:8px}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{padding:13px 15px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:#e8efeb;white-space:nowrap}}td:first-child{{min-width:155px}}td:last-child{{min-width:290px}}figure{{margin:0;background:white;border:1px solid var(--line);padding:20px;border-radius:10px}}figure img{{display:block;width:100%;height:auto}}figcaption{{font-size:13px;color:var(--muted)}}nav{{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0;padding-bottom:22px;border-bottom:1px solid var(--line)}}li{{margin:8px 0}}footer{{border-top:1px solid var(--line);padding-top:20px;margin-top:40px;font-size:13px;color:var(--muted)}}@media(max-width:760px){{main{{padding:24px 16px}}h1{{font-size:28px}}.cards{{grid-template-columns:1fr}}.value{{font-size:27px}}}}@media print{{body{{background:white}}main{{padding:0}}nav{{display:none}}.table{{overflow:visible}}h2{{break-after:avoid}}figure,.card{{break-inside:avoid}}}}
</style></head><body><main>
<div class="eyebrow">BC1 · INVENTORY &amp; DATA READINESS</div><h1>1 L 플라스틱 전기주전자<br>공장 출고 기준 LCA 데이터 감사</h1>
<p class="intro">제공된 BOM과 실제 USLCI 원본을 확인한 독립 실행 기록입니다. 계산에 필요한 데이터 연결과 제조 정보가 충족되지 않아, 탄소배출 총량은 아직 산출하지 않았습니다.</p>
<p class="meta">연구일 {esc(summary['study_date'])} · 실행 {esc(summary['run_id'])} · 미국 배경자료 시나리오 · 실제 제조 지역 미상</p>
<nav>{navigation}</nav>
<section class="cards"><div class="card">제품 질량<div class="value">723 <span class="unit">g</span></div></div><div class="card">포장 질량<div class="value">137.8 <span class="unit">g</span></div></div><div class="card">포장된 주전자 1대<div class="value">860.8 <span class="unit">g</span></div></div></section>
<div class="status"><strong>GWP100: 미계산</strong>단위: kg CO₂-eq / 포장된 주전자 1대. 누락된 값을 0으로 처리하지 않았습니다. GWP 기여도 상위 3개와 신뢰구간도 산출하지 않았습니다.</div>
<h2>확인된 결과</h2><p>질량 검산은 통과했습니다. 배경자료는 USLCI {esc(summary.get('database_release','미감사'))}이며, 후보 그래프에서 고유 공정 {summary.get('unique_reachable_processes','미확인')}개를 검사했습니다. 공급·배분·대체효과 검토가 남은 연결은 {unresolved if edges else '미확인'}개입니다. 이는 구조 감사 결과이며, 완성된 LCA 공급망을 의미하지 않습니다.</p>
<figure><img src="mass_breakdown.svg" alt="재료별 완제품 질량 막대그래프"><figcaption>질량 상위: PP, 스테인리스, 판지. 질량 순위로 탄소배출 기여도를 추론할 수 없습니다.</figcaption></figure>
<h2>재료별 매칭 판정</h2>{map_table}
<h2>검증 결과</h2>{check_table}
<h2>민감도와 불확실성</h2><p>수율 100%, 98%, 95%를 가정한 질량 민감도만 계산했습니다. 이는 사용자가 제공한 실제 수율이나 확률분포가 아닙니다. GWP 불확실성·Monte Carlo·P05/P95는 미계산입니다. <a href="mass_sensitivity.csv">질량 민감도 표</a></p>
<h2>탄소배출 계산을 완료하려면</h2><ol><li>황동·POM·실리콘의 적합한 물리적 LCI와 나일론 등급을 확보합니다. 구리·PC·나일론의 금액 기반 대체자료를 사용할 경우 섹터와 가격 기준, 외부 USEEIO 연결을 별도로 검토합니다.</li><li>소재별 수율, 성형 공정, 조립 전력, 운송 거리와 스크랩 처리를 결정합니다. 재료·포장·에너지의 중복 계상을 확인합니다.</li><li>전력 등 외부 공급자료, 내부의 누락·모호한 공급자, 공동제품 배분과 수식을 해결하고 FEDEFL과 호환되는 GWP100 방법을 적용합니다.</li><li>원본 결과를 보존한 새 실행에서 계산하고 기여도 합계와 단위, 질량수지, 미특성화 흐름을 검증합니다.</li></ol>
<footer>재현: Python 표준 라이브러리만 사용. 원본 데이터의 SHA-256, 데이터셋 UUID·버전·기간 및 검색 기록은 프로젝트에 포함되어 있습니다. API 응답 실패와 계산 불가는 수치 0과 구분됩니다.</footer>
</main></body></html>'''
    (output/'report.html').write_text(document,encoding='utf-8')
