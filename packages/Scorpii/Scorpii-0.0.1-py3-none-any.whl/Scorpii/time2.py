import time, threading

def wait(timeToWait):
    timeStart = time.time()

    while (time.time() - timeStart) < timeToWait:
        continue

    return

def stopwatch_start(id=1):
    int(id)
    globals()[str(id)] = time.time()

def stopwatch_stop(id=1):
    int(id)
    return time.time() - globals()[str(id)]

def timer(time,func):
    def timer_thread():
        wait(time)
        func()
    
    t = threading.Thread(target=timer_thread)
    t.start()
