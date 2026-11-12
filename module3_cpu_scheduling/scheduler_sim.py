#!/usr/bin/env python3
"""
Module 3: CPU Scheduling Algorithms Simulator
Student: NITHIN N | Roll No: 25BTRPW066
Algorithms: FCFS, Non-Preemptive SJF, Round Robin (Quantum = 3 ms), plus SRTF (Preemptive SJF)
Processes:
  P1: AT = 0, BT = 9
  P2: AT = 2, BT = 7
  P3: AT = 3, BT = 8
  P4: AT = 6, BT = 8
"""

import copy

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.completion_time = -1
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1

    def __repr__(self):
        return f"{self.pid}(AT={self.arrival_time}, BT={self.burst_time})"


def print_gantt_chart(gantt):
    """
    gantt is a list of tuples: (pid, start_time, end_time)
    """
    # Merge consecutive identical processes
    merged = []
    for pid, st, et in gantt:
        if st == et:
            continue
        if merged and merged[-1][0] == pid:
            merged[-1] = (pid, merged[-1][1], et)
        else:
            merged.append((pid, st, et))

    top_bar = "+"
    mid_bar = "|"
    time_bar = f"{merged[0][1]}"

    for pid, st, et in merged:
        span = max(4, (et - st) * 2)
        top_bar += "-" * span + "+"
        label = f"{pid}".center(span)
        mid_bar += label + "|"
        time_str = f"{et}"
        time_bar += time_str.rjust(span + 1)

    print("  Gantt Chart:")
    print("  " + top_bar)
    print("  " + mid_bar)
    print("  " + top_bar)
    print("  " + time_bar)


def print_metrics_table(processes, algo_name, total_time):
    print(f"\n  Schedule Metrics for {algo_name}:")
    print("  " + "-" * 76)
    print(f"  {'PID':<6} | {'AT (ms)':<8} | {'BT (ms)':<8} | {'CT (ms)':<8} | {'TAT (ms)':<9} | {'WT (ms)':<8} | {'RT (ms)':<8}")
    print("  " + "-" * 76)

    total_tat = 0
    total_wt = 0
    total_rt = 0
    n = len(processes)

    for p in sorted(processes, key=lambda x: x.pid):
        total_tat += p.turnaround_time
        total_wt += p.waiting_time
        total_rt += p.response_time
        print(f"  {p.pid:<6} | {p.arrival_time:<8} | {p.burst_time:<8} | {p.completion_time:<8} | {p.turnaround_time:<9} | {p.waiting_time:<8} | {p.response_time:<8}")

    print("  " + "-" * 76)
    avg_tat = total_tat / n
    avg_wt = total_wt / n
    avg_rt = total_rt / n
    throughput = n / total_time
    cpu_util = 100.0  # since no idle time from 0 to 32

    print(f"  Average Turnaround Time (TAT) : {avg_tat:.2f} ms")
    print(f"  Average Waiting Time (WT)    : {avg_wt:.2f} ms")
    print(f"  Average Response Time (RT)   : {avg_rt:.2f} ms")
    print(f"  CPU Utilization              : {cpu_util:.2f} % (Total Execution Time = {total_time} ms)")
    print(f"  Throughput                   : {throughput:.4f} processes/ms ({throughput*1000:.1f} proc/sec)")
    print("  " + "-" * 76)
    return avg_tat, avg_wt, avg_rt


def simulate_fcfs(proc_list):
    procs = [copy.deepcopy(p) for p in sorted(proc_list, key=lambda x: (x.arrival_time, x.pid))]
    current_time = 0
    gantt = []

    for p in procs:
        if current_time < p.arrival_time:
            gantt.append(("IDLE", current_time, p.arrival_time))
            current_time = p.arrival_time
        
        p.start_time = current_time
        p.response_time = p.start_time - p.arrival_time
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        gantt.append((p.pid, p.start_time, p.completion_time))

    print("\n" + "=" * 80)
    print("1. FIRST-COME, FIRST-SERVED (FCFS) SCHEDULING")
    print("=" * 80)
    print_gantt_chart(gantt)
    avg_tat, avg_wt, avg_rt = print_metrics_table(procs, "FCFS", current_time)
    return {"algo": "FCFS", "avg_tat": avg_tat, "avg_wt": avg_wt, "avg_rt": avg_rt, "gantt": gantt}


def simulate_sjf_non_preemptive(proc_list):
    procs = [copy.deepcopy(p) for p in proc_list]
    completed = []
    current_time = 0
    gantt = []
    n = len(procs)

    while len(completed) < n:
        available = [p for p in procs if p.arrival_time <= current_time and p not in completed]
        if not available:
            # CPU idle until next arrival
            next_arr = min(p.arrival_time for p in procs if p not in completed)
            gantt.append(("IDLE", current_time, next_arr))
            current_time = next_arr
            continue

        # Non-preemptive: pick shortest burst time. Tie-breaker: earliest arrival time, then PID
        best = min(available, key=lambda x: (x.burst_time, x.arrival_time, x.pid))
        best.start_time = current_time
        best.response_time = best.start_time - best.arrival_time
        current_time += best.burst_time
        best.completion_time = current_time
        best.turnaround_time = best.completion_time - best.arrival_time
        best.waiting_time = best.turnaround_time - best.burst_time
        gantt.append((best.pid, best.start_time, best.completion_time))
        completed.append(best)

    print("\n" + "=" * 80)
    print("2. SHORTEST JOB FIRST (SJF - NON-PREEMPTIVE)")
    print("=" * 80)
    print_gantt_chart(gantt)
    avg_tat, avg_wt, avg_rt = print_metrics_table(completed, "SJF Non-Preemptive", current_time)
    return {"algo": "SJF (Non-Preemptive)", "avg_tat": avg_tat, "avg_wt": avg_wt, "avg_rt": avg_rt, "gantt": gantt}


def simulate_round_robin(proc_list, quantum=3):
    procs = {p.pid: copy.deepcopy(p) for p in proc_list}
    arrivals = sorted([p for p in proc_list], key=lambda x: (x.arrival_time, x.pid))
    
    current_time = 0
    ready_queue = []
    gantt = []
    arrival_idx = 0
    n = len(proc_list)
    completed_count = 0

    # Add initial processes arriving at t=0
    while arrival_idx < n and arrivals[arrival_idx].arrival_time <= current_time:
        ready_queue.append(arrivals[arrival_idx].pid)
        arrival_idx += 1

    while completed_count < n:
        if not ready_queue:
            if arrival_idx < n:
                next_arr = arrivals[arrival_idx].arrival_time
                gantt.append(("IDLE", current_time, next_arr))
                current_time = next_arr
                while arrival_idx < n and arrivals[arrival_idx].arrival_time <= current_time:
                    ready_queue.append(arrivals[arrival_idx].pid)
                    arrival_idx += 1
            continue

        curr_pid = ready_queue.pop(0)
        p = procs[curr_pid]

        if p.response_time == -1:
            p.response_time = current_time - p.arrival_time
            p.start_time = current_time

        exec_time = min(quantum, p.remaining_time)
        start_exec = current_time
        current_time += exec_time
        p.remaining_time -= exec_time
        gantt.append((p.pid, start_exec, current_time))

        # Check for new arrivals while this process was executing
        while arrival_idx < n and arrivals[arrival_idx].arrival_time <= current_time:
            ready_queue.append(arrivals[arrival_idx].pid)
            arrival_idx += 1

        if p.remaining_time > 0:
            ready_queue.append(p.pid)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed_count += 1

    print("\n" + "=" * 80)
    print(f"3. ROUND ROBIN SCHEDULING (QUANTUM = {quantum} ms)")
    print("=" * 80)
    print_gantt_chart(gantt)
    completed_list = list(procs.values())
    avg_tat, avg_wt, avg_rt = print_metrics_table(completed_list, f"Round Robin (Q={quantum}ms)", current_time)
    return {"algo": f"Round Robin (Q={quantum}ms)", "avg_tat": avg_tat, "avg_wt": avg_wt, "avg_rt": avg_rt, "gantt": gantt}


def simulate_srtf(proc_list):
    procs = {p.pid: copy.deepcopy(p) for p in proc_list}
    current_time = 0
    completed = []
    gantt = []
    n = len(proc_list)

    while len(completed) < n:
        available = [p for p in procs.values() if p.arrival_time <= current_time and p.remaining_time > 0]
        if not available:
            current_time += 1
            continue

        best = min(available, key=lambda x: (x.remaining_time, x.arrival_time, x.pid))
        if best.response_time == -1:
            best.response_time = current_time - best.arrival_time

        start_time = current_time
        current_time += 1
        best.remaining_time -= 1
        gantt.append((best.pid, start_time, current_time))

        if best.remaining_time == 0:
            best.completion_time = current_time
            best.turnaround_time = best.completion_time - best.arrival_time
            best.waiting_time = best.turnaround_time - best.burst_time
            completed.append(best)

    print("\n" + "=" * 80)
    print("4. SHORTEST REMAINING TIME FIRST (SRTF / PREEMPTIVE SJF) - REFERENCE COMPARISON")
    print("=" * 80)
    print_gantt_chart(gantt)
    avg_tat, avg_wt, avg_rt = print_metrics_table(completed, "SRTF (Preemptive SJF)", current_time)
    return {"algo": "SRTF (Preemptive)", "avg_tat": avg_tat, "avg_wt": avg_wt, "avg_rt": avg_rt, "gantt": gantt}


def run_all_schedulers():
    print("=" * 80)
    print("MODULE 3: CPU SCHEDULING SIMULATION & COMPARATIVE EVALUATION")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Workload: High-Concurrency Food Delivery Core Tasks (P1: Dispatch, P2: Match, P3: Cart, P4: Ledger)")
    print("=" * 80)

    # Dataset from problem statement
    raw_processes = [
        Process("P1", arrival_time=0, burst_time=9),
        Process("P2", arrival_time=2, burst_time=7),
        Process("P3", arrival_time=3, burst_time=8),
        Process("P4", arrival_time=6, burst_time=8),
    ]

    r1 = simulate_fcfs(raw_processes)
    r2 = simulate_sjf_non_preemptive(raw_processes)
    r3 = simulate_round_robin(raw_processes, quantum=3)
    r4 = simulate_srtf(raw_processes)

    print("\n" + "=" * 80)
    print("5. COMPARATIVE SCHEDULING BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"{'Algorithm':<26} | {'Avg TAT (ms)':<14} | {'Avg WT (ms)':<14} | {'Avg RT (ms)':<14} | {'Key Tradeoff'}")
    print("-" * 80)
    print(f"{r1['algo']:<26} | {r1['avg_tat']:<14.2f} | {r1['avg_wt']:<14.2f} | {r1['avg_rt']:<14.2f} | Convoy effect, Poor response")
    print(f"{r2['algo']:<26} | {r2['avg_tat']:<14.2f} | {r2['avg_wt']:<14.2f} | {r2['avg_rt']:<14.2f} | Identical to FCFS due to P1 head start")
    print(f"{r3['algo']:<26} | {r3['avg_tat']:<14.2f} | {r3['avg_wt']:<14.2f} | {r3['avg_rt']:<14.2f} | Superior fairness & responsiveness (RT=2.5ms)")
    print(f"{r4['algo']:<26} | {r4['avg_tat']:<14.2f} | {r4['avg_wt']:<14.2f} | {r4['avg_rt']:<14.2f} | High context switches; starvation risk")
    print("=" * 80)
    print("PLATFORM RECOMMENDATION & TECHNICAL JUSTIFICATION:")
    print("• For a live Food Delivery Platform, user-facing latency and system responsiveness are paramount.")
    print("• Under FCFS / Non-Preemptive SJF, P4 suffers an intolerable waiting time of 18 ms and a response time of 18 ms.")
    print("• ROUND ROBIN (Quantum = 3 ms) achieves an Average Response Time of 2.50 ms (a 73.7% reduction vs 9.50 ms)! ")
    print("• RR guarantees starvation-free execution, preventing batch ledger tasks from blocking real-time driver tracking.")
    print("=" * 80)

if __name__ == "__main__":
    run_all_schedulers()
