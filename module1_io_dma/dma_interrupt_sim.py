#!/usr/bin/env python3
"""
Module 1: Interrupt-Driven I/O vs. DMA Simulation
Student: NITHIN N | Roll No: 25BTRPW066
Food Delivery Platform Scenario: Bulk Order Media / Telemetry Dispatch Transfer
"""

import sys
import time

def calculate_io_metrics():
    # Problem prompt parameters
    transfer_size_mb = 47.0
    transfer_size_bytes = int(transfer_size_mb * 1024 * 1024)  # 49,283,072 bytes
    duration_sec = 5.0
    interrupt_rate = 20.0  # interrupts / sec

    # Prompt calculation
    expected_interrupts = int(interrupt_rate * duration_sec)
    bytes_per_interrupt = transfer_size_bytes / expected_interrupts
    kb_per_interrupt = bytes_per_interrupt / 1024.0
    mb_per_sec = transfer_size_mb / duration_sec

    # Traditional unbuffered character I/O comparison (1 byte per interrupt)
    unbuffered_interrupts = transfer_size_bytes
    isr_overhead_sec = 3.0e-6  # 3 microseconds context switch + ISR
    unbuffered_cpu_time = unbuffered_interrupts * isr_overhead_sec
    unbuffered_cpu_utilization = (unbuffered_cpu_time / duration_sec) * 100.0

    # DMA model
    dma_interrupts = 1  # 1 completion interrupt for entire buffer
    dma_setup_time_sec = 1.0e-6
    dma_isr_time_sec = 2.0e-6
    dma_cpu_time = dma_setup_time_sec + (dma_interrupts * dma_isr_time_sec)
    dma_cpu_utilization = (dma_cpu_time / duration_sec) * 100.0

    # Block-buffered I/O (prompt case)
    buffered_cpu_time = expected_interrupts * isr_overhead_sec
    buffered_cpu_utilization = (buffered_cpu_time / duration_sec) * 100.0

    print("=" * 80)
    print("MODULE 1: INTERRUPT-DRIVEN I/O VS. DMA PERFORMANCE EVALUATION")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Scenario: High-Concurrency Food Delivery Platform (Bulk Order Blob Dispatch)")
    print("=" * 80)
    print(f"Transfer Payload Size       : {transfer_size_mb:.2f} MB ({transfer_size_bytes:,} bytes)")
    print(f"Transfer Duration           : {duration_sec:.2f} seconds")
    print(f"Configured Interrupt Rate   : {interrupt_rate:.2f} interrupts/second")
    print(f"Overall Data Throughput     : {mb_per_sec:.2f} MB/second")
    print("-" * 80)
    print("1. PROMPT CALCULATION (BLOCK-BUFFERED INTERRUPT-DRIVEN I/O):")
    print(f"   Expected Total Interrupts = {interrupt_rate:.0f} interrupts/sec * {duration_sec:.0f} sec")
    print(f"                             = {expected_interrupts} interrupts")
    print(f"   Payload per Interrupt     = {kb_per_interrupt:.2f} KB ({bytes_per_interrupt:,.2f} bytes)")
    print(f"   Total CPU ISR Time spent  = {buffered_cpu_time * 1e3:.4f} ms")
    print(f"   CPU Core Utilization      = {buffered_cpu_utilization:.4f} %")
    print("-" * 80)
    print("2. COMPARATIVE ARCHITECTURAL SPECTRUM:")
    print(f"   a) Unbuffered Character I/O (1 byte/IRQ):")
    print(f"      - Total Interrupts     : {unbuffered_interrupts:,} interrupts")
    print(f"      - Total CPU Time       : {unbuffered_cpu_time:.2f} seconds")
    print(f"      - CPU Utilization      : {unbuffered_cpu_utilization:.2f} % (CRITICAL LIVELOCK)")
    print(f"   b) Block-Buffered I/O (Prompt Config - {expected_interrupts} IRQs):")
    print(f"      - Total Interrupts     : {expected_interrupts} interrupts")
    print(f"      - Total CPU Time       : {buffered_cpu_time * 1e3:.4f} ms")
    print(f"      - CPU Utilization      : {buffered_cpu_utilization:.4f} %")
    print(f"   c) Direct Memory Access (DMA Engine - Bus Mastering):")
    print(f"      - Total Interrupts     : {dma_interrupts} completion interrupt")
    print(f"      - Total CPU Time       : {dma_cpu_time * 1e6:.2f} microseconds")
    print(f"      - CPU Utilization      : {dma_cpu_utilization:.6f} % (OPTIMAL)")
    print("=" * 80)
    print("3. LINUX DIAGNOSTIC VERIFICATION METHODOLOGY:")
    print("   - Step 1: Trace IRQ distribution via:  watch -n 1 'cat /proc/interrupts'")
    print("   - Step 2: Sample context switches via: vmstat 1 (inspect 'in' and 'cs' columns)")
    print("   - Step 3: Kernel tracepoints via:      perf stat -e irq:irq_handler_entry -a sleep 5")
    print("   - Step 4: eBPF low-level latency:      bpftrace -e 'tracepoint:irq:irq_handler_entry { @[kstack] = count(); }'")
    print("=" * 80)

if __name__ == "__main__":
    calculate_io_metrics()
