#!/usr/bin/env python3
"""
Module 8: File System Allocation, Caching & Crash Recovery Simulator
Student: NITHIN N | Roll No: 25BTRPW066
Workload: 1,481 file ops/min (41% Reads = 607 ops/min, 59% Updates = 874 ops/min)
Scenario: Food Delivery Order Ledger & Telemetry File Service
"""

import math

def evaluate_file_system():
    total_ops_per_min = 1481
    total_ops_per_sec = total_ops_per_min / 60.0
    read_ratio = 0.41
    update_ratio = 0.59

    reads_per_min = total_ops_per_min * read_ratio
    updates_per_min = total_ops_per_min * update_ratio
    reads_per_sec = reads_per_min / 60.0
    updates_per_sec = updates_per_min / 60.0

    print("=" * 85)
    print("MODULE 8: FILE SYSTEM ALLOCATION, BUFFERING & CRASH RECOVERY EVALUATOR")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Platform Scenario: High-Throughput Food Delivery Ledger & Order State Service")
    print("=" * 85)
    print(f"Total Workload Throughput  : {total_ops_per_min} ops/min ({total_ops_per_sec:.2f} ops/sec)")
    print(f"Read Operations (41%)      : {reads_per_min:.1f} reads/min ({reads_per_sec:.2f} reads/sec)")
    print(f"Update/Write Ops (59%)     : {updates_per_min:.1f} updates/min ({updates_per_sec:.2f} updates/sec)")
    print("Workload Classification    : WRITE-DOMINANT DYNAMIC MUTATION PATTERN")
    print("-" * 85)

    print("\n[A] COMPARATIVE EVALUATION OF FILE ALLOCATION METHODS")
    print("-" * 85)
    print(f"{'Allocation Method':<22} | {'Read Latency (Random)':<22} | {'Update/Append Overhead':<22} | {'Crash Resilience'}")
    print("-" * 85)
    print(f"{'Contiguous Allocation':<22} | {'O(1) - Instant (Best)':<22} | {'O(N) - Severe realloc':<22} | {'High (Simple metadata)'}")
    print(f"{'Linked Allocation':<22} | {'O(k) - Sequential seek':<22} | {'O(1) - Pointer append':<22} | {'Vulnerable (Lost links)'}")
    print(f"{'Indexed / Inode Extents':<22} | {'O(1) - Direct/Extent':<22} | {'O(1) - Fast B-Tree add':<22} | {'High (Journal-backed)'}")
    print("-" * 85)

    # Simulation of Caching Strategies
    cache_hit_rate = 0.94  # 94% of reads served from Linux Page Cache
    direct_reads_disk = reads_per_sec * (1.0 - cache_hit_rate)
    cached_reads_dram = reads_per_sec * cache_hit_rate

    # Write buffering analysis
    # Without writeback buffering: every update issues synchronous fsync() -> 10ms disk latency
    sync_write_latency_ms = 12.0
    sync_total_wait_sec = updates_per_sec * (sync_write_latency_ms / 1000.0)

    # With Linux Page Cache Write-Back + WAL Batching (50ms commit window)
    async_write_latency_us = 15.0  # DRAM copy latency
    wal_batch_window_ms = 50.0

    print("\n[B] BUFFERING & CACHING SUBSYSTEM PERFORMANCE")
    print("-" * 85)
    print("1. Read Path (Page Cache Acceleration):")
    print(f"   - Cached Reads (Served from DRAM Page Cache) : {cached_reads_dram:.2f} ops/sec ({cache_hit_rate*100:.0f}%)")
    print(f"   - Cold Reads (Physical NVMe Block I/O)       : {direct_reads_disk:.2f} ops/sec ({(1-cache_hit_rate)*100:.0f}%)")
    print(f"   - DRAM Read Access Time                      : ~100 nanoseconds")
    print(f"   - NVMe Read Access Time                      : ~80 microseconds")
    print("2. Write/Update Path (Synchronous vs. Asynchronous WAL):")
    print(f"   - Synchronous O_SYNC Writes (No Caching)     : Worker thread stalls {sync_total_wait_sec*1000:.1f} ms/sec ({(sync_total_wait_sec)*100:.1f}% I/O Wait)")
    print(f"   - Write-Back Page Cache with WAL Batching    : Ingestion latency drops to {async_write_latency_us:.1f} µs")
    print(f"   - Batched Group Commits to Journal           : 20 flushes/sec (every {wal_batch_window_ms:.0f} ms)")

    print("\n[C] CRASH RECOVERY & ATOMICITY ARCHITECTURE")
    print("-" * 85)
    print("• Problem: With 874 updates/min, a sudden server power failure or kernel panic")
    print("  can leave uncommitted order transactions, orphan driver assignments, or corrupted file inodes.")
    print("• Multi-Tier Recovery Solution:")
    print("  1. Ext4 Journaling (data=ordered):")
    print("     - Metadata transactions are written to circular on-disk journal before block pointers commit.")
    print("     - Guarantees zero file system corruption on sudden crash; replay time < 1.5 seconds.")
    print("  2. Application-Level Write-Ahead Logging (WAL):")
    print("     - Every state mutation (e.g. Order #1042 -> Status: PICKED_UP) appends to append-only WAL.")
    print("     - In-memory state can be 100% reconstructed by sequential log replay from latest checkpoint.")
    print("  3. Double Buffering & Copy-On-Write (COW):")
    print("     - State snapshots written to shadow pages and atomically swapped via rename() system call.")
    print("=" * 85)
    print("FINAL RECOMMENDATION:")
    print("-> Use INDEXED EXTENT-BASED ALLOCATION (Ext4 / XFS) paired with LINUX WRITE-BACK PAGE CACHE")
    print("   and WRITE-AHEAD LOGGING (WAL). This eliminates external fragmentation, caps random read/write")
    print("   latency at O(1), and satisfies strict zero-data-loss durability SLAs.")
    print("=" * 85)

if __name__ == "__main__":
    evaluate_file_system()
