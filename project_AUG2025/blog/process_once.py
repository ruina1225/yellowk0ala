from queue_file import dequeue, mark_done
item, p = dequeue()
print("DEQ:", bool(item), p)
if item and p:
    mark_done(p, {"postId": "OK"})
    print("MOVED -> DONE")
