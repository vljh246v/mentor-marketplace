# Preflight Check — 셋업 전제조건 검증

여러 스킬이 시작 시 동일하게 수행하는 표준 절차. 스킬은 이 파일 절차를 따르고, 결과에 따라 진행/종료를 결정한다.

## 검증 단계

### 1. `⚙️ 멘토링 설정` 페이지 존재 확인

Notion 워크스페이스 검색으로 정확 일치 페이지 1개를 찾는다.

```
notion-search query: "멘토링 설정"
```

`⚙️ 멘토링 설정` 제목 페이지가 결과에 없으면 **부재** 판정.

### 2. 페이지 본문 무결성 확인

존재 시 페이지를 fetch해서 다음 필드 확인:

- `mentor.name`, `mentor.org`, `mentor.title` (멘토 본인)
- `mentoring.field` (NCS 분야 코드)
- `📚 멘토링 자동화 허브` 부모 링크

하나라도 비어 있으면 **불완전** 판정.

### 3. 결과 처리

| 상태 | 동작 |
|------|------|
| 존재 + 완전 | 다음 단계로 진행 |
| 부재 | 아래 부재 메시지 안내 + 종료 |
| 불완전 | 아래 불완전 메시지 안내 + 종료 |

## 표준 안내 메시지

### 부재 시

```
멘토링 설정 페이지가 Notion에 없습니다.
먼저 setup-mentor-toolkit 스킬을 실행해서 셋업을 완료해주세요.

실행 방법: 
> 셋업해줘
```

### 불완전 시

```
⚙️ 멘토링 설정 페이지에 누락된 항목이 있습니다: {필드 목록}
setup-mentor-toolkit을 다시 실행하거나 Notion에서 직접 채워주세요.
```

## 추가 전제 (스킬별)

특정 스킬은 위 검증에 추가 조건이 붙는다. 본인 SKILL.md 상단 frontmatter 직후에 명시.

| 스킬 | 추가 전제 |
|------|----------|
| `init-mentoring` | 없음 |
| `mentee-analyzer` | 멘티 트래커에 해당 멘티 행 존재 |
| `pre-assessment` | `init-mentoring` 완료 (멘티 분석 페이지 존재) |
| `create-report` | 멘티 페이지에 회차 노트 1개 이상 존재 |
| `start-session` / `end-session` / `between-sessions` | 트래커에 해당 멘티 등록됨 |
| `company-recommender` / `resume-reviewer` / `interview-prep` | 멘티 분석 완료 권장 (없으면 일반 답변) |
