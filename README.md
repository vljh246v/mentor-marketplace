# mentor-marketplace

청년미래플러스 멘토용 **Claude Code** 플러그인 모음. 멘토링 워크플로우 전체를 자동화하는 도구를 한곳에 모았습니다.

## 설치 방법

```bash
claude plugin marketplace add https://github.com/vljh246v/mentor-marketplace
claude plugin install mentor-toolkit
```

업데이트 받기:

```bash
claude plugin update mentor-toolkit
```

특정 버전으로 핀:

```bash
claude plugin install mentor-toolkit@v0.1.0
```

---

## 포함된 플러그인

### 🎯 mentor-toolkit `v0.1.0`

청년미래플러스 멘토링 자동화 풀 패키지.

**핵심 기능**:
- 멘티 자료 경로만 알려주면 자동 등록·분석·트래킹
- 회차 사이 결과물 검토(이력서·자소서·PR·학습) 자동화
- 회차 시작 시 컨텍스트 자동 로드 + 1분 브리핑
- 종료 시 청년미래플러스 PDF 3종 직접 생성 (별지 3-1·3-2 + 참여자 역량 결과보고서)
- 한글 폰트 임베드, AI 티 안 나는 자연스러운 한국어 강제 검수

**스킬 10개 + 에이전트 2개**:
- `setup-mentor-toolkit` (1회 셋업)
- `init-mentoring` (새 멘티)
- `start-session` (회차 시작 브리핑)
- `between-sessions` (회차 사이 모든 작업)
- `mentee-analyzer` / `company-recommender` / `resume-reviewer` / `interview-prep`
- `create-report` (PDF 3종 직접 출력)
- `report-writer` (Notion 비공식 정리)
- `company-research-agent` / `mock-interviewer-agent`

자세한 사용법은 [mentor-toolkit/README.md](./mentor-toolkit/README.md) 참고.

---

## 시스템 요구사항

- **Claude Code CLI** — https://docs.claude.com/en/docs/claude-code
- **Notion MCP** 연결 (`claude mcp add notion ...` 또는 `~/.claude.json` / 작업 디렉터리 `.mcp.json` 등록)
- **Python 3.10+** + 다음 패키지 (PDF 생성 시 자동 설치 안내):
  ```bash
  pip install --break-system-packages weasyprint jinja2 mplfonts requests
  ```
  macOS는 `brew install pango libffi` 추가 필요할 수 있음

---

## 기여

이슈·PR 환영합니다. 청년미래플러스 멘토 본인의 워크플로우 개선 아이디어가 있으면 GitHub Issues로.

## 라이선스

MIT (각 플러그인 LICENSE 참고)

## 작성자

jaehyun ([@vljh246v](https://github.com/vljh246v))
