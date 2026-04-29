---
name: end-session
description: Close out a completed mentoring session by reading the Notion session page first, then structuring and distributing notes to the correct sections. Update the mentee tracker automatically. Use when the user says "OO N차 끝", "N차 끝났어", "N차 미팅 끝", "방금 N차 끝", "OO N차 종료", "end session", or any phrase indicating a session just finished. Distinct from between-sessions (which handles the inter-session gap) — end-session is triggered immediately after a session, reads Notion first, and asks only for gaps.
---

# End Session — 회차 마무리

> **위치**: `start-session`(회차 시작) → 멘토링 진행 → ⭐ **end-session(회차 종료)** → `between-sessions`(회차 사이 작업) → `start-session`(다음 회차)

회차가 끝난 직후 호출. **Notion 먼저 읽고**, 없는 것만 묻는다.

## 원칙

1. **Notion-first**: 멘티 이름 + 회차 번호를 확인하자마자 Notion 회차 페이지 즉시 fetch. 질문 먼저 하지 않는다.
2. **빈 자리만 질문**: fetch 후 비어있는 섹션만 1개 메시지에 묶어서 묻는다. 이미 있는 내용은 다시 묻지 않는다.
3. **트래커 자동 갱신**: 처리 완료 후 진행한 회차 +1, 진행 상태 갱신.

---

## 처리 절차

### Step 1: 멘티 + 회차 식별

발화에서 멘티 이름과 회차 번호 파싱:
- "권미리 1차 끝" → 멘티: 권미리, 회차: 1
- "박다솔 2차 미팅 끝났어" → 멘티: 박다솔, 회차: 2
- "방금 N차 끝" (이름 없음) → 트래커에서 현재 진행 중인 멘티 확인 후 1회 확인

회차 번호가 불명확하면 트래커의 `진행 상태`에서 현재 진행 중인 회차 자동 추론.

### Step 2: Notion 회차 페이지 즉시 fetch

트래커에서 멘티 페이지 URL → 해당 회차 하위 페이지 fetch.

페이지가 없으면: *"N차 페이지가 Notion에 없습니다. start-session으로 만드셨나요?"* 1회 확인.

fetch 결과를 다음 섹션으로 분류 (섹션명은 정규 구조 그대로):
- `🗣️ 대화 노트`
- `🤔 멘티가 한 말`
- `💡 멘토 코멘트`
- `📝 다음 회차 과제`
- `📅 다음 멘토링 예정일`
- `🤝 멘토 to-do`

### Step 3: 빈 섹션 파악 → 최소 질문

fetch 결과에서 **비어있는 섹션만** 하나의 메시지로 묶어 묻기.

이미 작성된 섹션은 묻지 않는다.

예시 (과제·예정일만 없을 때):
```
N차 페이지 읽었습니다. 2가지만 확인:

1. 다음 회차까지 부여한 과제 (없으면 "없음"):
2. 다음 멘토링 예정일 (모르면 "미정"):
```

모든 섹션이 채워져 있으면 바로 Step 4로.

### Step 4: 회차 페이지 구조화 + 기록

Notion 회차 페이지의 각 섹션이 올바른 형식으로 채워지도록 업데이트:

**🗣️ 대화 노트**
- 자유 텍스트를 bullet 3~5개로 압축
- 구체적 사실 위주 (추상 평가 제거)

**🤔 멘티가 한 말**
- 멘티가 직접 말한 것 위주
- AI 해석 최소화

**💡 멘토 코멘트**
- 멘토가 준 조언·피드백 정리
- 자연스러운 한국어 (natural-tone 규칙 적용)

**📝 다음 회차 과제**
```
- [ ] 과제 1 (예: 자기소개서 v2 작성)
- [ ] 과제 2 (예: 인프런 Spring Security 강의 3시간)
```

**📅 다음 멘토링 예정일**
`YYYY.MM.DD.(요일)` 형식으로 기록

**🤝 멘토 to-do** (있을 때만)
```
- [ ] 멘토가 할 것 (예: 지원 공고 3개 추려두기)
```

**📷 사진** (있을 때만)
- 회차 페이지의 `📷 사진` 섹션에 이미지 블록이 있으면 URL 확인만 (별도 처리 없음)
- 없으면 안내: *"회차 사진이 없습니다. PDF에 빈자리로 표시됩니다. 추가하려면 Notion 회차 페이지 `📷 사진` 섹션에 첨부하세요."*

### Step 5: 트래커 갱신

- `진행한 회차`: N차 완료 → N으로 갱신 (이미 N이면 그대로)
- `진행 상태`: N차 완료 기준으로 갱신
  - 1차 완료 → `2차 진행` (계획 회차 ≥ 2인 경우) 또는 `보고서 작성중` (계획 회차 1)
  - 2차 완료 → `3차 진행` 또는 `보고서 작성중`
  - 마지막 회차 완료 (진행한 회차 = 계획 회차) → `보고서 작성중`
- `최근 업데이트`: 오늘 날짜

### Step 6: 결과 안내

```
✅ {멘티명} {N}차 마무리 완료

📋 정리된 내용
- 핵심 대화: {1줄 요약}
- 과제: {과제 수}개 부여
- 다음 예정일: {날짜 or 미정}

📁 {N}차 페이지: {Notion URL}
📊 트래커: {진행한 회차} / {계획 회차}차 → 상태: {진행 상태}

💡 다음 단계
- between-sessions: 회차 사이 멘티 결과물 검토·미완 과제 처리
- start-session: {N+1}차 시작 시 이전 내용 자동 로드
```

---

## 엣지 케이스

**Notion 페이지는 있지만 완전히 비어있는 경우**

한 번에 묶어서 짧게 묻기:
```
{N}차 페이지가 비어있습니다. 간단히 알려주시면 채울게요:

1. 오늘 어떤 얘기 했나요? (짧게 OK):
2. 다음 회차 과제:
3. 다음 예정일:
4. 멘티가 한 인상적인 말 (있으면):
```

**조기 종료인 경우**

"더 이상 진행 안 해요" 또는 유사 발화 → 트래커 진행 상태 `조기 종료`로 갱신, 종료 사유 메모 기록, create-report 안내.

---

## 다른 스킬과의 관계

- **`start-session`**: 다음 회차 시작 시 end-session이 기록한 과제·예정일·멘토 to-do 자동 로드
- **`between-sessions`**: end-session 이후 회차 사이 기간 — 결과물 검토·미완 과제 처리 담당
- **`create-report`**: 마지막 회차 end-session 완료 후 PDF 생성 안내
