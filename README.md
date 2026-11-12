# Operating Systems Experimental Lab: High-Concurrency Food Delivery Platform

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FNITHIN-aiml69%2FOS-FOOD-DELIVERY-)

**Student Name:** NITHIN N  
**Roll Number:** `25BTRPW066`  
**GitHub Repository:** [https://github.com/NITHIN-aiml69/OS-FOOD-DELIVERY-](https://github.com/NITHIN-aiml69/OS-FOOD-DELIVERY-)  
**Platform Architecture:** Distributed Cloud & Edge Food Delivery Platform (Order Ingestion, Matching, Telemetry, and Accounting)  
**Execution Environment:** macOS / Linux (POSIX-compliant, Python 3.13, Clang/GCC)

---

## 📌 Executive Summary & Architecture Overview

This repository provides an enterprise-grade, programmatic implementation of 10 foundational Operating System subsystems designed specifically for a real-time, high-concurrency **Food Delivery Platform**. The platform processes dynamic order bursts, real-time rider GPS tracking streams, restaurant kitchen queues, and high-frequency financial ledgers.

The project implements mathematical models, POSIX multithreaded and process primitives, scheduling simulators, memory allocation allocators, page-replacement algorithms, disk seek optimizers, file system caching simulators, Linux performance telemetry diagnostics, and container-vs-VM evaluation engines.

---

## 📂 Repository Directory Layout

```
.
├── README.md                              # Complete Lab documentation & execution guide
├── run_all_experiments.py                 # Master test runner executing all 10 modules
├── module1_io_dma/                        # Module 1: Interrupt-Driven I/O vs. DMA
│   ├── dma_interrupt_sim.py               # Analytical calculation & CPU utilization model
│   ├── dma_trace.c                        # C memory burst transfer benchmark
│   └── dma_trace                          # Compiled C binary
├── module2_kernel_arch/                   # Module 2: Monolithic vs. Microkernel (Fork-Exec-Wait)
│   ├── kernel_arch_sim.py                 # Quantitative IPC & privilege crossing simulator
│   ├── fork_exec_monolithic.c             # Concrete POSIX fork-exec-wait implementation
│   └── fork_exec_monolithic               # Compiled POSIX C binary
├── module3_cpu_scheduling/                # Module 3: CPU Scheduling (FCFS, SJF, RR Q=3, SRTF)
│   └── scheduler_sim.py                   # Gantt chart renderer & TAT/WT/RT metrics engine
├── module4_concurrency_deadlock/          # Module 4: Concurrency, Deadlocks & Banker's Algorithm
│   ├── deadlock_bankers.py                # Banker's safety state & deadlock simulator
│   ├── sync_posix.c                       # Multithreaded C implementation (Mutex + Semaphores)
│   └── sync_posix                         # Compiled POSIX C binary
├── module5_memory_allocation/             # Module 5: Dynamic Memory Allocation (First/Best/Worst)
│   └── memory_alloc_sim.py                # Allocation maps, remaining holes & fragmentation metrics
├── module6_virtual_memory/                # Module 6: Virtual Memory & Page Replacement
│   └── page_replacement_sim.py           # FIFO, LRU, Optimal page trace & Thrashing mitigation engine
├── module7_disk_scheduling/               # Module 7: Disk Cylinder Head Scheduling
│   └── disk_scheduler_sim.py              # FCFS, SSTF, SCAN, C-SCAN, and LOOK seek simulator
├── module8_filesystem_caching/            # Module 8: File System Allocation, Caching & Crash Recovery
│   └── filesystem_sim.py                  # Inode extents, Write-Back Page Cache & WAL recovery model
├── module9_linux_perf_telemetry/          # Module 9: Linux Performance Telemetry & Bottleneck Fix
│   └── bottleneck_analyzer.py             # Mock /proc parser, 49% I/O wait root cause & remediation
└── module10_container_vs_vm/              # Module 10: Containerization vs. Virtual Machines
    └── deployment_evaluator.py            # Multi-criteria scoring, IPC matrix & rollback triggers
```

---

## 🚀 Deployment (Local, Docker, Kubernetes & Vercel)

### 1. Cloud Deployment via Vercel:
The project includes serverless WSGI configuration ([`api/index.py`](file:///Users/nithinn/Downloads/OS%20EXP%20LEARNING/api/index.py), [`vercel.json`](file:///Users/nithinn/Downloads/OS%20EXP%20LEARNING/vercel.json), and [`requirements.txt`](file:///Users/nithinn/Downloads/OS%20EXP%20LEARNING/requirements.txt)).
- **Via GitHub:** Push this repo to GitHub, open [Vercel](https://vercel.com/new), click **Import**, and click **Deploy**.
- **Via Vercel CLI:** Run `./deploy_cloud.sh` or `npx vercel --prod`.

### 2. Live Local Dashboard:
```bash
python3 platform_server.py
```
Visit: [http://localhost:8080](http://localhost:8080)

### 3. Docker & Kubernetes:
```bash
# Docker Compose
docker-compose up --build

# Kubernetes
kubectl apply -f k8s/
```

---

## 🚀 Quick Start: Running Experiments

### Run All Modules Concurrently (Automated Suite):
```bash
python3 run_all_experiments.py
```

### Run Individual Modules:
- **Module 1 (I/O & DMA):**
  ```bash
  python3 module1_io_dma/dma_interrupt_sim.py
  ./module1_io_dma/dma_trace
  ```
- **Module 2 (Kernel Architecture):**
  ```bash
  python3 module2_kernel_arch/kernel_arch_sim.py
  ./module2_kernel_arch/fork_exec_monolithic
  ```
- **Module 3 (CPU Scheduling):**
  ```bash
  python3 module3_cpu_scheduling/scheduler_sim.py
  ```
- **Module 4 (Synchronization & Deadlocks):**
  ```bash
  python3 module4_concurrency_deadlock/deadlock_bankers.py
  ./module4_concurrency_deadlock/sync_posix
  ```
- **Module 5 (Memory Allocation):**
  ```bash
  python3 module5_memory_allocation/memory_alloc_sim.py
  ```
- **Module 6 (Page Replacement):**
  ```bash
  python3 module6_virtual_memory/page_replacement_sim.py
  ```
- **Module 7 (Disk Scheduling):**
  ```bash
  python3 module7_disk_scheduling/disk_scheduler_sim.py
  ```
- **Module 8 (File System & Caching):**
  ```bash
  python3 module8_filesystem_caching/filesystem_sim.py
  ```
- **Module 9 (Performance Monitoring & Bottleneck):**
  ```bash
  python3 module9_linux_perf_telemetry/bottleneck_analyzer.py
  ```
- **Module 10 (Containers vs. VMs):**
  ```bash
  python3 module10_container_vs_vm/deployment_evaluator.py
  ```

---

## 📊 Summary of Experimental Results & Key Takeaways

| Module | Core Parameters | Selected Solution | Key Numerical Result / SLA |
|---|---|---|---|
| **1. I/O vs. DMA** | 47 MB transfer @ 20 IRQ/s over 5s | Direct Memory Access (DMA) | 100 IRQs (buffered) vs 1 IRQ (DMA). Eliminates CPU load by >99%. |
| **2. Kernel Architecture** | Fork-Exec-Wait process lifecycles | Monolithic Kernel (Linux) | Latency: 45 µs (Monolithic) vs 265 µs (Microkernel). 5.8x faster spawn rate. |
| **3. CPU Scheduling** | P1–P4 bursts [9, 7, 8, 8] ms, arrivals [0, 2, 3, 6] ms | Round Robin (Q=3 ms) | Avg RT = 2.50 ms (vs 9.50 ms in FCFS/SJF). Prevents worker starvation. |
| **4. Synchronization** | 3 Workers, 3 DB Tokens, 1 Audit Log Mutex | Strict Resource Ordering & Banker's | Zero deadlocks, zero race conditions ($Total = 9$ verified cycles). |
| **5. Memory Allocation** | Blocks [113, 219, 325, 501, 737] KB, Requests [96, 192, 288, 404] KB | First-Fit Allocation | Preserves 737 KB block intact; passes 600 KB burst test (Worst-Fit fails). |
| **6. Page Replacement** | 4 Frames, Ref String [4, 5, 6, 7, 4, 5, 1, 4, 5, 6, 7, 1] | LRU / Clock Algorithm (2Q) | OPT = 6 faults (50% hits), LRU = 8 faults (33.3% hits), FIFO = 10 faults. |
| **7. Disk Scheduling** | Cylinders [32, 68, 104, 140, 174, 52, 120, 192], Head=142 (down) | SSTF / LOOK (mq-deadline for SSD) | SSTF & LOOK: 270 cylinders; SCAN: 334 cylinders; C-SCAN: 366 cylinders. |
| **8. File System** | 1,481 ops/min (41% Reads, 59% Updates) | Ext4 Extents + Page Cache + WAL | Write latency drops from 12 ms to 15 µs; crash recovery < 1.5 seconds. |
| **9. Telemetry & Fix** | CPU=76%, Mem=58%, I/O Wait=49%, Latency=44ms | Redis + Asynchronous I/O (`io_uring`) | I/O wait slashed from 49.0% to 2.1%; P99 latency slashed from 44 ms to 3.8 ms. |
| **10. Containers vs VMs** | 349 Concurrent Users across Microservices | Container Pods (Kubernetes) | Composite score: 9.15/10 (Container) vs 5.20/10 (VM). Auto-rollback < 12s. |

---
**Author:** NITHIN N (Roll: `25BTRPW066`)  
**Operating Systems Laboratory Examination & Experimental Benchmark**
