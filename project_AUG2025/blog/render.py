# render.py
# templates/post.md.j2 템플릿에 context를 주입해 최종 본문(마크다운/HTML)을 생성

from jinja2 import Environment, FileSystemLoader   # 템플릿 로더/엔진
from pathlib import Path                            # 경로 처리

TEMPLATES_DIR = Path("templates")                   # 템플릿 폴더 경로

def render_post(context: dict) -> str:
    """
    context 예시:
    {
      "title": "...",
      "body": "...(LLM 결과)",
      "locks": {...},
      "images": ["...","..."]
    }
    """
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))  # 템플릿 엔진 준비
    tpl = env.get_template("post.md.j2")                            # 템플릿 선택
    return tpl.render(**context)                                    # 렌더 결과 문자열 반환
