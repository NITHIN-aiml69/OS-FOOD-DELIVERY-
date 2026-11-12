#!/usr/bin/env python3
"""
Module 7: Disk Scheduling Algorithms Simulator
Student: NITHIN N | Roll No: 25BTRPW066
Requests: [32, 68, 104, 140, 174, 52, 120, 192]
Initial Head: 142 (Moving toward lower cylinders)
Disk Boundaries: Cylinders 0 to 199
Algorithms: FCFS, SSTF, SCAN, C-SCAN (and LOOK / C-LOOK)
"""

def simulate_fcfs(requests, initial_head):
    sequence = [initial_head] + list(requests)
    movements = []
    total_movement = 0

    for i in range(len(sequence) - 1):
        diff = abs(sequence[i+1] - sequence[i])
        movements.append(diff)
        total_movement += diff

    return {
        'algo': 'FCFS',
        'sequence': sequence,
        'movements': movements,
        'total_movement': total_movement
    }


def simulate_sstf(requests, initial_head):
    unvisited = list(requests)
    current_head = initial_head
    sequence = [initial_head]
    movements = []
    total_movement = 0

    while unvisited:
        # Pick request with minimum distance to current_head
        # Tie break: lower cylinder number
        closest = min(unvisited, key=lambda r: (abs(r - current_head), r))
        diff = abs(closest - current_head)
        movements.append(diff)
        total_movement += diff
        current_head = closest
        sequence.append(current_head)
        unvisited.remove(closest)

    return {
        'algo': 'SSTF',
        'sequence': sequence,
        'movements': movements,
        'total_movement': total_movement
    }


def simulate_scan(requests, initial_head, max_cylinder=199, direction="down"):
    """
    SCAN (Elevator): moves toward lower cylinders until cylinder 0, then reverses toward 199.
    """
    lower = sorted([r for r in requests if r <= initial_head], reverse=True)
    upper = sorted([r for r in requests if r > initial_head])

    sequence = [initial_head]
    if direction == "down":
        # Visit lower requests down to 0
        sequence.extend(lower)
        if 0 not in sequence:
            sequence.append(0)  # Reaches boundary 0
        sequence.extend(upper)
    else:
        sequence.extend(upper)
        if max_cylinder not in sequence:
            sequence.append(max_cylinder)
        sequence.extend(lower)

    movements = []
    total_movement = 0
    for i in range(len(sequence) - 1):
        diff = abs(sequence[i+1] - sequence[i])
        movements.append(diff)
        total_movement += diff

    return {
        'algo': 'SCAN',
        'sequence': sequence,
        'movements': movements,
        'total_movement': total_movement
    }


def simulate_c_scan(requests, initial_head, max_cylinder=199, direction="down"):
    """
    C-SCAN (Circular SCAN): moves toward cylinder 0, jumps to 199, continues in same direction.
    """
    lower = sorted([r for r in requests if r <= initial_head], reverse=True)
    upper = sorted([r for r in requests if r > initial_head], reverse=True)

    sequence = [initial_head]
    if direction == "down":
        sequence.extend(lower)
        if 0 not in sequence:
            sequence.append(0)
        # Circular jump to outer end (199)
        sequence.append(max_cylinder)
        sequence.extend(upper)
    else:
        # Upward C-SCAN
        upper_asc = sorted(upper)
        sequence.extend(upper_asc)
        sequence.append(max_cylinder)
        sequence.append(0)
        sequence.extend(sorted(lower))

    movements = []
    total_movement = 0
    for i in range(len(sequence) - 1):
        diff = abs(sequence[i+1] - sequence[i])
        movements.append(diff)
        total_movement += diff

    return {
        'algo': 'C-SCAN',
        'sequence': sequence,
        'movements': movements,
        'total_movement': total_movement
    }


def simulate_look(requests, initial_head, direction="down"):
    """
    LOOK: Like SCAN but only goes as far as the lowest request (no excursion to cylinder 0).
    """
    lower = sorted([r for r in requests if r <= initial_head], reverse=True)
    upper = sorted([r for r in requests if r > initial_head])

    sequence = [initial_head] + lower + upper
    movements = []
    total_movement = 0
    for i in range(len(sequence) - 1):
        diff = abs(sequence[i+1] - sequence[i])
        movements.append(diff)
        total_movement += diff

    return {
        'algo': 'LOOK',
        'sequence': sequence,
        'movements': movements,
        'total_movement': total_movement
    }


def format_sequence(seq):
    return " -> ".join(map(str, seq))


def print_disk_results():
    requests = [32, 68, 104, 140, 174, 52, 120, 192]
    initial_head = 142
    max_cylinder = 199

    print("=" * 85)
    print("MODULE 7: DISK SCHEDULING ALGORITHMS SIMULATOR")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print(f"Pending Requests   : {requests} (Total: {len(requests)})")
    print(f"Initial Head Pos   : {initial_head}")
    print(f"Initial Direction  : Decreasing / Downward (towards cylinder 0)")
    print(f"Disk Boundaries    : 0 to {max_cylinder} (200 Cylinders)")
    print("=" * 85)

    r_fcfs = simulate_fcfs(requests, initial_head)
    r_sstf = simulate_sstf(requests, initial_head)
    r_scan = simulate_scan(requests, initial_head, max_cylinder, direction="down")
    r_cscan = simulate_c_scan(requests, initial_head, max_cylinder, direction="down")
    r_look = simulate_look(requests, initial_head, direction="down")

    results = [r_fcfs, r_sstf, r_scan, r_cscan, r_look]

    for res in results:
        print(f"\n[{res['algo']} EXECUTION TRACE]")
        print("-" * 85)
        print(f"Seek Trajectory : {format_sequence(res['sequence'])}")
        print(f"Step Seek Diffs : {res['movements']}")
        print(f"Total Movement  : {res['total_movement']} Cylinders")

    print("\n" + "=" * 85)
    print("COMPARATIVE EVALUATION SUMMARY")
    print("=" * 85)
    print(f"{'Algorithm':<14} | {'Total Head Movement':<22} | {'Relative Overhead vs SSTF':<26} | {'Starvation Risk'}")
    print("-" * 85)
    sstf_mv = r_sstf['total_movement']
    for res in results:
        ratio = (res['total_movement'] / sstf_mv) * 100 - 100
        ratio_str = f"+{ratio:.1f}%" if ratio > 0 else "0.0% (Baseline)"
        starv = "High (Far cylinders)" if res['algo'] == "SSTF" else "None"
        if res['algo'] == "FCFS":
            starv = "None (High Variance)"
        print(f"{res['algo']:<14} | {res['total_movement']:<6} cylinders        | {ratio_str:<26} | {starv}")

    print("=" * 85)
    print("TECHNICAL JUSTIFICATION & STORAGE SUBSYSTEM RECOMMENDATION:")
    print("1. Rotational Media (HDD): SSTF achieves the absolute lowest seek movement (270 cylinders),")
    print("   closely matched by LOOK (270 cylinders). However, SSTF risks severe starvation of outer")
    print("   cylinders (174, 192) under bursty order streams. C-SCAN / LOOK provides bounded wait-time variance.")
    print("2. Modern Cloud SSD / NVMe (Food Delivery Platform Reality): Flash storage has zero physical")
    print("   moving read/write heads (seek time = 0). Cylinder scheduling is obsolete for SSDs.")
    print("3. Production Recommendation: Use Linux 'mq-deadline' or 'none/kyber' multi-queue scheduler.")
    print("   mq-deadline enforces read/write deadline expiration guarantees, ensuring order placement API")
    print("   writes are completed within <5ms while serving real-time customer read queries.")
    print("=" * 85)

if __name__ == "__main__":
    print_disk_results()
