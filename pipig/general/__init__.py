from Queue import Queue
from threading import Thread
from time import sleep

def do_stuff(q):
  while True:
    print q.get()
    sleep(0.1)
    q.task_done()


if __name__ == '__main__':
  q = Queue(maxsize=0)
  num_threads = 3

  for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,))
    worker.setDaemon(True)
    worker.start()

  for y in range (10):
    for x in range(100):
      q.put(x + y * 100)
    q.join()
    print "Batch " + str(y) + " Done"