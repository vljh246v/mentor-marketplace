#!/usr/bin/env python3
"""
청년미래플러스 멘토링 결과 문서 PDF 생성기.

입력: stdin으로 JSON (data-k 스키마와 동일)
출력: PDF 3개를 --output-dir로 지정한 디렉터리에 저장 (기본은 호출자가 지정)
  - {멘티명}_별지3-1_멘토링일지.pdf  (3회차 합본)
  - {멘티명}_별지3-2_결과보고서.pdf
  - {멘티명}_참여자역량결과보고서.pdf

의존:
  pip install --break-system-packages weasyprint jinja2 mplfonts requests
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"

# Noto Sans CJK ships with mplfonts package
try:
    import mplfonts
    FONT_DIR = Path(mplfonts.__file__).parent / "fonts"
    NOTO_REGULAR = FONT_DIR / "NotoSansCJKsc-Regular.otf"
    NOTO_BOLD = NOTO_REGULAR  # mplfonts has Regular only; bold via CSS font-weight
    if not NOTO_REGULAR.exists():
        raise FileNotFoundError(NOTO_REGULAR)
except Exception as e:
    print(f"한글 폰트 로드 실패: {e}", file=sys.stderr)
    sys.exit(1)


def safe_filename(s: str) -> str:
    """파일명 안전 처리. 한글은 보존."""
    s = re.sub(r"[\\/:*?\"<>|]", "_", s or "")
    return s.strip()[:80] or "untitled"


def load_image_as_data_url(path_or_url: str) -> str:
    """이미지 파일 경로 또는 URL을 base64 data URL로 변환."""
    if not path_or_url:
        return ""
    try:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            import requests
            resp = requests.get(path_or_url, timeout=15)
            resp.raise_for_status()
            ct = resp.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
            data = resp.content
        else:
            p = Path(path_or_url)
            if not p.exists():
                return ""
            data = p.read_bytes()
            ext = p.suffix.lower().lstrip(".")
            ct = f"image/{ {'jpg':'jpeg', 'jpeg':'jpeg', 'png':'png', 'gif':'gif', 'webp':'webp'}.get(ext, 'jpeg') }"
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{ct};base64,{b64}"
    except Exception as e:
        print(f"이미지 로드 실패 ({path_or_url}): {e}", file=sys.stderr)
        return ""


def render_pdf(template_name: str, context: dict, output_path: Path) -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["nl2br"] = lambda s: (s or "").replace("\n", "<br>")
    template = env.get_template(template_name)
    html = template.render(
        font_path=NOTO_REGULAR.as_uri(),
        **context,
    )
    HTML(string=html, base_url=str(SCRIPT_DIR)).write_pdf(str(output_path))


def _detect_session_indices(data: dict) -> list[int]:
    """회차 키 동적 검출 (s1.* ~ sN.*)."""
    indices = set()
    for key in data.keys():
        m = re.match(r"^s(\d+)\.", key)
        if m:
            indices.add(int(m.group(1)))
    return sorted(indices)


def build_journal_pdf(data: dict, output_dir: Path, mentee: str) -> Path:
    """별지 3-1 멘토링 일지 — 진행한 모든 회차 합본 (1~N차 자동 검출)."""
    sessions = []
    for n in _detect_session_indices(data):
        prefix = f"s{n}."
        if not (data.get(prefix + "datetime") or data.get(prefix + "topic") or data.get(prefix + "content")):
            continue
        sessions.append({
            "n": n,
            "datetime": data.get(prefix + "datetime", ""),
            "place": data.get(prefix + "place", ""),
            "place_detail": data.get(prefix + "placeDetail", ""),
            "session": data.get(prefix + "session", ""),
            "topic": data.get(prefix + "topic", ""),
            "content": data.get(prefix + "content", ""),
            "photo1": load_image_as_data_url(data.get(prefix + "photo1", "")),
            "photo2": load_image_as_data_url(data.get(prefix + "photo2", "")),
        })

    ctx = {
        "mentor_org": data.get("mentor.org", ""),
        "mentor_name": data.get("mentor.name", ""),
        "mentee_org": data.get("mentee.org", ""),
        "mentee_name": data.get("mentee.name", ""),
        "field": data.get("mentoring.field", "20. 정보기술"),
        "sessions": sessions,
    }
    out = output_dir / f"{safe_filename(mentee)}_별지3-1_멘토링일지.pdf"
    render_pdf("journal.html", ctx, out)
    return out


def build_report_pdf(data: dict, output_dir: Path, mentee: str) -> Path:
    """별지 3-2 멘토링 결과보고서 (2 페이지)."""
    # 결과보고서 표는 진행한 회차만 행으로 (빈 회차는 누락)
    detected = _detect_session_indices(data)
    table_sessions = []
    for n in detected:
        dt = data.get(f"s{n}.datetime", "")
        tp = data.get(f"s{n}.topic", "")
        if dt or tp:
            table_sessions.append({"n": n, "datetime": dt, "topic": tp})

    ctx = {
        "mentor_org": data.get("mentor.org", ""),
        "mentor_name": data.get("mentor.name", ""),
        "mentee_org": data.get("mentee.org", ""),
        "mentee_name": data.get("mentee.name", ""),
        "field": data.get("mentoring.field", "20. 정보기술"),
        "sessions": table_sessions,
        "outcome": data.get("r.outcome", ""),
        "support": data.get("r.support", ""),
        "suggest": data.get("r.suggest", ""),
        "final": data.get("r.final", ""),
        "sign_year": data.get("r.signYear", ""),
        "sign_month": data.get("r.signMonth", ""),
        "sign_day": data.get("r.signDay", ""),
        "sign_org": data.get("r.signOrg", "") or data.get("mentor.org", ""),
        "sign_title": data.get("r.signTitle", ""),
        "sign_name": data.get("r.signName", "") or data.get("mentor.name", ""),
    }
    out = output_dir / f"{safe_filename(mentee)}_별지3-2_결과보고서.pdf"
    render_pdf("report.html", ctx, out)
    return out


def build_capability_pdf(data: dict, output_dir: Path, mentee: str) -> Path:
    """참여자 역량 결과보고서 (사전 평가지, 1 페이지)."""
    ctx = {
        "date": data.get("cap.date", ""),
        "mentee_name": data.get("mentee.name", ""),
        "target_job": data.get("cap.targetJob", ""),
        "mentor_name": data.get("mentor.name", ""),
        "mentor_group": data.get("cap.mentorGroup", ""),  # 옵셔널 — 셋업에 그룹 멘토가 없으면 빈 값
        "doc_review": data.get("cap.docReview", ""),
        "completeness": data.get("cap.completeness", ""),
        "plan": data.get("cap.plan", ""),
    }
    out = output_dir / f"{safe_filename(mentee)}_참여자역량결과보고서.pdf"
    render_pdf("capability.html", ctx, out)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="청년미래플러스 멘토링 PDF 생성")
    parser.add_argument("--json", "-j", required=True, help="입력 JSON 파일 경로")
    parser.add_argument("--output-dir", "-o", required=True, help="PDF 저장 디렉터리")
    args = parser.parse_args()

    json_path = Path(args.json)
    if not json_path.exists():
        print(f"JSON 파일 없음: {json_path}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    mentee = data.get("mentee.name") or "untitled"

    paths = []
    paths.append(build_journal_pdf(data, output_dir, mentee))
    paths.append(build_report_pdf(data, output_dir, mentee))
    paths.append(build_capability_pdf(data, output_dir, mentee))

    print(json.dumps(
        {"output_dir": str(output_dir), "files": [str(p) for p in paths]},
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
