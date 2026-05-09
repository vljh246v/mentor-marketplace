# 채용 사이트 활용 가이드

회사 추천 시 정적 DB보다 **실시간 채용 공고**가 우선이다. 멘토가 추천할 때 "지금 뽑고 있는 곳"을 기준으로 매칭해야 멘티에게 의미 있다.

## 수집 도구 우선순위

1. **Scrapling MCP 우선 (선택 의존성)**
   - 검색 결과 페이지: `mcp__scrapling__.bulk_fetch`
   - 상세 페이지 검증: `mcp__scrapling__.fetch`
   - JS 렌더링/보호/부분 응답: `mcp__scrapling__.stealthy_fetch` 또는 `bulk_stealthy_fetch`
   - 권장 옵션: `locale: ko-KR`, `timezone_id: Asia/Seoul`, `wait: 3000~8000`, 필요 시 `network_idle: true`
2. **Fallback**
   - Scrapling MCP가 없거나 사이트가 전부 막히면 WebFetch/WebSearch를 사용한다.
   - 그래도 막히면 사용자에게 JD 텍스트나 공고 URL을 붙여달라고 요청한 뒤 매칭만 수행한다.

Scrapling MCP는 플러그인 필수 설치 조건이 아니다. 다만 Scrapling 없이 fallback으로 만든 추천에는 수집 방식과 검증 신뢰도 제한을 표시한다. Scrapling 결과는 검색 결과와 상세 페이지가 다를 수 있다. 검색 목록에서 찾은 후보라도 반드시 상세 페이지에서 `지원하기`/`지원마감`/`마감 또는 삭제` 상태를 확인한다.

## 1차 소스 (한국 백엔드 채용 핵심 3곳)

### 원티드 (Wanted) — https://www.wanted.co.kr
- 신입~5년차 IT 직군 강세, 모던 스택 회사 多
- 검색 URL 패턴 (참고):
  - 백엔드 전체: `https://www.wanted.co.kr/wdlist/518/872`
  - 키워드 검색: `https://www.wanted.co.kr/search?query=백엔드 자바`
- 공고 페이지에서 추출할 것: 회사명, 포지션, 요구 경력, 주요 기술, JD 본문, 우대사항, 연봉(있으면)
- 회사 페이지: `https://www.wanted.co.kr/company/{회사ID}` — 회사 소개·재직자 후기

### 사람인 (Saramin) — https://www.saramin.co.kr
- 채용 공고 양 가장 많음, SI·중견·대기업 포함
- 검색 URL 패턴: `https://www.saramin.co.kr/zf_user/search/recruit?searchword=백엔드`
- 직군 코드(`cat_kewd`)로 필터 가능 — 백엔드 개발자: `cat_kewd=84`
- 검색 결과 페이지에서 회사명·연차·지역·마감일 일괄 추출
- 단점: SI/SM 회사가 다수 섞여 있어 필터 필요

### 직행 (Zighang) — https://zighang.com
- 개발자 특화, 큐레이션 채용 (잡플래닛 + 채용)
- IT 회사 기준 깐깐, 노이즈 적음
- 카테고리·연차로 필터 가능
- 단점: 공고 수는 위 둘보다 적음, 보완 소스로 활용
- URL 검색 파라미터가 실제 필터에 반영되지 않을 수 있음. 홈/공고 목록에서 후보를 찾은 뒤 상세 페이지 URL(`/recruitment/{id}`)로 재검증.

## 2차 소스 (보조)

- **잡플래닛**: 회사 평가·연봉 검증
- **잡코리아**: 사람인과 유사, 보조용
- **링크드인**: 경력 5년+ 시니어, 외국계
- **회사별 공식 채용 페이지**: 토스/카카오/우아한형제들 등은 공식 사이트가 더 빠름
- **Disquiet**, **데모데이**: 시리즈 A 이전 초기 스타트업

## 회사 검증 소스

추천 후보는 `company-validation.md`의 회사 검증 게이트를 통과해야 한다. 검증 소스 우선순위:

1. 공식 홈페이지 또는 공식 채용 페이지
2. 채용 상세 JD 원문
3. 사람인·잡코리아·원티드 회사 페이지의 기업정보
4. 잡플래닛·블라인드·크레딧잡 등 평판 보조 소스
5. 최근 뉴스 검색
6. DART 또는 기업 공시가 있는 회사는 공시 정보

주의:
- 평판 사이트 점수는 단독 결정 근거로 쓰지 않는다.
- 동일한 부정 시그널이 2개 이상 출처에서 반복되면 C 또는 D로 낮춘다.
- 공식 홈페이지나 기업정보가 전혀 확인되지 않으면 추천하지 않는다.

## 검색 전략

### Step 1: 키워드 조합 만들기
멘티 정보에서 다음을 조합해 검색 쿼리 생성:
- **유형 + 연차**: "백엔드 신입" / "백엔드 3년차" / "Java 시니어"
- **스택**: "Spring Boot Kotlin" / "Java JPA"
- **도메인** (있으면): "핀테크 백엔드" / "커머스 Java"
- **희망 조건**: "원격" / "외국계" 같은 보조 토큰

### Step 2: 사이트별 분배
- 신입~3년차 → 원티드 60% + 사람인 30% + 직행 10%
- 3~7년차 → 원티드 50% + 직행 30% + 사람인 20%
- 7년+ → 링크드인 + 회사 직접 채용 페이지 우선
- SI 회피 멘티 → 원티드·직행 위주, 사람인은 필터 강하게

### Step 3: 공고 수집·필터
Scrapling MCP로 검색 결과 페이지를 가져온 뒤:
- 회사명 중복 제거 (같은 회사가 5개 공고 올린 경우 1개만)
- 마감 임박 공고 우선 표시
- 멘티 거주지 기반 지역 필터
- "주말근무" "야간가능" 같은 키워드 있으면 자동 감점
- 상세 페이지에서 마감/삭제/지원마감이면 추천 후보에서 제외하거나 "마감 가능성" 주의로 격하

### Step 4: 회사 검증 게이트
주요 후보 회사 5~10개에 대해 `company-validation.md` 기준으로 검증한다:
- 회사 페이지 fetch → 규모, 도메인, 시리즈 단계
- 공식 홈페이지 또는 공식 채용 페이지 확인
- 사람인·잡코리아·원티드 회사 페이지로 업력, 규모, 소재지 확인
- 가능하면 잡플래닛·블라인드·크레딧잡·뉴스로 평판 보조 확인
- `references/company-database.md`의 정성 평가와 교차 확인
- A/B/C/D 검증 등급, 검증 신뢰도, 확인 출처, 주요 리스크 기록

### Step 5: 매칭 룰 적용
`matching-rules.md`의 5차원 점수를 각 회사에 매김. 25점 만점. 단, D등급은 제외하고 C등급은 메인 트랙에 올리지 않는다.

## 출력에 반영할 정보

각 추천 회사 카드에 다음 포함:
- 회사명 + JD 링크 (원티드/사람인/직행 중 어디서 찾았는지)
- 포지션명·요구 경력·주요 스택
- 핏 점수 (5차원 합계)
- 검증 등급 (A/B/C/D)
- 검증 신뢰도 (높음/보통/낮음)
- 수집 방식 (Scrapling MCP/WebSearch fallback/사용자 제공 JD)
- 확인 출처 (JD, 공식 홈페이지, 기업정보, 평판/뉴스 등)
- 핵심 매칭 이유 (1~2줄)
- 주요 리스크 / 부족한 역량 / 보강 액션
- 마감일 (있으면)

## 주의사항

- Scrapling/WebFetch 결과는 시간이 지나면 다시 갱신해야 함. 출력 끝에 *"※ 검색 시점: YYYY-MM-DD"* 명시.
- 채용 사이트의 robots.txt·이용약관 존중. 본 스킬은 사람이 사용할 후보 추천이지 자동 지원이 아님.
- Scrapling과 WebFetch가 모두 막히면 사용자에게 사이트 직접 검색 후 JD 텍스트를 붙여달라고 요청 → 그 텍스트로 매칭 룰 적용.
- 회사 평가는 멘토 시점 의견임을 명시. 결정은 멘티가 직접 (잡플래닛, 지인 평판, 면접 시 분위기).

## Scrapling MCP 호출 예시

검색 결과 병렬 수집:

```json
{
  "urls": [
    "https://www.wanted.co.kr/search?query=%EB%B0%B1%EC%97%94%EB%93%9C%20Spring%203%EB%85%84%EC%B0%A8&tab=position",
    "https://www.saramin.co.kr/zf_user/search/recruit?searchword=%EB%B0%B1%EC%97%94%EB%93%9C%20Spring%203%EB%85%84%EC%B0%A8",
    "https://zighang.com/"
  ],
  "extraction_type": "markdown",
  "main_content_only": true,
  "locale": "ko-KR",
  "timezone_id": "Asia/Seoul",
  "wait": 5000
}
```

상세 페이지 검증:

```json
{
  "url": "https://www.wanted.co.kr/wd/123456",
  "extraction_type": "markdown",
  "main_content_only": true,
  "locale": "ko-KR",
  "timezone_id": "Asia/Seoul",
  "wait": 2000
}
```

추출된 결과를 멘티 프로필과 매칭 룰에 통과시켜 점수화.
