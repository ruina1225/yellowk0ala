from pathlib import Path
from queue_file import mark_done

p = Path("queue/processing")
for f in p.glob("*.json"):
    print("MARK_DONE:", f)
    mark_done(f, {"postId": "MANUAL-OK"})
