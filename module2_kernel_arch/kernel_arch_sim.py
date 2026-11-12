#!/usr/bin/env python3
"""
Module 2: Monolithic vs. Microkernel Architecture Simulation (fork-exec-wait)
Student: NITHIN N | Roll No: 25BTRPW066
Food Delivery Platform Scenario: Spawning high-throughput order dispatch workers
"""

import time

def compare_architectures():
    print("=" * 85)
    print("MODULE 2: MONOLITHIC VS. MICROKERNEL ARCHITECTURE (FORK-EXEC-WAIT EVALUATION)")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Platform Scenario: Spawning Order Processing & Driver Dispatch Workers")
    print("=" * 85)

    # Architectural Step-by-Step Breakdown
    print("\n[A] SYSTEM CALL TRACE: FORK-EXEC-WAIT SEQUENCE BREAKDOWN")
    print("-" * 85)
    print("1. MONOLITHIC KERNEL (e.g., Linux / Unix):")
    print("   • fork() [sys_clone]:")
    print("     - Step 1: User process invokes 'syscall' / 'int 0x80' (Ring 3 -> Ring 0).")
    print("     - Step 2: In-kernel Process Manager duplicates parent PCB (task_struct).")
    print("     - Step 3: Sets up Copy-on-Write (COW) page table entries directly in kernel space.")
    print("     - Step 4: Allocates PID, attaches to scheduler runqueue, returns child PID (Ring 0 -> Ring 3).")
    print("     - Context switches: 0 address-space switches, 2 privilege level transitions.")
    print("   • exec() [sys_execve]:")
    print("     - Step 1: User process traps into kernel (Ring 3 -> Ring 0).")
    print("     - Step 2: VFS (in-kernel) reads ELF binary directly from disk/page cache.")
    print("     - Step 3: Memory management subsystem releases old address space & maps ELF segments.")
    print("     - Step 4: Resets registers and jumps to new entry point (Ring 0 -> Ring 3).")
    print("     - Context switches: 1 address-space flush, 2 privilege level transitions.")
    print("   • wait() [sys_wait4]:")
    print("     - Step 1: Parent traps into kernel (Ring 3 -> Ring 0).")
    print("     - Step 2: Kernel puts parent onto wait queue; scheduler yields CPU.")
    print("     - Step 3: On child exit, in-kernel exit handler sets state to TASK_ZOMBIE, sends SIGCHLD.")
    print("     - Step 4: Parent reaped, exit status returned directly (Ring 0 -> Ring 3).")
    print("-" * 85)
    print("2. MICROKERNEL ARCHITECTURE (e.g., seL4, Minix, QNX, Mach):")
    print("   • fork():")
    print("     - Step 1: Client library marshals request into IPC message.")
    print("     - Step 2: IPC trap to microkernel (Ring 3 -> Ring 0).")
    print("     - Step 3: Kernel context-switches to user-space Process Server (Ring 0 -> Ring 3).")
    print("     - Step 4: Process Server sends IPC request to Memory Server (Ring 3 -> Ring 0 -> Ring 3).")
    print("     - Step 5: Memory Server allocates address space, sends IPC response back to Process Server.")
    print("     - Step 6: Process Server registers thread with Microkernel scheduler.")
    print("     - Step 7: Process Server sends IPC response back to client (Ring 3 -> Ring 0 -> Ring 3).")
    print("     - Context switches: 4+ full address space switches, 8+ privilege transitions!")
    print("   • exec():")
    print("     - Step 1: Client sends IPC to VFS Server (User space).")
    print("     - Step 2: VFS Server sends IPC to Disk Driver Server (User space) to read ELF.")
    print("     - Step 3: VFS Server sends IPC to Memory Server to map binary pages.")
    print("     - Step 4: Memory Server maps frames and replies to Process Server.")
    print("     - Step 5: Process Server resets thread register state and signals execution start.")
    print("     - Context switches: 6+ address space switches, 12+ privilege transitions!")
    print("   • wait():")
    print("     - Step 1: Parent sends IPC to Process Server and blocks on message receive.")
    print("     - Step 2: When child exits, it sends IPC to Process Server.")
    print("     - Step 3: Process Server wakes parent via IPC notification message.")
    print("     - Context switches: 3+ address space switches, 6+ privilege transitions.")
    
    # Quantitative Benchmarking Model
    mono_privilege_switches = 6
    mono_addr_switches = 1
    mono_ipc_messages = 0
    mono_avg_latency_us = 45.0  # typical Linux fork+exec+wait with COW

    micro_privilege_switches = 26
    micro_addr_switches = 13
    micro_ipc_messages = 10
    micro_avg_latency_us = 265.0  # typical microkernel IPC marshalling + TLB flushes

    print("\n[B] QUANTITATIVE ARCHITECTURAL COMPARISON (PER FORK-EXEC-WAIT CYCLE)")
    print("-" * 85)
    print(f"{'Performance Metric':<32} | {'Monolithic (Linux)':<22} | {'Microkernel (seL4/QNX)':<22}")
    print("-" * 85)
    print(f"{'Privilege Level Crossings':<32} | {mono_privilege_switches:<22} | {micro_privilege_switches:<22}")
    print(f"{'Address Space Switches (TLB)':<32} | {mono_addr_switches:<22} | {micro_addr_switches:<22}")
    print(f"{'IPC Messages / Copies':<32} | {mono_ipc_messages:<22} | {micro_ipc_messages:<22}")
    print(f"{'Average Cycle Latency (µs)':<32} | {mono_avg_latency_us:<22.1f} | {micro_avg_latency_us:<22.1f}")
    print(f"{'Throughput (spawns/sec)':<32} | {1e6/mono_avg_latency_us:<22,.0f} | {1e6/micro_avg_latency_us:<22,.0f}")
    print(f"{'Fault Isolation':<32} | {'Fault in driver crashes OS':<22} | {'Fault isolated to server':<22}")
    print(f"{'Kernel Codebase Size (LoC)':<32} | {'~30,000,000 LoC (Extensive)':<22} | {'~10,000 LoC (Verifiable)':<22}")
    print("-" * 85)

    print("\n[C] ARCHITECTURAL JUSTIFICATION FOR FOOD DELIVERY PLATFORM:")
    print("1. High-Throughput Cloud Backend (Orders, Dispatch, Dynamic Pricing):")
    print("   -> OPTIMAL CHOICE: MONOLITHIC KERNEL (Linux with Cgroups & Namespaces).")
    print("   -> Justification: High order concurrency demands minimal latency (<50 µs process spawns),")
    print("      zero-copy IPC via memory mapping, and direct VFS page caching. Microkernel IPC overhead")
    print("      imposes a 5.8x latency penalty per worker lifecycle.")
    print("2. Edge / Autonomous Delivery Hardware (Drones, Self-Driving Delivery Bots):")
    print("   -> OPTIMAL CHOICE: MICROKERNEL (e.g., QNX or seL4).")
    print("   -> Justification: Crash resilience is non-negotiable. If a LiDAR or sensor driver fails,")
    print("      it can be restarted in user-space without crashing flight/motor stabilization systems.")
    print("=" * 85)

if __name__ == "__main__":
    compare_architectures()
