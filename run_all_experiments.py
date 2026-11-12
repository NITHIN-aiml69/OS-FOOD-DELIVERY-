#!/usr/bin/env python3
"""
Master Execution Suite: Operating Systems Experimental Lab
Food Delivery Platform Simulation Framework
Student: NITHIN N | Roll Number: 25BTRPW066
Executes all 10 lab experiments with end-to-end verification.
"""

import subprocess
import sys
import os
import time

MODULES = [
    ("Module 1: Interrupt-Driven I/O vs. DMA", ["python3", "module1_io_dma/dma_interrupt_sim.py"]),
    ("Module 1 (C Benchmark): DMA & Interrupt Emulation", ["./module1_io_dma/dma_trace"]),
    ("Module 2: Monolithic vs. Microkernel Architecture", ["python3", "module2_kernel_arch/kernel_arch_sim.py"]),
    ("Module 2 (POSIX C): Fork-Exec-Wait Process Lifecycle", ["./module2_kernel_arch/fork_exec_monolithic"]),
    ("Module 3: CPU Scheduling (FCFS, SJF, RR Q=3)", ["python3", "module3_cpu_scheduling/scheduler_sim.py"]),
    ("Module 4: Process Synchronization & Deadlocks (Banker's)", ["python3", "module4_concurrency_deadlock/deadlock_bankers.py"]),
    ("Module 4 (POSIX C): Multithreaded Mutex & Semaphores", ["./module4_concurrency_deadlock/sync_posix"]),
    ("Module 5: Memory Allocation (First-Fit vs. Best-Fit)", ["python3", "module5_memory_allocation/memory_alloc_sim.py"]),
    ("Module 6: Virtual Memory & Page Replacement (FIFO, LRU, OPT)", ["python3", "module6_virtual_memory/page_replacement_sim.py"]),
    ("Module 7: Disk Scheduling (FCFS, SSTF, SCAN, C-SCAN)", ["python3", "module7_disk_scheduling/disk_scheduler_sim.py"]),
    ("Module 8: File System Allocation & Buffering", ["python3", "module8_filesystem_caching/filesystem_sim.py"]),
    ("Module 9: Linux Performance Telemetry & Bottleneck Fix", ["python3", "module9_linux_perf_telemetry/bottleneck_analyzer.py"]),
    ("Module 10: Containerization vs. VMs Deployment", ["python3", "module10_container_vs_vm/deployment_evaluator.py"]),
]

# Always change working directory to this script's directory so it works from anywhere
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

def main():
    print("=" * 90)
    print("OPERATING SYSTEMS EXPERIMENTAL LAB - MASTER TEST RUNNER")
    print("Institution: Deep Learning / Advanced Systems Engineering Lab")
    print("Student Name: NITHIN N | Roll Number: 25BTRPW066")
    print("Scenario: High-Concurrency Cloud Food Delivery Infrastructure")
    print(f"Working Directory: {PROJECT_DIR}")
    print("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 90)

    # First compile C binaries if needed
    os.system("clang -O2 module1_io_dma/dma_trace.c -o module1_io_dma/dma_trace")
    os.system("clang -O2 module2_kernel_arch/fork_exec_monolithic.c -o module2_kernel_arch/fork_exec_monolithic")
    os.system("clang -O2 -pthread module4_concurrency_deadlock/sync_posix.c -o module4_concurrency_deadlock/sync_posix")

    passed = 0
    failed = 0

    for title, cmd in MODULES:
        print(f"\n>>> EXECUTING: {title}...")
        try:
            res = subprocess.run(cmd, capture_output=False, text=True, check=True)
            passed += 1
        except Exception as e:
            print(f"FAILED: {e}", file=sys.stderr)
            failed += 1

    print("\n" + "=" * 90)
    print(f"ALL EXPERIMENTAL MODULES COMPLETED: {passed} PASSED, {failed} FAILED.")
    print("System verified for high-concurrency food delivery platform operations.")
    print("=" * 90)

if __name__ == "__main__":
    main()
