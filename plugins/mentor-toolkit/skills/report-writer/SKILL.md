---
name: report-writer
description: Write a freeform Notion-only mentoring summary (강점·약점·다음 스텝) — useful for internal mentor notes or sharing a casual recap with a mentee outside official submission. For the OFFICIAL 운영기관 제출용 양식 (PDF 3종), use the `create-report` skill instead. Use this skill when the user explicitly says "노션에만 정리해줘", "비공식 정리", "멘티에게 보낼 요약" — otherwise default to `create-report`.
---

# Report Writer (Notion 전용 비공식 정리)

> **공식 양식 PDF가 필요하면 이 스킬이 아니라 `create-report`를 사용.** 이 스킬은 노션에 자유 형식으로 정리하는 보조 도구.

## 언제 사용

- 멘토 본인의 회고용 메모
- 멘티에게 가벼운 종합 요약을 노션 페이지로 공유
- 공식 양식 작성 전 초안

공식 제출용 양식이 필요하면 즉시 `create-report`로 위임:
> "공식 운영기관 제출용 PDF 3종이 필요하시면 *'OO님 보고서 PDF 만들어줘'* 라고 말씀해 주세요."

## 처리 절차

### Step 1: Notion 컨텍스트 수집
- 멘티 분석 페이지
- 1차~N차 멘토링 페이지 (진행한 회차 동적 검출)
- (있을 때) 조기 종료 메모

## 검수 단계 (출력 직전 필수)

작성한 한국어 텍스트를 출력하기 전에 `korean-proofreader-agent`(Task 도구)로 검수한다.

호출 입력:
- 검수할 텍스트 본문
- `context: notion-note` / `notion-analysis` / `pdf-output` / `chat-card` 중 적절한 값 명시
  (이 skill의 경우 `context: notion-note`)

반환된 issue 처리:
- `severity: high` (명백한 오타·hallucination) → 즉시 적용
- `severity: medium` / `low` (외래어 표기·반복·톤·AI 시그널) → 멘토에게 1줄로 묶어 confirm 후 적용
- 빈 배열이면 그대로 출력

검수 1회 통과 후 출력. 통과 안 하면 무한 루프 방지를 위해 최대 2회까지만 재검수.

### Step 2: Notion `📝 템플릿 모음 > 5️⃣ 결과 보고서 템플릿` 페이지 작성
- Executive Summary
- 회차별 진행 요약 (진행한 만큼만)
- 성장 포인트
- 멘토 종합 평가
- 추천 다음 스텝

### Step 3: 트래커 상태 업데이트
- `완료` 또는 `조기 종료` (이미 그 상태면 유지)
- `최근 업데이트` 오늘로

## 한국어 톤 규칙

이 skill이 작성하는 모든 한국어 텍스트는 plugin 루트의 `references/natural-tone.md`를 따른다 — AI 시그널 단어 추방, 어미 다양화, 같은 어미 4번 이상 반복 금지, 안전 표현 남발 금지. 작성 후 그 reference의 자가 점검 5문항을 한 번 통과시켜야 출력 가능.

## 출력 (채팅 요약 카드)

```
✅ Notion 정리 완료: {멘티}

📄 노션 페이지: {URL}

🧾 핵심 요약
- 시작점: {1줄}
- 도달점: {1줄}
- 가장 큰 변화: {1줄}

🪜 다음 권장 액션
- *"OO님 보고서 PDF 만들어줘"* → create-report (운영기관 제출용 PDF 3종 공식 생성)
```

## 다른 스킬과의 관계

- **`create-report`**: 공식 PDF 3종 직접 생성 (이쪽이 메인 결과물). 이 스킬은 보조.
- `init-mentoring`, `mentee-analyzer`, `company-recommender`, `resume-reviewer`, `interview-prep`: 멘토링 도구
