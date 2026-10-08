# BC1 1 L 전기주전자 — 미국 USLCI 기반 공장 출고 LCA 데이터 감사

**계산 상태: `not calculated` — GWP100 총량은 미계산이며 0이 아닙니다.**

제공된 12개 재료의 질량을 검증하고, 실제 USLCI 원본의 1,434개 공정을 검색했습니다. 제품 **723 g**, 포장 **137.8 g**, 합계 **860.8 g**이 확인됐습니다. 재료 후보와 공급망 구조를 감사했으나, 제조 정보·적합한 배경자료·공급자 연결·영향평가 방법이 완비되지 않았습니다. 이 결과물은 완성된 탄소발자국 수치 대신 **재현 가능한 입력·매칭·누락 검증 결과**를 제공합니다.

[보고서 열기](results/independent/report.html) · [매칭표](results/independent/mapping.csv) · [검증 결과](results/independent/checks.csv) · [기계 판독 요약](results/independent/summary.json)

## 1. Study identity and purpose

| 항목 | 실제 기록 |
|---|---|
| 연구 제목 | BC1 1 L 플라스틱 전기주전자의 미국 배경자료 기반 공장 출고 LCA 데이터 감사 |
| 공개 학생/그룹 별칭 | ParkSM1212 — 공개 GitHub 계정 별칭 |
| 저장소 URL | [https://github.com/ParkSM1212/bc1-kettle-lca](https://github.com/ParkSM1212/bc1-kettle-lca) |
| 실행 식별자 | `bc1-uslci-independent-20261008` |
| 연구일 / 시간대 | 2026-10-08 / Asia/Seoul |
| 실행 구분 | independent — 다른 연구자의 답안을 비교·반영하지 않음 |
| Git tag / commit | 별도 태그 없음. 이 파일을 포함한 실제 커밋은 저장소 History에서 확인하며 자신의 미래 SHA를 본문에 넣지 않음 |
| 목적 | 포장된 주전자 1대의 공장 출고 GWP100 산정에 필요한 데이터와 모델의 준비 상태 검증 |
| 의도한 비교 | 제품 대안 비교는 미지정. 이번에는 질량 수율의 가정별 변화만 비교하며 GWP 비교는 하지 않음 |

요구사항 파일은 결과물의 구성 기준으로 해석했습니다. 분석 후 사용자의 명시적 요청으로 GitHub 공개 저장소에 게시했습니다. 제출 양식과 개인정보 입력은 실행하지 않았습니다. 제출 시 저장소의 실제 최종 커밋에서 **40자리 SHA를 확인하여 양식에 기록**해야 합니다. 이 README에 자신의 미래 커밋 해시를 만들어 넣지 않았습니다.

## 2. Product, declared unit and system boundary

선언단위는 **공장에서 제조와 포장을 마친 BC1 1 L 플라스틱 전기주전자 1대**입니다. BC1·용량·공장 출고 조건은 첨부 요구사항에서, 재료별 질량은 사용자 제공 BOM에서 가져왔습니다. 정격 전력·전압·부품 수·합금 및 수지의 상세 등급은 unknown입니다.

BOM 출처는 2026-10-08에 제공된 재료 목록이며, 원측정일과 제조사의 문서 버전은 unknown입니다. 실행 입력의 로컬 상대 경로는 [`inputs/bom.csv`](inputs/bom.csv)입니다. 사용자 메시지의 줄 끝 `\`를 줄 구분자로 처리했으며, 재료명·질량·범위는 보존했습니다.

| 범위 | 검산 질량 | 요구 질량 | 차이 |
|---|---:|---:|---:|
| Kettle | 723 g | 723 g | 0 g |
| Packaging | 137.8 g | 137.8 g | 0 g |
| 포장된 제품 | 860.8 g | 860.8 g | 0 g |

의도한 경계에는 원료 생산, 소재 생산, 부품 성형, 투입물 운송, 조립 전력, 제조 스크랩 처리, 포장 생산·포장 작업이 포함됩니다. 아직 수량이나 공급자를 확보하지 못한 단계도 경계 안의 **미해결 항목**으로 남겼습니다. 유통·소비자 사용·수명 종료 처리는 제외하며, 별도 확장 시나리오는 없습니다. 시설·설비 등 배경공정에 이미 포함된 항목의 경계를 임의로 삭제하지 않았습니다.

12개 BOM 항목은 모두 유지했으며 의도적인 질량 컷오프는 없습니다. 배경자료의 `CUTOFF` 흐름도 자동으로 0 처리하지 않습니다. 미국 USLCI 배경 시나리오는 사용자가 선택했습니다. 실제 제조 지역과 생산 기준연도는 unknown이고, 개별 데이터의 북미·미국 지역 및 유효기간은 매칭표에 별도로 기록했습니다. **데이터베이스 발행연도 2026을 모든 공정의 관측연도로 간주하지 않습니다.**

## 3. Foreground inventory and quantitative assumptions

아래 질량의 근거·상태는 모두 사용자 제공 [`inputs/bom.csv`](inputs/bom.csv), `sourced`입니다. 이는 완제품에 남은 질량이며 구매 질량은 아닙니다.

| 재료 | 완제품 질량 (g) | 변환 질량 (kg) | 범위 |
|---|---:|---:|---|
| Stainless steel | 186 | 0.186 | Kettle |
| Brass | 20.25 | 0.02025 | Kettle |
| Copper | 15 | 0.015 | Kettle |
| Polypropylene (PP) | 350.25 | 0.35025 | Kettle |
| Polyvinyl chloride (PVC) | 43.5 | 0.0435 | Kettle |
| Nylon, grade unspecified | 49.5 | 0.0495 | Kettle |
| Polyoxymethylene (POM) | 9.75 | 0.00975 | Kettle |
| Polycarbonate (PC) | 6.75 | 0.00675 | Kettle |
| Acrylonitrile-butadiene-styrene (ABS) | 30 | 0.030 | Kettle |
| Silicone | 12 | 0.012 | Kettle |
| LDPE packaging foil | 6.3 | 0.0063 | Packaging |
| Cardboard packaging | 131.5 | 0.1315 | Packaging |

수율·공정·운송·스크랩·가격의 값, 단위, 근거, 상태는 [`foreground_parameters.csv`](inputs/foreground_parameters.csv)에 있습니다. 제조 수율, 성형 작업량, 조립 kWh, 운송 t·km, 스크랩 kg는 모두 **unknown**입니다. 근거 없는 추정치를 기준안에 입력하지 않았습니다. 가격은 금액 기반 모델을 채택하지 않아 기준안에서는 not applicable입니다.

완제품 질량을 `m_g`, 해당 소재 수율을 `y`라 하면 구매 질량은 `m_g / (1000 × y)` kg, 스크랩은 `구매 질량 − m_g/1000` kg입니다. 수율을 모르면 구매량도 unknown입니다. 공급 공정의 기준 산출량이 `q_ref`이면 활동량은 동일 단위로 변환한 수요량을 `q_ref`로 나눕니다. kg와 g는 1,000배, kWh와 MJ는 3.6배 관계이며, 데이터셋 단위와 흐름 속성을 먼저 확인해야 합니다. 이번 실행은 g→kg와 가상 수율별 질량만 계산했고 LCIA 공정 스케일링은 수행하지 않았습니다.

중복 계산 검토에서 확인한 구체적인 예는 다음과 같습니다. 원본 UUID, 수치, 단위, 해시는 [`boundary_evidence.csv`](results/independent/boundary_evidence.csv)에 있습니다.

- PP 사출성형 후보는 **성형품 1 kg당 PP 수지 1.034 kg, 전력 6.444 MJ, 골판지 0.1 kg**를 이미 포함합니다. 이를 전체 성형품 공정으로 채택하면 수지 생산을 다시 별도 가산하면 안 됩니다. 0.1 kg 포장도 BOM 포장과의 중복 여부를 먼저 확인해야 합니다.
- LLDPE 필름 후보에는 수지·압출이 각각 1.02 kg 포함됩니다. 이 후보를 LDPE 필름과 동일하다고 간주하지 않았으며 손실을 다시 덧붙이지 않았습니다.
- 스테인리스 코일 후보에는 압연이, 골판지 후보에는 골판지·시트 공정이 포함됩니다. PVC 수지 후보의 경계에는 수지 생산에 필요한 입고 운송이 포함됩니다. 이 사실은 주전자 조립이나 공장까지의 추가 운송이 모두 포함됐다는 뜻은 아닙니다.

## 4. Background data and matching decisions

실제로 검색한 자료는 **USLCI 1.2026-09.0**의 JSON-LD 원본입니다. 저장소 리비전은 `fddfc1a7a6c93e1a71f457446df7813245c828e6`, 검색한 공정은 1,434개, 흐름은 5,708개입니다. 수집일은 2026-10-08이며 파일 크기는 32,056,606 bytes입니다. 원본 SHA-256은 다음과 같습니다.

```text
d1b354d11b757efecd8f456077744e83b9c74b4df0d99e18256bdd0335ac5009
```

발행판은 [공식 USLCI 릴리스 문서](https://github.com/FLCAC-admin/uslci-content/blob/dev/docs/release_info/press-release.md)를 확인했으며, 실제 받은 바이트는 위 리비전과 해시로 고정했습니다. [공식 다운로드 안내](https://github.com/FLCAC-admin/uslci-content/blob/dev/docs/release_info/release-downloads.md)의 최신 JSON-LD 링크는 [공개 저장소](https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/datasets)로 연결됩니다. 원본 ZIP은 배포 압축파일에 포함하지 않고 정확한 수집 절차를 제공합니다.

| 판정 | 재료 | 해석 |
|---|---|---|
| 소재 후보 6개 | 스테인리스, PP, PVC, ABS, LDPE, 판지 | 물질·형상·등급·경계를 추가 확인해야 하며 GWP 계산에 승인된 계수가 아님 |
| 금액 기반 연결 3개 | 구리, 나일론, PC | USEEIO 연결 공정이며 독립적인 물리적 배출계수가 아님; 미채택 |
| 미해결 3개 | 황동, POM, 실리콘 | 지정한 이름·동의어의 전체 공정명 검색에서 적합한 생산 공정을 찾지 못함 |

[`mapping.csv`](results/independent/mapping.csv)는 모든 BOM 입력에 대해 데이터베이스·발행판·데이터셋명·UUID·버전·지역·유효기간·기준 흐름/양/단위·원본 URL·수집일·개별 JSON 해시 및 대안·판정 이유를 기록합니다. 미해결 항목은 unknown입니다. 성형·전력·운송·스크랩 검색도 [`search_log.csv`](results/independent/search_log.csv)와 [`search_candidates.csv`](results/independent/search_candidates.csv)에 포함되며, 전경 수량이 없어 해당 단계의 최종 공급자를 선택하지 않았습니다.

전체 검색은 공정명에 대한 대소문자 무시 부분문자열 검색입니다. **데이터베이스 전체에서 그 물질이 절대 존재하지 않는다는 증명은 아닙니다.** 질적으로 다른 재료, 예를 들어 실리콘 대신 규소 금속, 구리 대신 황산구리, ABS 대신 아크릴로니트릴은 채택하지 않았습니다. 나일론은 6과 66 중 하나로 임의 확정하지 않았습니다.

금액 기반 연결의 부문, USD 가격, 2012 가격연도, 원자료의 `producer price` 기준, 1 kg 기준량은 [`monetary_bridge_review.csv`](results/independent/monetary_bridge_review.csv)에 있습니다. 예컨대 구리 연결은 1 kg당 9.13 USD의 광물 정광 부문 수요입니다. 이는 구매가격·기초가격과의 일치가 검증되지 않은 부문 대체값이며 kg CO₂-eq/kg이 아닙니다. 실제 구매량, 공급 USEEIO 모델과 적합성이 확정되지 않아 사용하지 않았습니다.

모든 선택 후보의 `processType`은 `UNIT_PROCESS`입니다. 이것만으로 모든 목록이 동일한 세부 경계를 갖는다고 단정하지 않습니다. 누적 LCIA 계수를 사용한 적은 없습니다. 최신 USLCI는 외부 전력 저장소 등에 의존합니다. [공식 Commons Merged 안내](https://flcac-admin.github.io/FLCAC-docs/commons-merged/)는 관련 자료를 통합하는 경로를 설명하지만, 이번에 통합 저장소를 수집·계산했다고 주장하지 않습니다.

TianGong [CLI](https://github.com/tiangong-lca/cli)와 [조직 저장소](https://github.com/orgs/tiangong-lca/repositories)는 기능과 접근 경로를 검토했습니다. [데이터 저장소](https://github.com/tiangong-lca/data)는 과거 스냅샷이라고 명시하므로 최신 데이터를 받은 것으로 취급하지 않았습니다. 이번 기준안에는 TianGong 자료를 혼합하지 않았습니다. 인증·추가 검색 절차는 [`docs/data_access.md`](docs/data_access.md)에 있습니다.

## 5. Calculation and impact-assessment methods

실제 실행 알고리즘은 CSV 검증 → Decimal 질량 합산·단위 변환 → 원본 ZIP 해시/CRC 확인 → 공정명 전체 검색 → 명시적 후보와 원본 UUID 결합 → 공급 공정 그래프 탐색 → 누락·배분·수식·미평가 기본흐름 목록 출력입니다. 구현은 [`src/audit.py`](src/audit.py)이며 Python 3.12.14 표준 라이브러리를 사용합니다. **LCA 행렬 솔버는 실행하지 않았습니다.**

공급자 탐색은 흐름 UUID와 방향을 사용합니다. `defaultProvider`를 우선 확인하고, 지정이 없으면 해당 기준 흐름의 유일한 생산자/폐기물 처리자를 구조적 후보로 연결합니다. 여러 후보를 임의 선택하지 않습니다. 공동제품 연결은 탐색하되 배분 검토 대상으로 남깁니다. 제품의 투입과 폐기물의 산출 방향을 구분하며, 순환은 방문 집합으로 처리합니다. 이 그래프 연결은 최종 공급자 선정이나 수치 계산이 아닙니다.

완성된 과정 기반 LCA라면 단위·배분·공급자가 일관된 기술행렬 `A`, 수요 `f`에 대해 `A s = f`, 기본흐름 `g = B s`, 영향 `h = C g`를 계산해야 합니다. 이번에는 `A/B/C`를 구성하거나 해를 구하지 않았으므로 GWP 총량·부분합 모두 not calculated입니다. 가산 가능한 검증된 누적계수도 확보하지 않았습니다.

시스템 모델 및 전경 배분은 unknown입니다. 배경자료의 `defaultAllocationMethod`는 그대로 기록했고, 공동제품·배분과 `amountFormula`를 별도 표시했습니다. 수식의 저장된 수치가 현행 파라미터와 동일하다고 추정하지 않았습니다. 재활용 함량·스크랩 처리·회피효과를 결정하지 않았고 임의의 크레딧을 부여하지 않았습니다.

영향지표의 목표 시간범위는 **GWP100의 100년**이지만, 특성화 방법명·버전·계수 파일은 not selected입니다. 생물기원 탄소, 토지이용 변화 및 지연배출의 처리도 unknown입니다. 향후 방법은 FEDEFL 흐름과 호환성을 확인해야 합니다. 단순 물질명만 같다는 이유로 계수를 매칭하면 안 됩니다.

후보 그래프에서 확인된 고유 기본흐름 2,868개는 [`elementary_flows_pending.csv`](results/independent/elementary_flows_pending.csv)에 기록했습니다. 이 수는 **미특성화 흐름 수가 아니라 특성화 검토 대기 흐름 수**입니다. 방법이 정해지지 않아 미특성화 흐름 수 자체는 unknown입니다. 누락 공급자를 0으로 계산하지 않았습니다.

## 6. How to reproduce the analysis

```text
README.md                           연구 요약과 10개 필수 항목
inputs/bom.csv                      사용자 BOM
inputs/study.json                    경계·질량 검산 기준·실행 정보
inputs/foreground_parameters.csv    제조 정보와 가정의 상태
inputs/search_queries.json          전체 이름 검색 조건
inputs/matching_decisions.json      후보 UUID·선정 이유·대안
inputs/tiangong-search/              선택적 추가 검색 요청
data/source_manifest.json           원본 리비전·크기·SHA-256
src/fetch_uslci.py                   고정된 공개 원본 수집과 검증
src/audit.py                        질량·검색·공급망 감사
src/report.py                       HTML 보고서·질량 그림 생성
tests/test_audit.py                 단위·미상 값·공급자 처리 테스트
results/independent/                보존한 독립 실행 결과·표·그림
docs/                              접근 절차·수집 기록·결정 기록
```

실행 환경은 Windows, Python **3.12.14**이며 외부 Python 의존성은 없습니다. `requirements.txt`는 이를 명시합니다. CSV는 UTF-8 BOM, JSON/HTML/Markdown은 UTF-8입니다. 다음은 PowerShell에서 프로젝트 폴더를 현재 디렉터리로 둔 재현 명령입니다. Codex 번들 Python 대신 동일 버전의 Python 실행 파일을 지정해도 됩니다.

```powershell
$pythonExe = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $pythonExe --version
& $pythonExe -m unittest discover -s tests -v

# 데이터 재수집: 공식 API Guide에서 발급받은 키를 세션 환경변수로만 입력합니다.
$env:LCA_COMMONS_API_KEY = Read-Host -MaskInput 'LCA Commons API key'
& $pythonExe src\fetch_uslci.py
Remove-Item Env:LCA_COMMONS_API_KEY

# 새 디렉터리로 재현합니다. 독립 실행 결과를 덮어쓰지 않습니다.
& $pythonExe src\audit.py --archive data\raw\uslci-1.2026-09.0.jsonld.zip --out results\reproduced
Start-Process results\reproduced\report.html
```

계정과 키는 [공식 API Guide](https://www.lcacommons.gov/lca-commons-api-guide)의 요구사항을 따릅니다. 이번 수집은 공식 문서가 제공하는 공개 데모 접근으로 수행했습니다. 키 값·토큰·개인 세션은 배포 파일에 저장하지 않았습니다. `fetch_uslci.py`는 `LCA_COMMONS_API_KEY`만 읽고 검증된 캐시가 있으면 네트워크 요청 없이 재사용합니다. 원본 다운로드 항목이 만료되거나 바이트가 달라지면 중단하며 새 발행판으로 조용히 대체하지 않습니다. API 429는 검색 결과 0건이 아닙니다.

원본이 없더라도 질량 검산은 다음과 같이 재현할 수 있습니다. 이 경우 배경자료 검증은 수행되지 않습니다.

```powershell
& $pythonExe src\audit.py --out results\mass-only
```

보고서는 브라우저에서 로컬 HTML을 열면 됩니다. 외부 웹 글꼴이나 서버가 필요 없습니다. [`docs/data_access.md`](docs/data_access.md)는 원본이 만료된 경우의 수동 수집, TianGong 인증, 외부 공급자료 접근을 설명합니다. 이번 감사는 확률 추출을 사용하지 않아 난수 seed는 not applicable입니다. 전체 GWP 산정에는 아직 7절의 데이터·모델 보완 작업이 필요합니다.

## 7. Results, checks and interpretation

**완료된 결과:** 질량 검산, 전체 공정명 검색, 후보 비교, 원본·개별 공정 해시, 공급 구조 감사, 질량 수율 예시, 실행 가능한 재현 코드. **미완료된 수치:** GWP100 총량, 소재별 배출량, 제조·운송 배출량, GWP 상위 3개.

| 지표/검사 | 결과 |
|---|---|
| 포장된 제품 질량 | 860.8 g |
| GWP100 | not calculated — kg CO₂-eq/포장된 주전자 1대 |
| GWP 기여도 상위 3개 | not calculated |
| 질량 상위 3개 | PP 350.25 g, 스테인리스 186 g, 판지 131.5 g |
| 후보 루트 / 탐색된 고유 공정 | 9 / 383 |
| 명시적 공급 연결 / 유일 기준 흐름 후보 연결 | 1,254 / 5 |
| 공급자를 찾지 못한 연결 | 609 |
| 공급자가 여러 개인 연결 | 17 |
| 공동제품 배분 검토 연결 | 75 |
| 회피효과 모델 검토 연결 | 15 |
| 합계 검토 대상 연결 | 716 |
| g→kg·BOM 질량 검산·원본 해시/CRC | pass |
| 공급망 폐쇄 | fail — 위 검토 항목이 남음 |
| 구매량 질량수지·기여도 합계 | not calculated |
| 중복 계산 검증 | unresolved — 포함된 수지·전력·포장 경계를 식별했으나 최종 모델 미구성 |

연결 수는 `(공정 UUID, 교환 internalId, 흐름 UUID)` 기준으로 중복을 제거한 구조 통계입니다. [`supplier_links.csv`](results/independent/supplier_links.csv)는 각 루트별 추적 경로를 보존하므로 같은 연결이 여러 루트에 나타납니다. 단순 행 수를 위 통계와 비교해서는 안 됩니다. [`supplier_closure.csv`](results/independent/supplier_closure.csv)는 루트별 검사, [`model_flags.csv`](results/independent/model_flags.csv)는 미평가 수식·공동제품 목록, [`reachable_process_manifest.csv`](results/independent/reachable_process_manifest.csv)는 탐색된 모든 공정의 출처입니다.

완전한 투입물 목록과 단계별 미계산 상태는 [`contributions.csv`](results/independent/contributions.csv)에 있습니다. 빈 수치 셀은 같은 행의 `not_calculated`와 함께 해석해야 합니다. CSV 합계 함수로 빈 셀을 제외해 얻은 0은 이 연구의 결과가 아닙니다. JSON에서는 미상 수치를 `null`로 저장합니다.

[질량 그림](results/independent/mass_breakdown.svg)은 탄소배출 기여도 그림이 아닙니다. PP가 가장 무겁다는 사실만으로 GWP의 최대 기여자라고 결론 내릴 수 없습니다. 오래된 공정 관측기간, 불명확한 등급, 조건부 판지/스테인리스 대체, 외부 전력·USEEIO 의존성과 미해결 제조 단계 때문에 제품 간 탄소우열을 주장할 수 없습니다.

GWP 계산을 완료하려면 황동·POM·실리콘 자료, 구리·나일론·PC의 적합한 물리적 자료 또는 검증된 금액 기반 대체, 실제 제조 전경, 공급자·배분·수식 해결, GWP100 방법·흐름 매칭 및 수치 솔버가 필요합니다. 이 패키지의 프로그램은 **감사 도구이며 LCIA 솔버가 아닙니다.**

## 8. Uncertainty and sensitivity

GWP 불확실성은 **not calculated**입니다. 분포·상관관계·표본 수·Monte Carlo seed·수렴 검증과 평균·중앙값·P05·P95는 모두 not applicable 또는 unavailable이며, 완성된 수치 모델과 근거가 없기 때문입니다. 중앙 90% 구간을 추정하거나 신뢰구간처럼 제시하지 않았습니다.

계산한 것은 전체 소재에 같은 수율을 적용하는 **독립적인 질량 예시**입니다. 100%·98%·95%는 실제 공장값이나 확률분포가 아닌 `assumed` 시나리오입니다.

| 가상 균일 수율 | 구매 질량 (g) | 스크랩 (g) |
|---|---:|---:|
| 100% | 860.800 | 0.000 |
| 98% | 878.367 | 17.567 |
| 95% | 906.105 | 45.305 |

세부값은 [`mass_sensitivity.csv`](results/independent/mass_sensitivity.csv)에 있습니다. 이 민감도는 배출량 증가율을 뜻하지 않습니다. 향후 파라미터 불확실성, 공급자/영향방법 선택 시나리오, 반복 AI 실행 간 변동을 구분해서 분석해야 합니다. 이번에는 반복 AI 실행 비교나 데이터베이스별 GWP 비교를 하지 않았습니다.

## 9. Codex and human decisions

작업 도구는 Codex이며 세션 설명상 GPT-6 계열입니다. **사용자 UI에 표시된 정확한 모델명·버전은 unknown**이고, reasoning 설정·sampling temperature·모델 seed도 unknown입니다. 실행일은 2026-10-08입니다. 병렬 하위 에이전트는 사용하지 않았습니다.

사용자는 BOM과 출처 링크·요구사항을 제공하고 미국 USLCI 배경자료 사용을 선택했습니다. 후보 검색, 조건부 매칭, 부적합 대체의 거절, 누락값 처리와 코드 구현은 Codex가 수행했습니다. 사용자에게 승인받지 않은 소재 등급·수율·전력량을 기준안으로 채택하지 않았습니다.

중요한 요청 요지·결정·수정은 [`docs/decision_log.md`](docs/decision_log.md)에 정리했습니다. 원문 대화나 개인정보를 공개 파일에 복사하지 않았습니다. API 경로의 끝 슬래시 오류와 일시적인 검색 제한은 [`docs/retrieval_log.csv`](docs/retrieval_log.csv)에 기록했습니다. 초기 개발에서 JSON-LD의 `isQuantitativeReference` 필드와 공동제품 연결 처리를 바로잡았고, 최종 결과는 수정된 코드로 다시 생성했습니다.

12개 자동 테스트를 통과했습니다. 질량은 요구사항의 별도 통제값과 비교했고, 순환·복수 공급자·외부 공급자·폐기물 방향·공동제품·회피효과·미상 수율을 검증했습니다. 테스트 기록은 [`docs/test_results.txt`](docs/test_results.txt)에 있습니다. **사람이 독립적으로 검토·승인한 LCA 결과는 아직 없습니다.**

## 10. Independent and revised runs

독립 실행 결과는 [`results/independent/`](results/independent/)에 보존했습니다. 보존 파일별 SHA-256은 [`data/independent_output_manifest.json`](data/independent_output_manifest.json)에 있습니다. 프로그램은 비어 있지 않은 출력 폴더를 거부하여 원본 덮어쓰기를 방지합니다.

별도 Git tag는 없습니다. 독립 출력은 위 파일 해시와 GitHub 업로드 커밋으로 보존됩니다. 최종 40자리 커밋 SHA는 저장소 History에서 확인하여 제출 양식에 기록하세요. GitHub 게시를 위한 저장소 URL·공개 별칭 갱신은 연구 수치의 수정이 아닙니다. 로컬 개발 중의 스키마·그래프 처리 수정은 감사 코드의 오류 수정이며, 다른 연구자의 답안을 본 뒤의 모델 수정 실험이 아닙니다.

이번에는 revised run을 수행하지 않았습니다. 이전 커밋, 변경 결정 하나, 예측 효과, 원본/수정 GWP 수치, 절대차·백분율차는 모두 **not applicable**입니다. 향후 수율·공급자·등급 등을 바꾸면 새 식별자와 출력 폴더를 만들고, 오류 수정과 타당한 모델 대안을 구분해 기록해야 합니다.
