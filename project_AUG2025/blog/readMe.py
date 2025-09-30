# naver-golf-bot/
#   .env                      # NAVER API or 계정정보
#   urls.txt                  # 재가공할 원문 블로그 URL 목록
#   main.py                   # 엔트리포인트(스케줄 포함)
#   scrape.py                 # 네이버 블로그 파서
#   extract.py                # 가격/날짜/조건 추출기(정규식)
#   llm.py                    # Ollama 호출
#   render.py                 # 템플릿 렌더링(Jinja2)
#   post_naver.py             # API/Playwright 업로더
#   templates/
#     post.md.j2              # 출력 템플릿 (Markdown/HTML)
#   data/
#     cache/                  # 원문 캐시
#     out/                    # 생성 결과(리뷰/검증 로그)


