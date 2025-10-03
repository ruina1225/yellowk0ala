import os, json
from pathlib import Path
import queue_file

print("CWD:", os.getcwd())
print("PY:", __import__("sys").executable)
print("INBOX     :", queue_file.INBOX)
print("PROCESSING:", queue_file.PROCESSING)
print("DONE      :", queue_file.DONE)
print("FAILED    :", queue_file.FAILED)

proc = Path(queue_file.PROCESSING)
files = list(proc.glob("*.json"))
print("PROCESSING FILES:", [f.name for f in files])

for f in files:
    print("\n--- Try read:", f.name)
    try:
        txt = f.read_text(encoding="utf-8-sig")
        json.loads(txt)
        print("JSON READ OK with utf-8-sig")
    except Exception as e:
        print("JSON READ FAIL:", repr(e))

    try:
        from queue_file import mark_done
        mark_done(f, {"postId": "DIAG-OK"})
        print("mark_done OK -> moved to DONE")
    except Exception as e:
        print("mark_done FAIL:", repr(e))
