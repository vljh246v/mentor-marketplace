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

### Step 2: Notion `📝 템플릿 모음 > 5️⃣ 결과 보고서 템플릿` 페이지 작성
- Executive Summary
- 회차별 진행 요약 (진행한 만큼만)
- 성장 포인트
- 멘토 종합 평가
- 추천 다음 스텝

### Step 3: 트래커 상태 업데이트
- `완료` 또는 `조기 종료` (이미 그 상태면 유지)
- `최근 업데이트` 오늘로

## 톤

- AI 시그널 단어 ("다양한·지속적·체계적·효과적·전반적") 추방
- 어미 다양화 (~다 / ~음 / ~한다 섞기)
- 구체적 회차·과제·코드 사례 명시
- 추측은 추측이라고 표시

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
