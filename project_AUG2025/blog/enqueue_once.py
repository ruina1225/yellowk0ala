import json, uuid
from pathlib import Path
p = Path("queue/inbox"); p.mkdir(parents=True, exist_ok=True)
f = p / f"blogjob_{uuid.uuid4().hex}.json"
item = {"title":"메인 파이프라인 테스트","content":"본문 예시입니다","categoryNo":1}
f.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
print("enqueued:", f)
