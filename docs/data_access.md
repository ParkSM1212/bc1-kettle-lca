# 데이터 접근과 미완료 작업

## 실제 사용한 USLCI 원본

배포된 [원본 매니페스트](../data/source_manifest.json)의 리비전과 SHA-256을 사용합니다. 원본은 공공 USLCI 서버에서 JSON-LD ZIP으로 수집했으며, 배포 압축파일에는 원본 데이터 덤프를 넣지 않았습니다. 원본의 라이선스·인용 조건은 공급처와 각 데이터셋에서 확인해야 합니다. 공개 접근 가능성과 모든 자료에 대한 일괄 재배포 허용은 구분합니다.

기본 재현은 프로젝트 루트에서 `python src/fetch_uslci.py`입니다. `LCA_COMMONS_API_KEY` 환경변수를 먼저 설정하며, 키를 소스·로그·README에 쓰지 않습니다. 공식 안내: [LCA Commons API Guide](https://www.lcacommons.gov/lca-commons-api-guide).

원본을 직접 내려받아 `data/raw/uslci-1.2026-09.0.jsonld.zip`에 둘 수도 있습니다. 해시가 일치하는 파일만 감사 코드가 수용합니다. 공개 저장소의 최신 내용은 나중에 바뀔 수 있으므로 다음 세 정보를 함께 확인합니다.

1. 발행판 `1.2026-09.0`.
2. 저장소 리비전 `fddfc1a7a6c93e1a71f457446df7813245c828e6`.
3. 원본 ZIP SHA-256 `d1b354d11b757efecd8f456077744e83b9c74b4df0d99e18256bdd0335ac5009`.

수집 당시 API 준비 경로는 `/download/json/prepare/National_Renewable_Energy_Laboratory/USLCI_Database_Public`였습니다. 응답은 문서의 JSON 예시와 달리 **일반 텍스트 다운로드 식별자**였습니다. 실제 다운로드는 `/download/json/{식별자}`로 성공했습니다. `data/source_manifest.json`의 식별자는 인증 자격증명이 아니라 공개 저장소 리비전을 식별하는 값입니다.

정확한 원본이 서버에서 더 이상 제공되지 않거나 ZIP의 직렬화 바이트가 변경되면 스크립트가 실패할 수 있습니다. 이를 무시해 해시를 바꾸지 마세요. 같은 리비전의 새 패키지라면 개별 공정 해시를 검토하고 별도 수집 기록과 새 실행을 만들어야 합니다. 최신판으로 바꾸는 경우는 독립적인 새 데이터 시나리오입니다.

API 검색 `/search/`는 이번 실행에서 404였지만 `/search`는 동작했습니다. 연속 검색 중 429 응답도 발생했습니다. 실패를 빈 결과로 해석하지 않았고, 성공적으로 다운로드한 전체 원본을 **오프라인으로 검색**해 최종 검색 기록을 만들었습니다. 따라서 최종 `search_log.csv`에는 누락된 API 페이지나 429를 0건으로 기록한 결과가 없습니다.

## TianGong CLI — 선택적 추가 데이터 확보

사용자가 제공한 [CLI 저장소](https://github.com/tiangong-lca/cli)의 공식 명령과 [npm 패키지 메타데이터](https://registry.npmjs.org/@tiangong-lca%2fcli/latest)를 확인했습니다. 2026-10-08에 조회한 공개 패키지는 `@tiangong-lca/cli` **0.1.27**이며, 명시된 엔진 조건은 Node `>=24.19.0 <25`, pnpm `11.24.0`입니다. 메타데이터 확인은 설치·인증·데이터 검색 실행을 의미하지 않습니다. 이번에는 CLI를 설치하거나 사용자 계정으로 로그인하지 않았습니다.

해당 런타임을 갖춘 환경에서 아래는 공식 CLI 방식에 버전을 고정한 추가 검색 명령입니다. 실제 실행하지 않은 선택적 절차입니다.

```powershell
node --version
pnpm --version
pnpm dlx @tiangong-lca/cli@0.1.27 --help
pnpm dlx @tiangong-lca/cli@0.1.27 auth login
pnpm dlx @tiangong-lca/cli@0.1.27 auth doctor-auth --json
pnpm dlx @tiangong-lca/cli@0.1.27 search process --input inputs/tiangong-search/04-pp.json --json
```

일반 Production 로그인은 공식 CLI의 기본 설정과 브라우저 OAuth를 사용합니다. 별도 환경에서 필요한 설정 이름에는 `TIANGONG_LCA_API_BASE_URL`, `TIANGONG_LCA_SUPABASE_PUBLISHABLE_KEY`, `TIANGONG_LCA_OAUTH_CLIENT_ID`, `TIANGONG_LCA_OAUTH_REDIRECT_URI`, `TIANGONG_LCA_REGION`이 있습니다. 값은 제공처의 해당 환경 설정을 사용해야 합니다. 이번 프로젝트는 해당 값을 수집·저장하지 않습니다.

12개 재료용 검색 요청 JSON을 [`inputs/tiangong-search/`](../inputs/tiangong-search/)에 준비했습니다. **검색 결과 파일이 아니라 요청문**입니다. 새로 찾은 데이터는 UUID·버전·지역·기간·기준 흐름·단위·공급자·경계를 확인하고, 원본 바이트 해시와 접근권한을 기록해야 합니다. 검색 결과를 자동으로 USLCI와 혼합하지 않습니다.

[TianGong 과거 데이터 저장소](https://github.com/tiangong-lca/data)는 2026-06-21 이후 유지보수를 종료한 과거 스냅샷으로 안내됩니다. 최신 자료는 [TianGong 플랫폼](https://lca.tiangong.earth/)의 데이터셋 Export 경로를 이용해야 합니다.

## 전체 LCA 계산에 남은 외부 의존성

- USLCI 전력 연결에 필요한 [U.S. electricity baseline](https://www.lcacommons.gov/lca-collaboration/Federal_LCA_Commons/US_electricity_baseline/datasets) 및 기타 외부 공급자료. 통합 옵션은 [Commons Merged 공식 안내](https://flcac-admin.github.io/FLCAC-docs/commons-merged/) 참고. 이번 수집에는 이 저장소를 포함하지 않았습니다.
- 금액 기반 연결을 쓸 경우 실제 연결 대상 USEEIO 데이터, 부문 적합성, 2012 USD producer-price 기준 검증. 나일론 등급·구리 제품 단계의 일치 여부가 추가로 필요합니다.
- 황동·POM·실리콘 물리적 자료 또는 근거가 있는 대체안, 원료/제품 등급 및 혼합비.
- 공장 수율·가공·조립·운송·스크랩 처리, 후보 공정과 BOM 포장의 중복 조정.
- FEDEFL에 맞는 GWP100 특성화 방법과 실제 LCIA 솔버. 이번 코드에는 해당 솔버가 구현되어 있지 않습니다.

계정·데이터가 없는 단계를 완료했다고 표시하지 않습니다. `not calculated`는 위 작업을 명시적으로 남긴 연구 결과 상태입니다.
