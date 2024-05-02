import time
import typing
import threading


tracing = False


class PerformanceCounter(object):
    def __init__(self, name: str, parent: typing.Optional['PerformanceCounter'] = None) -> None:
        self.name = name
        self.counter = 0
        self.thread_counter = 0
        self.time = 0
        self.children: typing.Dict[str, PerformanceCounter] = {}
        self.lock = threading.Lock()
        self.parent: typing.Optional[PerformanceCounter] = parent
        self.thread_info = threading.local()

    def get_child(self, name: str) -> "PerformanceCounter":
        with self.lock:
            if name not in self.children:
                self.children[name] = PerformanceCounter(name=name, parent=self)
        child = self.children[name]
        return child

    def update(self, proc_time: float):
        if hasattr(self.thread_info, "counted"):
            must_count = 0
        else:
            must_count = 1
            self.thread_info.counted = True
        with self.lock:
            self.thread_counter += must_count
            self.time += proc_time
            self.counter += 1


thread_perf = {}
perf_root = PerformanceCounter("root")


def get_current_perf() -> PerformanceCounter:
    global thread_perf
    thread_name = threading.current_thread().name
    if thread_name not in thread_perf:
        thread_perf[thread_name] = perf_root
    return thread_perf[thread_name]


def set_current_perf(counter: PerformanceCounter):
    global thread_perf
    thread_name = threading.current_thread().name
    thread_perf[thread_name] = counter


class TracingCodeBlock(object):
    def __init__(self, name: str):
        if not tracing:
            return
        global thread_perf
        self.parent = get_current_perf()
        self.perf_counter = self.parent.get_child(name=name)
        set_current_perf(self.perf_counter)
        self.start = None

    def __del__(self):
        pass

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not tracing:
            return
        global thread_perf
        self.perf_counter.update(proc_time=time.time() - self.start)
        set_current_perf(self.parent)


class PerformanceReport(object):
    def __init__(self):
        self.start = time.time()

    def show_counter(self, counter: PerformanceCounter, indentation: int = 0):
        formatted_name = format("".join(['--' for i in range(indentation)]) + counter.name, "<50")
        formatted_thread = format(counter.thread_counter, ">10")
        formatted_counter = format(counter.counter, ">10")
        formatted_time = format(counter.time, ">15.3f")
        print(formatted_name+formatted_thread+formatted_counter+formatted_time)
        for child in counter.children.values():
            self.show_counter(counter=child, indentation=indentation + 1)

    def __del__(self):
        if not tracing:
            return
        formatted_name = format("COUNTER", "<50")
        formatted_thread = format("THREADS", ">10")
        formatted_counter = format("CALLS", ">10")
        formatted_time = format("TIME", ">15")
        print(formatted_name+formatted_thread+formatted_counter+formatted_time)
        perf_root.update(proc_time=time.time() - self.start)
        self.show_counter(perf_root)

class NotTracingCodeBlock(object):
    def __init__(self, name: str):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


CodeBlock = TracingCodeBlock
perf_report = PerformanceReport()


def start_profile():
    global tracing
    tracing = True
