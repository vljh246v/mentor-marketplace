---
name: create-report
description: Generate the official 청년미래플러스 mentoring result documents as PDF files directly from a mentee's Notion page. Output 3 PDFs ([별지 3-1] 멘토링 일지 3회차 통합 + [별지 3-2] 결과보고서 + 참여자 역량 결과보고서). Pulls session notes, photos, and analysis from Notion automatically. Writes in natural human-mentor voice — no AI tells. Session datetimes follow the operator's announced schedule (set in 멘토링 설정), not actual mentoring dates. Use when the user says "보고서 만들어줘", "양식 채워줘", "결과보고서 작성", "PDF 뽑아줘", "create report", "역량 결과보고서", "사전 평가지", "공식 양식", "제출용 보고서", or shares a Notion mentee page URL after mentoring ends. Works for any session count (1~N), respects 구직청년/재직청년 track differences.
---

# Create Report — 청년미래플러스 PDF 생성기

> **전제조건**: `setup-mentor-toolkit`이 한 번 실행돼서 `⚙️ 멘토링 설정`이 있어야 함. 없으면 `setup-mentor-toolkit` 먼저 실행하라고 안내 후 종료.

## 결과물 (PDF 3개)

`${OUTPUTS_DIR}/`에 한글 파일명으로 직접 저장:

1. `{멘티명}_별지3-1_멘토링일지.pdf` — 회차별 페이지 분리, 회차당 1장 = 최대 3장
2. `{멘티명}_별지3-2_결과보고서.pdf` — 멘토 종합 + 서명, 2장
3. `{멘티명}_참여자역량결과보고서.pdf` — 사전 평가지, 1장

각 PDF는 weasyprint + Noto Sans CJK 폰트로 한글 정상 렌더링. 사진은 Notion 회차 페이지에서 자동 가져옴. 멘토는 PDF 받자마자 그대로 제출하거나, 서명 부분만 출력 후 수기로 도장.

## 절대 규칙

먼저 다음 reference 3개를 무조건 읽고 시작:
- `references/official-form-schema.md` — data-k 키 매핑 명세
- `references/official-format.md` — 양식 사양
- `references/natural-tone.md` — AI 티 안 나는 작성 규칙

위반 금지:
- **NCS 분야**: `⚙️ 멘토링 설정` 페이지의 NCS 코드 사용
- **회차 일자**: 운영기관 공지 일자 (실제 진행일 아님). 설정 페이지의 "운영기관 공지 회차 일자" 값을 사용
- **트랙 구분**: 구직자·학생·취준 → `구직청년 멘토링 N회차` / 재직자 계열 → `재직청년 멘토링 N회차`
- **AI 시그널 단어 추방**: "다양한·지속적·체계적·효과적·전반적·향후·추후·사료된다"
- **한국어 어미 다양화**: 같은 어미 4번 이상 연속 금지

## 처리 절차

### Step 1: 설정 + 멘티 트래커 읽기

`⚙️ 멘토링 설정` 페이지에서 가져옴:
- 멘토 본인 정보 (소속·성명·직위)
- NCS 분야 코드 (`mentoring.field`)
- 운영기관 공지 회차 일자 (1·2·3차)
- 멘토링 주 분야 (백엔드/프론트/디자인/기획 등 — 분야별 평가 기준 적용)

설정이 없으면 즉시 종료하고 *"먼저 setup-mentor-toolkit을 실행해주세요"* 안내.

`멘티 트래커` DB에서 가져옴:
- 멘티 유형 (트랙 결정)
- 진행 상태, 진행한 회차, 계획 회차, 종료 사유
- 멘티 페이지 URL

**종료 형태 도출** (트래커에 별도 컬럼 없음 — 진행 상태와 회차로 판정):
- 진행 상태 = `조기 종료` → "조기 종료" (보고서 톤·분량 축소)
- 진행한 회차 > 계획 회차 → "연장 완료"
- 그 외 (≥3회 또는 계획대로) → "정상 완료"
- 진행한 회차 = 0 → 보고서 생성 중단 ("회차 데이터가 없습니다. 분석만 있는 상태인데 계속 진행할까요?")

호출 시작 시 진행 상태가 `완료`/`조기 종료`가 아니면 `보고서 작성중`으로 1차 갱신, 보고서 완성 후 최종 상태로 갱신.

### Step 2: Notion 멘티 페이지 컨텍스트 수집

멘티 페이지 fetch + 모든 하위 페이지:
- 멘티 분석 페이지 → 강점·약점·유형·희망 직무
- 1차 멘토링 페이지 → 일시·주제·내용·과제 + 📨 회차 사이 업데이트 + 🤝 멘토 to-do
- 2차 멘토링 페이지 → 동일
- 3차 멘토링 페이지 → 동일
- 추가 회차 페이지(4차+)가 있을 때 모두 수집
- 조기 종료 메모

**빈 회차 처리**: 페이지가 존재하지만 본문이 비어 있으면 *"OO차 노트가 비어있습니다. 진행한 게 맞으면 멘토님이 1~2줄만 알려주세요. 빠뜨리고 PDF 만들면 회차가 누락됩니다"* 1회 확인.

### Step 3: 사진 자동 수집

각 회차 멘토링 페이지에 멘토가 첨부해 둔 이미지를 추출:
- Notion 페이지의 첨부 이미지 URL을 fetch (notion-fetch 결과의 이미지 블록)
- 없으면 빈 자리로 두고 "사진 없음" 표시
- 회차당 최대 2장. 더 많으면 처음 2장만.

### Step 4: 자연스러운 한국어 콘텐츠 작성

각 텍스트 필드를 작성하고 매번 5개 자가 질문 통과:

1. 다른 멘티에 그대로 통할 만큼 일반적인가?
2. 같은 어미 4번 이상 반복?
3. AI 시그널 단어 ≥ 2개?
4. 모든 항목 정확히 같은 분량?
5. 구체적 회차/과제/사례 0개?

하나라도 YES면 다시.

#### 별지 3-1 (멘토링 일지) — 회차당 다음 채움

- `sN.datetime`: 운영기관 공지 일자
- `sN.place`: `대면` / `비대면`
- `sN.placeDetail`: 카페명, Google Meet 등 (Notion 회차 페이지에서)
- `sN.session`: 트랙 + 회차 번호 (예: `구직청년 멘토링 1회차`)
- `sN.topic`: Notion 회차 페이지의 제목/주제
- `sN.content`: ○ 4단 구조 (도입·핵심 활동·멘토 조언·다음 과제). 3차는 마지막 항목을 "마무리·총괄"로

재직청년 트랙 3차는 `sN.content` 하단에 경력설계 로드맵 섹션 추가:
```
○ 경력설계 로드맵 (재직청년 3회차 결과물)
 - 단기 (3개월): ...
 - 중기 (1년): ...
 - 장기 (3년): ...
```

#### 별지 3-2 (결과보고서)

- `r.outcome`: ○ "초기 목표 달성도" + ○ "주요 성과·정성적 변화"
- `r.support`: ○ "후속 지원 필요" + ○ "운영기관 제언"
- `r.suggest`: ○ "운영 애로사항" + ○ "프로그램 개선 제언"
- `r.final`: 한 단락. 멘토 1인칭 OK. 멘티에게 남기는 마지막 말
- `r.signYear/Month/Day`: 제출일
- `r.signOrg/Title/Name`: 설정에서 가져온 멘토 본인 정보

#### 참여자 역량 결과보고서

- `cap.date`: 1회차 진행일자 (운영기관 공지)
- `cap.targetJob`: 멘티 분석에서 추출한 희망 직무
- `cap.docReview`: ● 4항목 (제출 서류 / 이력서 / 포트폴리오 / 직무능력은행)
- `cap.completeness`: ● 강점 1~2개 + 약점 1~2개 (요지 + 서술)
- `cap.plan`: ● 강점·약점에 1:1 대응되는 활동·강의·과제 (구체 강의명·도서명 명시)

### Step 5: PDF 생성 스크립트 호출

데이터를 JSON으로 임시 저장한 뒤 `scripts/build_pdfs.py` 호출:

```bash
# 데이터 JSON을 임시 파일로 저장
DATA_JSON=/tmp/mentor_report_$$.json
echo '<JSON 데이터>' > "$DATA_JSON"

# PDF 생성 (mplfonts·weasyprint 의존)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/create-report/scripts/build_pdfs.py \
  --json "$DATA_JSON" \
  --output-dir "${OUTPUTS_DIR}"

# 결과는 outputs 디렉터리에 3개 PDF
```

스크립트 의존성이 없으면 한 번에 설치:
```bash
pip install --break-system-packages --quiet weasyprint jinja2 mplfonts requests
```

JSON 임시 파일 작성 시 따옴표·`$` 같은 특수문자 안전 처리를 위해 `echo` 대신 Python heredoc 사용 권장:
```bash
python3 -c "
import json, sys
data = $JSON_STRING_AS_PYTHON_DICT
json.dump(data, open('/tmp/mentor_report_$$.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
"
```
또는 Write 도구로 직접 파일 생성.

**재생성 정책**: 같은 멘티에 대해 create-report를 다시 호출하면 기존 PDF는 **덮어쓰기**됩니다. 백업이 필요하면 호출 전 기존 파일을 다른 이름으로 복사. 부분 수정만 원하시면 멘티의 Notion 회차 페이지를 먼저 수정한 뒤 재호출.

### Step 6: 멘티 트래커 상태 갱신

- 정상·연장 완료 → 진행 상태 `완료`
- 조기 종료 → 진행 상태 `조기 종료` 유지
- `최근 업데이트` 오늘로

### Step 7: 사용자에게 결과 안내

```
✅ 결과 보고서 PDF 3종 생성 완료: {멘티}

📄 [View 별지 3-1 멘토링 일지](computer://...)
📄 [View 별지 3-2 결과보고서](computer://...)
📄 [View 참여자 역량 결과보고서](computer://...)

🧾 핵심 요약
- 트랙: {구직청년 / 재직청년}
- 진행 회차: {N}/{M} ({정상 완료 / 연장 완료 / 조기 종료})
- 희망 직무: {targetJob}
- 강점 1 요지: ...
- 약점 1 요지: ...
- 강화 방안 핵심: ...

⚠️ 자동 처리 못 하는 부분 (수기)
- 회차별 사진 (Notion 회차 페이지에 사진 올려두지 않으셨다면 PDF에 빈자리)
- 멘토 도장 (인) — 출력 후 직접
- (재직청년 3차) 경력설계 로드맵 별도 결과물 첨부
```

## 한국어·인코딩 주의

- 모든 파일 UTF-8, BOM 없음
- 파일명에 한글 사용 (한글 OK)
- `scripts/build_pdfs.py`는 `mplfonts.NotoSansCJKsc-Regular.otf`를 통해 한글 폰트 임베드
- weasyprint가 폰트 임베드한 PDF 생성 → 어디서 열어도 한글 깨지지 않음

## 부분 출력 (회차 가변)

- 1회만 진행 → 별지 3-1은 1장만, 결과보고서·역량보고서는 가능한 만큼만 작성
- 4차+ → 별지 3-1은 양식상 3차까지만 표기, 추가 회차 내용은 결과보고서 `r.outcome` 정성적 변화에 압축
- 조기 종료 → 종료 사유 직접 표기 금지. `r.outcome`에 *"OO 시점부터 멘티 사정으로 N회로 마무리"* 자연스럽게 표현

## 다른 스킬과의 관계

- `setup-mentor-toolkit` → 1회 셋업 (이 스킬의 전제)
- `init-mentoring`, `mentee-analyzer`, `company-recommender`, `resume-reviewer`, `interview-prep` → 멘토링 도중 도구
- **`create-report` (이 스킬)** → 멘토링 종료 후 공식 PDF 3종 생성 (종착점)
- `report-writer` → Notion 비공식 자유 정리 (보조)
