---
name: pre-assessment
description: Generate 참여자역량결과보고서 (사전 평가지) PDF for a mentee before the first session. Use when the user says "OO 사전 평가지 만들어줘", "OO 역량 보고서", "사전 평가지", "pre-assessment", or wants to generate the capability report PDF. Requires init-mentoring to have been completed (mentee analysis must exist in Notion).
---

# Pre-Assessment — 참여자역량결과보고서 PDF 생성

> **전제조건**: 시작 시 `references/preflight-check.md` 절차 수행. 추가 전제: `init-mentoring` 완료 (Notion에 멘티 분석 페이지 존재). 멘티 분석 부재 시 *"init-mentoring을 먼저 실행해서 멘티 분석을 완료해주세요"* 안내 후 종료.
> 1차 멘토링 시작 전에 작성해서 운영기관에 제출.

## 처리 절차

### Step 1: 설정 읽기

`⚙️ 멘토링 설정` 페이지에서:
- 멘토 이름, 소속
- 운영기관 공지 1회차 일자 → `cap.date` (예: `2026.04.29.(수)`)

### Step 2: 멘티 분석 읽기

트래커 DB + 멘티 페이지 + 멘티 분석 하위 페이지에서:
- 희망 직무 → `cap.targetJob`
- 이력서·포트폴리오 평가 내용
- 강점·약점 목록 (mentee-analyzer 결과)
- 멘티 유형 (트랙 결정)

멘티 분석이 Notion에 없으면: *"init-mentoring을 먼저 실행해서 멘티 분석을 완료해주세요"* 안내 후 종료.

### Step 3: cap 필드 작성

`create-report/references/official-form-schema.md`의 `cap.*` 섹션 형식 준수.
`../../references/natural-tone.md` 적용 (AI 시그널 단어 추방).

- **`cap.docReview`**: 이력서·포트폴리오·직무능력은행 계좌 인증서 → ● 4항목 형식
- **`cap.completeness`**: 강점 1~2개 + 약점 1~2개 → "1줄 요지 : 서술" 형식
- **`cap.plan`**: completeness 강점·약점과 1:1 대응 → 구체 강의명·도서명 명시

### Step 3.5: 검수 단계 (PDF 빌드 직전 필수)

작성한 `cap.*` 텍스트 필드(`cap.completeness`, `cap.plan`, `cap.docReview`)를 출력하기 전에 `korean-proofreader-agent`(Task 도구)로 검수한다.

호출 입력:
- 검수할 텍스트 본문 (cap 필드 합본)
- `context: pdf-output` (운영기관 제출 PDF — 존댓말 강제)

반환된 issue 처리:
- `severity: high` (명백한 오타·hallucination) → 즉시 적용
- `severity: medium` / `low` (외래어 표기·반복·톤·AI 시그널) → 멘토에게 1줄로 묶어 confirm 후 적용
- 빈 배열이면 그대로 PDF 빌드 진행

검수 1회 통과 후 빌드. 통과 안 하면 무한 루프 방지를 위해 최대 2회까지만 재검수.

### Step 4: JSON 작성 + PDF 생성

```bash
DATA_JSON=/tmp/pre_assessment_$$.json
OUT_DIR="${MENTOR_OUTPUT_DIR:-$(pwd)}"
mkdir -p "$OUT_DIR"

# CLAUDE_PLUGIN_ROOT는 Claude Code에서는 쓸 수 있지만 Codex에서는 보장되지 않는다.
# Codex에서는 현재 설치된 mentor-toolkit 플러그인 루트 절대경로를 넣는다.
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-/absolute/path/to/mentor-toolkit}"

python3 "${PLUGIN_ROOT}/skills/create-report/scripts/build_pdfs.py" \
  --json "$DATA_JSON" \
  --output-dir "$OUT_DIR" \
  --only capability

```

필요 최소 JSON 키:
```json
{
  "mentor.name": "...",
  "mentor.org": "...",
  "mentee.name": "...",
  "cap.date": "...",
  "cap.targetJob": "...",
  "cap.docReview": "...",
  "cap.completeness": "...",
  "cap.plan": "..."
}
```

의존성 없으면 (venv 권장):
```bash
python3 -m venv ~/.venvs/mentor-toolkit
source ~/.venvs/mentor-toolkit/bin/activate
pip install --quiet weasyprint jinja2 mplfonts requests
```

> fallback: `pip install --user ...`. 마지막 수단으로만 `pip install --break-system-packages ...`. 자세한 설치 안내는 `create-report` 스킬 의존성 섹션 참조.

### Step 5: 결과 안내

출력 경로와 파일명(`{멘티명}_참여자역량결과보고서.pdf`) 알려주기.
도장(인) 부분은 출력 후 수기 처리.

## 🪜 다음 권장 액션

> 출력 카드 마지막에 항상 1~3개 제시. 멘토가 그대로 복사해서 외칠 수 있는 트리거 문구 + 호출될 skill 이름 명시.

- *"OO님 1차 시작"* → start-session (사전 평가지 완료 후 1차 멘토링 진입)
