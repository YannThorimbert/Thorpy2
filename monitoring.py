import time
class Monitor:

    def __init__(self):
        self.last_start = {}
        self.n_called = {}
        self.tot_time = {}
        self.ended_ok = {}

    def main_loop(self):
        k = "_main_loop_"
        if k in self.last_start:
            self.tot_time[k] += time.perf_counter() - self.last_start[k]
            self.n_called[k] += 1
        else: #start of first loop
            self.n_called[k] = 0
            self.tot_time[k] = 0.
        self.last_start[k] = time.perf_counter()

    def start(self, symb):
        if not symb in self.tot_time:
            self.n_called[symb] = 0
            self.tot_time[symb] = 0.
        ok = self.ended_ok.get(symb, None)
        assert ok != False #ok must be either None (not set so far) or True
        self.ended_ok[symb] = False #for current iter
        self.last_start[symb] = time.perf_counter()

    def end(self, symb):
        assert symb in self.ended_ok
        assert self.ended_ok[symb] is False
        self.ended_ok[symb] = True
        self.tot_time[symb] += time.perf_counter() - self.last_start[symb]
        self.n_called[symb] += 1

    def show(self, reference_symb="_main_loop_"):
        fps = round(self.n_called.get(reference_symb) / self.tot_time.get(reference_symb))
        print("========== Monitoring statistics relative to", reference_symb, " : avg FPS =", fps, " ==========")
        L = max([len(symb) for symb in self.tot_time])
        print(f"{'markers (n times)':<{L+10}} {'| time':<{10}} {'| percentage':<{10}}")
        print("#"*(L+30))
        tot_time = self.tot_time[reference_symb]
        for symb in self.tot_time:
            t = self.tot_time[symb]
            col_a = " ".join([str(s) for s in [symb, "(", self.n_called[symb], "X)"]])
            col_b = " ".join([str(s) for s in ["|", round(t,2), "s"] ])
            col_c = " ".join([str(s) for s in ["|", round(t/tot_time * 100,1), "%"]])
            print(f"{col_a:<{L+10}} {col_b:<{10}} {col_c:<{10}}")
        print("***")
        print(list(self.tot_time.keys()))
        print()

    def reset(self):
        self.last_start.clear()
        self.n_called.clear()
        self.tot_time.clear()
        self.ended_ok.clear()

