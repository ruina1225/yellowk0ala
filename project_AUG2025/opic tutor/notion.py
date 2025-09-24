import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import date

# 환경변수 로드
load_dotenv()
NOTION_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DB_ID")

notion = Client(auth=NOTION_KEY)

def save_review_to_notion(topic, weaknesses, improvements, expressions):
    today = str(date.today())

    # 현재 DB의 전체 레코드 수 확인 (→ 순번 자동 증가)
    db_query = notion.databases.query(database_id=DATABASE_ID)
    record_count = len(db_query["results"]) + 1

    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            # Title 속성 (삭제 불가) → 순번 넣기
            "No": {"title": [{"text": {"content": str(record_count)}}]},
            "Date": {"date": {"start": today}},
            "Topic": {"rich_text": [{"text": {"content": topic}}]},
            "Weaknesses": {"rich_text": [{"text": {"content": ", ".join(weaknesses)}}]},
            "Improvements": {"rich_text": [{"text": {"content": ", ".join(improvements)}}]},
            "Expressions": {"rich_text": [{"text": {"content": ", ".join(expressions)}}]},
        }
    )

# 예시: GPT 결과물을 넣는 부분
sample_review = {
    "topic": "Travel, Technology",
    "weaknesses": ["시제 혼동", "어휘 반복", "발음 오류"],
    "improvements": ["과거시제 일관성", "형용사 다양화", "filler expressions 활용"],
    "expressions": [
        "From my perspective…",
        "It is undeniable that…",
        "One possible solution could be…"
    ]
}

save_review_to_notion(
    sample_review["topic"],
    sample_review["weaknesses"],
    sample_review["improvements"],
    sample_review["expressions"]
)

print("✅ Daily Review 저장 완료!")
