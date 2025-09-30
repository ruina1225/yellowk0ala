# main_filequeue.py
import os
import time
from dotenv import load_dotenv
from queue_file import dequeue, mark_done, mark_failed
from naver_api import write_blog_post, NaverApiError
from llm import run_llm_transform

load_dotenv()
MAX_RETRY = int(os.getenv("MAX_RETRY", "3"))


def process_item(item: dict):
    """
    item 예시:
    {
      "title": "파타야 3박4일 골프 패키지",
      "content": "원문 텍스트 또는 HTML",
      "categoryNo": 1
    }
    """
    title = item.get("title") or "제목 없음"
    raw_content = item.get("content") or "내용 없음"
    category_no = item.get("categoryNo")

    # 1) LLM 가공 (필요 없으면 주석 처리)
    refined_html = run_llm_transform(raw_content)

    # 2) 업로드 (재시도)
    for attempt in range(1, MAX_RETRY + 1):
        try:
            resp = write_blog_post(title, refined_html, category_no)
            print(f"[OK] attempt={attempt}", resp)
            return True, resp
        except NaverApiError as e:
            print(f"[NAVER FAIL:{attempt}] {e}")
        except Exception as e:
            print(f"[UNEXPECTED:{attempt}] {e}")
        time.sleep(2 * attempt)

    return False, {"error": "max_retry_exceeded"}


def main_loop():
    print("[RUN] file-queue consumer started. Ctrl+C to stop.")
    while True:
        item = dequeue()
        if not item:
            time.sleep(1)
            continue
        path, data = item
        ok, resp = process_item(data)
        if ok:
            mark_done(path)
        else:
            mark_failed(path, reason=str(resp))


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[STOP] bye!")


# # main_filequeue.py
# # 1건을 큐에서 꺼내 scrape → extract → llm → render → post_naver 순으로 처리
# # 성공시 mark_done, 실패시 mark_failed. 인자로 --loop 주면 계속 반복 처리.

# import argparse                          # CLI 인자 파싱
# import os                                # 환경변수
# from dotenv import load_dotenv           # .env 로딩
# from queue_file import dequeue, mark_done, mark_failed  # 큐 API
# from scrape import extract_content       # 스크레이핑
# from extract import extract_locks        # 잠금 추출
# from llm import generate_rewrite         # LLM 재작성
# from render import render_post           # 템플릿 렌더
# from post_naver import upload_post       # 네이버 업로드

# def process_once(max_retry: int) -> bool:
#     """큐에서 1건 처리. 처리했으면 True, 대기열이 비어있으면 False."""
#     url = dequeue()                                      # 큐에서 한 건 꺼내기
#     if not url:                                          # 없으면
#         print("[INFO] 대기열이 비어 있습니다.")           # 안내 로그
#         return False                                     # 처리 안 함

#     print(f"[START] 처리 시작: {url}")                   # 시작 로그
#     try:
#         # 1) 스크레이핑
#         src = extract_content(url)                       # title/text/images 추출
#         title, text, images = src["title"], src["text"], src["images"]

#         # 2) 잠금 추출(가격/기간/날짜)
#         locks = extract_locks(text)                      # {"price":...,"duration":...}

#         # 3) LLM 재작성
#         rewritten = generate_rewrite(title, text, locks) # 재작성 결과(마크다운/HTML)

#         # 4) 템플릿 렌더(자리표 처리 등)
#         html = render_post({
#             "title": title,                              # 제목
#             "body": rewritten,                           # 본문(LLM)
#             "locks": locks,                              # 잠금
#             "images": images,                            # 원문 이미지
#             "source_url": url,                           # 출처
#         })

#         # 5) 업로드(또는 DRY_RUN 프리뷰)
#         res = upload_post(title=title, html_body=html, image_urls=images)

#         if res.get("ok"):
#             mark_done(url)                               # 완료 처리
#             print(f"[DONE] 완료: {url} post_id={res.get('post_id')} preview={res.get('preview_path')}")
#         else:
#             # 실패 → 재시도
#             err = res.get("error", "upload failed")      # 오류 메시지
#             will_retry = mark_failed(url, err, max_retry=max_retry)
#             print(f"[FAIL] 업로드 실패: {url} ({err}) 재시도={will_retry}")
#     except Exception as e:
#         # 파이프라인 도중 예외
#         err = str(e)                                     # 예외 문자열화
#         will_retry = mark_failed(url, err, max_retry=max_retry)  # 실패 기록/재적재
#         print(f"[ERROR] 처리 실패: {url} ({err}) 재시도={will_retry}")

#     return True                                          # 처리 시도는 했음

# def main():
#     load_dotenv()                                        # .env 로드
#     max_retry = int(os.getenv("MAX_RETRY", "3"))         # 최대 재시도 횟수
#     parser = argparse.ArgumentParser()                   # 인자 파서
#     parser.add_argument("--loop", action="store_true", help="대기열이 빌 때까지 반복 처리")  # --loop 옵션
#     args = parser.parse_args()                           # 인자 파싱
#     if args.loop:                                        # 루프 모드?
#         while process_once(max_retry):                   # 처리 성공 동안 반복
#             pass                                         # no-op
#         print("[INFO] 처리 종료(대기열 비움).")          # 종료 안내
#     else:
#         process_once(max_retry)                          # 1회 처리

# if __name__ == "__main__":                               # 스크립트 직접 실행시
#     main()                                               # main 호출

# # ----------------------------------------

# # main_filequeue.py
# # ... (기존 import들)
# from naver_api import write_blog_post

# def process_item(item):
#     """
#     item: 큐에서 꺼낸 dict 예) {"title": "...", "content": "...", "categoryNo": 1}
#     1) 전처리/LLM 가공 (이미 있으시면 그대로)
#     2) 네이버 업로드
#     """
#     title = item.get("title") or "제목 없음"
#     content = item.get("content") or "내용 없음"
#     category_no = item.get("categoryNo")  # 없으면 None

#     # (선택) 여기에서 LLM 가공 로직 수행
#     # content = run_llm_transform(content)

#     # 네이버 블로그 업로드
#     resp = write_blog_post(title, content, category_no)
#     # 업로드 성공/실패 판단 로깅
#     if isinstance(resp, dict) and resp.get("message") == "success":
#         # 네이버 표준 성공 응답 형태 예: {"message":"success","result":{...}}
#         return True, resp
#     else:
#         # 실패 시 resp 안에 error 코드/메시지가 들어있을 수 있음
#         return False, resp

# def main():
#     # ... 큐에서 item 꺼내는 기존 루프
#     # for item in dequeue_loop():
#     #     ok, resp = process_item(item)
#     #     if ok: mark_done(item_id)
#     #     else:  mark_failed(item_id, reason=resp)

#     pass

# if __name__ == "__main__":
#     main()
