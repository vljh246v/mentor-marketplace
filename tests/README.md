# tests

`build_pdfs.py` 회귀 테스트.

## 실행

```bash
# venv 권장
python3 -m venv ~/.venvs/mentor-toolkit
source ~/.venvs/mentor-toolkit/bin/activate

pip install jinja2 mplfonts pytest

pytest tests/ -v
```

`weasyprint`는 dry-run 테스트에서 사용하지 않으므로 시스템 라이브러리(pango/cairo) 없이도 실행 가능.

## 무엇을 검증하나

| 테스트 | 시나리오 |
|--------|----------|
| `test_full_three_sessions` | 3회차 정상 케이스 — journal + report 둘 다 렌더 |
| `test_minimal_one_session_dynamic_detection` | 1회차 조기 종료 — `s1.*`만 있을 때 회차 검출 정확 |
| `test_capability_only` | `pre-assessment`가 호출하는 `--only capability` 경로 |
| `test_default_generates_all_three` | `--only` 미지정 시 PDF 3종 |
| `test_missing_json_returns_error` | 존재하지 않는 JSON 입력 시 exit code 2 |
| `test_filename_safe_korean` | 한글 멘티명이 파일명에 그대로 보존 |

## fixture 추가

`tests/fixtures/sample_*.json`에 케이스 추가. 새 fixture를 쓰는 테스트도 함께 추가.
