import json, uuid
from pathlib import Path

p = Path("queue/inbox"); p.mkdir(parents=True, exist_ok=True)
f = p / f"job_{uuid.uuid4().hex}.json"
item = {
  "title": "엔드투엔드 테스트",
  "content": "이 본문은 자동 글 생성 파이프라인 테스트용입니다.",
  "categoryNo": 1
}
f.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
print("enqueued:", f)
