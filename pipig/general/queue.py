from Queue import Queue, Empty
from threading import Thread, Event

num_fetch_threads = 2
queue = Queue()
quit_event = Event()

def do_work(item):
    print str(item)

def worker(queue):
    while True:
        try:
            item = queue.get()
        except Empty:
            continue

        do_work(item)
        queue.task_done()

for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for i in range(100):
    queue.put(i)

print "Main Thread Waiting"
quit_event.set()
queue.join()
print "Done"

