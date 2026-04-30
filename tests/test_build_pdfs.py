"""build_pdfs.py 회귀 테스트.

dry-run 모드로 weasyprint 없이 jinja2만으로 템플릿 렌더 검증.
실 PDF 생성은 별도 통합 테스트 또는 수동 확인.

실행:
    pip install jinja2 mplfonts pytest
    pytest tests/

mplfonts가 설치돼 있지 않으면 dry-run에서도 폰트 로드 단계가 생략돼야 하지만
스크립트가 _load_runtime을 호출하지 않으므로 무관함.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "plugins/mentor-toolkit/skills/create-report/scripts/build_pdfs.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run_dry(json_path: Path, output_dir: Path, only: list[str] | None = None):
    cmd = [sys.executable, str(SCRIPT), "--json", str(json_path), "--output-dir", str(output_dir), "--dry-run"]
    if only:
        for o in only:
            cmd += ["--only", o]
    return subprocess.run(cmd, capture_output=True, text=True)


@pytest.fixture
def out_dir(tmp_path):
    return tmp_path / "out"


def test_full_three_sessions(out_dir):
    """3회차 fullcase: journal + report 양쪽 dry render 성공."""
    result = run_dry(FIXTURES / "sample_full.json", out_dir, only=["journal", "report"])
    assert result.returncode == 0, result.stderr

    journal = out_dir / "김지훈_별지3-1_멘토링일지.dry.html"
    report = out_dir / "김지훈_별지3-2_결과보고서.dry.html"
    assert journal.exists(), f"journal sidecar 누락: {journal}"
    assert report.exists(), f"report sidecar 누락: {report}"

    journal_html = journal.read_text(encoding="utf-8")
    # 3회차 모두 렌더됐는지 토픽 키워드로 검증
    assert "이력서 점검과 1차 목표 설정" in journal_html
    assert "포트폴리오와 기술 깊이 보강" in journal_html
    assert "모의 면접과 마무리" in journal_html

    report_html = report.read_text(encoding="utf-8")
    assert "김지훈" in report_html
    assert "홍길동" in report_html


def test_minimal_one_session_dynamic_detection(out_dir):
    """1회차 단축 케이스: s1만 있어도 정상 렌더, s2/s3 출력 없음."""
    result = run_dry(FIXTURES / "sample_minimal.json", out_dir, only=["journal"])
    assert result.returncode == 0, result.stderr

    journal = out_dir / "박미영_별지3-1_멘토링일지.dry.html"
    assert journal.exists()

    html = journal.read_text(encoding="utf-8")
    assert "포트폴리오 진단" in html
    # 회차 검출은 동적 — 빈 회차 키 없으면 추가 회차 채움 없음.
    # 템플릿에 '3회차' 정적 안내문이 있어 키워드 매치 대신 채워진 cell 패턴으로 검증.
    assert '<td class="fill">1회차</td>' in html
    assert '<td class="fill">2회차</td>' not in html
    assert '<td class="fill">3회차</td>' not in html


def test_capability_only(out_dir):
    """pre-assessment용 capability 단독 생성."""
    result = run_dry(FIXTURES / "sample_capability.json", out_dir, only=["capability"])
    assert result.returncode == 0, result.stderr

    cap = out_dir / "이수진_참여자역량결과보고서.dry.html"
    assert cap.exists()

    html = cap.read_text(encoding="utf-8")
    assert "이수진" in html
    assert "서비스 기획자" in html
    assert "북극성 지표" in html


def test_default_generates_all_three(out_dir):
    """--only 생략 시 PDF 3종 모두 생성."""
    result = run_dry(FIXTURES / "sample_full.json", out_dir, only=None)
    assert result.returncode == 0, result.stderr

    assert (out_dir / "김지훈_별지3-1_멘토링일지.dry.html").exists()
    assert (out_dir / "김지훈_별지3-2_결과보고서.dry.html").exists()
    assert (out_dir / "김지훈_참여자역량결과보고서.dry.html").exists()


def test_missing_json_returns_error(tmp_path):
    """JSON 부재 시 종료 코드 2."""
    result = run_dry(tmp_path / "nonexistent.json", tmp_path / "out")
    assert result.returncode == 2
    assert "JSON 파일 없음" in result.stderr


def test_filename_safe_korean(out_dir):
    """한글 파일명에 위험 문자가 없으면 그대로 사용."""
    result = run_dry(FIXTURES / "sample_full.json", out_dir, only=["report"])
    assert result.returncode == 0
    expected = out_dir / "김지훈_별지3-2_결과보고서.dry.html"
    assert expected.exists()
