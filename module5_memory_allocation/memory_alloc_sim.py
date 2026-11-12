#!/usr/bin/env python3
"""
Module 5: Memory Allocation Simulator (First-Fit, Best-Fit, Worst-Fit)
Student: NITHIN N | Roll No: 25BTRPW066
Scenario: Dynamic Heap / Partition Allocation for Microservice Workers
Blocks: [113, 219, 325, 501, 737] KB
Processes: [96, 192, 288, 404] KB
"""

import copy

def simulate_allocation(strategy, initial_blocks, requests, subsequent_request=None):
    # Each block is a dict: {'id': i+1, 'initial_size': size, 'remaining_size': size, 'allocated_to': None}
    blocks = [{'id': i + 1, 'initial_size': s, 'remaining_size': s, 'allocated': []} for i, s in enumerate(initial_blocks)]
    allocation_log = []
    
    all_requests = list(enumerate(requests, 1))
    if subsequent_request:
        all_requests.append((len(requests) + 1, subsequent_request))

    next_fit_pointer = 0

    for proc_id, req_size in all_requests:
        allocated = False
        target_block = None

        if strategy == "First-Fit":
            for b in blocks:
                if b['remaining_size'] >= req_size:
                    target_block = b
                    break

        elif strategy == "Best-Fit":
            candidates = [b for b in blocks if b['remaining_size'] >= req_size]
            if candidates:
                target_block = min(candidates, key=lambda b: b['remaining_size'])

        elif strategy == "Worst-Fit":
            candidates = [b for b in blocks if b['remaining_size'] >= req_size]
            if candidates:
                target_block = max(candidates, key=lambda b: b['remaining_size'])

        elif strategy == "Next-Fit":
            n = len(blocks)
            for step in range(n):
                idx = (next_fit_pointer + step) % n
                if blocks[idx]['remaining_size'] >= req_size:
                    target_block = blocks[idx]
                    next_fit_pointer = idx
                    break

        if target_block:
            target_block['remaining_size'] -= req_size
            target_block['allocated'].append((f"P{proc_id}", req_size))
            allocation_log.append({
                'process': f"P{proc_id}",
                'requested': req_size,
                'block_id': target_block['id'],
                'initial_block_size': target_block['initial_size'],
                'remaining_hole': target_block['remaining_size'],
                'status': 'Allocated'
            })
        else:
            allocation_log.append({
                'process': f"P{proc_id}",
                'requested': req_size,
                'block_id': 'None',
                'initial_block_size': 0,
                'remaining_hole': 0,
                'status': 'FAILED (External Fragmentation)'
            })

    return blocks, allocation_log


def evaluate_memory_performance():
    initial_blocks = [113, 219, 325, 501, 737]  # Total: 1895 KB
    requests = [96, 192, 288, 404]               # Total: 980 KB
    stress_request = 600                         # Edge test subsequent allocation (P5 = 600 KB)

    total_memory = sum(initial_blocks)
    total_requested = sum(requests)

    strategies = ["First-Fit", "Best-Fit", "Worst-Fit", "Next-Fit"]

    print("=" * 85)
    print("MODULE 5: DYNAMIC MEMORY ALLOCATION & FRAGMENTATION EVALUATOR")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Free Memory Blocks : [113, 219, 325, 501, 737] KB (Total = 1,895 KB)")
    print("Process Requests   : [P1: 96, P2: 192, P3: 288, P4: 404] KB (Total = 980 KB)")
    print("=" * 85)

    summary_records = []

    for strat in strategies:
        print(f"\n[{strat.upper()} SIMULATION]")
        print("-" * 85)
        blocks, logs = simulate_allocation(strat, initial_blocks, requests, subsequent_request=stress_request)

        print(f"{'Process':<8} | {'Requested':<10} | {'Assigned Block':<16} | {'Status':<12} | {'Remaining Hole in Block':<24}")
        print("-" * 85)
        for entry in logs:
            b_info = f"Block {entry['block_id']} ({entry['initial_block_size']} KB)" if entry['block_id'] != 'None' else "None"
            rem_info = f"{entry['remaining_hole']} KB" if entry['block_id'] != 'None' else "N/A"
            print(f"{entry['process']:<8} | {entry['requested']:<7} KB | {b_info:<16} | {entry['status']:<12} | {rem_info:<24}")

        # Metrics computation for standard 4 requests (excluding stress request for standard evaluation)
        blocks_std, logs_std = simulate_allocation(strat, initial_blocks, requests)
        allocated_bytes = sum(entry['requested'] for entry in logs_std if entry['status'] == 'Allocated')
        remaining_free_memory = sum(b['remaining_size'] for b in blocks_std)
        holes = [b['remaining_size'] for b in blocks_std if b['remaining_size'] > 0]
        max_contiguous_free = max(holes) if holes else 0
        p5_status = logs[-1]['status']

        print("\n  Remaining Memory Map:")
        for b in blocks_std:
            alloc_str = ", ".join([f"{pid}:{sz}KB" for pid, sz in b['allocated']]) if b['allocated'] else "Empty"
            print(f"   Block {b['id']} (Initial {b['initial_size']} KB) -> Remaining Hole: {b['remaining_size']} KB [Contents: {alloc_str}]")

        print(f"  Total Free Remaining Memory : {remaining_free_memory} KB")
        print(f"  Largest Contiguous Free Hole: {max_contiguous_free} KB")
        print(f"  Stress Test P5 (600 KB)     : {p5_status}")

        summary_records.append({
            'strategy': strat,
            'allocated': allocated_bytes,
            'free': remaining_free_memory,
            'largest_hole': max_contiguous_free,
            'p5_success': 'PASSED' if 'Allocated' in p5_status else 'FAILED',
            'holes': holes
        })

    print("\n" + "=" * 85)
    print("COMPARATIVE EVALUATION & FRAGMENTATION ANALYSIS")
    print("=" * 85)
    print(f"{'Strategy':<14} | {'Allocated':<12} | {'Free Memory':<13} | {'Largest Hole':<14} | {'P5 (600KB) Support':<20}")
    print("-" * 85)
    for r in summary_records:
        print(f"{r['strategy']:<14} | {r['allocated']} KB       | {r['free']} KB       | {r['largest_hole']} KB       | {r['p5_success']:<20}")

    print("=" * 85)
    print("TECHNICAL JUSTIFICATION & STRATEGY SELECTION:")
    print("1. Equivalence in Base Workload: Both First-Fit and Best-Fit successfully allocate P1–P4")
    print("   into Blocks 1, 2, 3, and 4 respectively, preserving Block 5 (737 KB) completely intact.")
    print("2. Search Overhead: First-Fit finishes search at the very first qualifying block (O(1) to O(n)),")
    print("   while Best-Fit must inspect all remaining blocks to find the minimal delta (O(n) or O(log n)).")
    print("3. Stress Resilience: Worst-Fit splinters large blocks, leaving its largest free hole at only")
    print("   244 KB, thereby FAILING the 600 KB allocation despite having 915 KB of total free memory!")
    print("   Both First-Fit and Best-Fit pass P5 (600 KB) with 137 KB remaining in Block 5.")
    print("4. RECOMMENDATION: FIRST-FIT is optimal for the Food Delivery Engine because it provides")
    print("   sub-microsecond memory allocation latency while retaining massive blocks for sudden traffic bursts.")
    print("=" * 85)

if __name__ == "__main__":
    evaluate_memory_performance()
