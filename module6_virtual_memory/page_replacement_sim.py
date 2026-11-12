#!/usr/bin/env python3
"""
Module 6: Virtual Memory & Page Replacement Simulator
Student: NITHIN N | Roll No: 25BTRPW066
Reference String: [4, 5, 6, 7, 4, 5, 1, 4, 5, 6, 7, 1]
Page Frames: 4
Algorithms: FIFO, LRU, Optimal (OPT) + Thrashing Detection & Mitigation Engine
"""

def simulate_fifo(ref_string, num_frames):
    frames = []
    faults = 0
    hits = 0
    trace = []

    for idx, page in enumerate(ref_string):
        status = ""
        evicted = None
        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                evicted = frames.pop(0)
                frames.append(page)
        
        # Snapshot of frames (padded to num_frames)
        display_frames = frames + ["-"] * (num_frames - len(frames))
        trace.append({
            'step': idx + 1,
            'ref': page,
            'frames': list(display_frames),
            'status': status,
            'evicted': evicted
        })

    return {"algo": "FIFO", "faults": faults, "hits": hits, "trace": trace}


def simulate_lru(ref_string, num_frames):
    frames = []  # will maintain order from least recently used to most recently used
    faults = 0
    hits = 0
    trace = []

    for idx, page in enumerate(ref_string):
        status = ""
        evicted = None
        if page in frames:
            hits += 1
            status = "HIT"
            # Move accessed page to the end (MRU)
            frames.remove(page)
            frames.append(page)
        else:
            faults += 1
            status = "FAULT"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                # Evict the least recently used (first element)
                evicted = frames.pop(0)
                frames.append(page)

        display_frames = frames + ["-"] * (num_frames - len(frames))
        trace.append({
            'step': idx + 1,
            'ref': page,
            'frames': list(display_frames),
            'status': status,
            'evicted': evicted
        })

    return {"algo": "LRU", "faults": faults, "hits": hits, "trace": trace}


def simulate_optimal(ref_string, num_frames):
    frames = []
    faults = 0
    hits = 0
    trace = []
    n = len(ref_string)

    for idx, page in enumerate(ref_string):
        status = ""
        evicted = None
        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                # Find page in frames that will not be used for the longest time in future
                future_refs = ref_string[idx + 1:]
                farthest_dist = -1
                victim = None

                for f in frames:
                    if f not in future_refs:
                        victim = f
                        break
                    else:
                        next_use = future_refs.index(f)
                        if next_use > farthest_dist:
                            farthest_dist = next_use
                            victim = f

                evicted = victim
                evict_idx = frames.index(victim)
                frames[evict_idx] = page

        display_frames = frames + ["-"] * (num_frames - len(frames))
        trace.append({
            'step': idx + 1,
            'ref': page,
            'frames': list(display_frames),
            'status': status,
            'evicted': evicted
        })

    return {"algo": "Optimal (OPT)", "faults": faults, "hits": hits, "trace": trace}


def print_step_trace(result, num_frames):
    print(f"\n[{result['algo'].upper()} STEP-BY-STEP TRACE]")
    print("-" * 75)
    frame_headers = " | ".join([f"Frame {i+1}" for i in range(num_frames)])
    print(f"{'Step':<5} | {'Ref Page':<8} | {frame_headers} | {'Event':<8} | {'Evicted'}")
    print("-" * 75)

    for row in result['trace']:
        frames_str = " | ".join([f"{str(f):^7}" for f in row['frames']])
        evict_str = f"Page {row['evicted']}" if row['evicted'] is not None else "-"
        print(f"{row['step']:<5} | {row['ref']:^8} | {frames_str} | {row['status']:<8} | {evict_str}")

    print("-" * 75)
    total_refs = len(result['trace'])
    hit_ratio = (result['hits'] / total_refs) * 100
    fault_ratio = (result['faults'] / total_refs) * 100
    print(f"Total Page Faults : {result['faults']} / {total_refs} ({fault_ratio:.2f}%)")
    print(f"Total Page Hits   : {result['hits']} / {total_refs} ({hit_ratio:.2f}%)")


def evaluate_thrashing_logic(pff_history, upper_threshold=0.60, lower_threshold=0.20):
    print("\n" + "=" * 80)
    print("THRASHING DETECTION & MITIGATION CONTROL ENGINE (PFF & WORKING SET)")
    print("=" * 80)
    print(f"Defined Policy Thresholds: Upper PFF = {upper_threshold*100:.0f}%, Lower PFF = {lower_threshold*100:.0f}%")
    print("-" * 80)
    print(f"{'Time Window':<12} | {'Local Fault Rate':<18} | {'Engine Diagnosis':<24} | {'Kernel Mitigation Action'}")
    print("-" * 80)

    for window_id, pff in enumerate(pff_history, 1):
        if pff > upper_threshold:
            diag = "CRITICAL THRASHING"
            action = "Suspend low-pri batch jobs (e.g. daily reports); grant +2 frames to dispatcher"
        elif pff < lower_threshold:
            diag = "OVER-ALLOCATED"
            action = "Reclaim 1 frame; return to free-page pool"
        else:
            diag = "OPTIMAL STABLE"
            action = "Maintain current working set frame allocation"

        print(f"Window {window_id:<5} | {pff*100:<17.1f}% | {diag:<24} | {action}")

    print("=" * 80)


def run_virtual_memory_lab():
    ref_string = [4, 5, 6, 7, 4, 5, 1, 4, 5, 6, 7, 1]
    num_frames = 4

    print("=" * 80)
    print("MODULE 6: VIRTUAL MEMORY PAGE REPLACEMENT SIMULATION")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print(f"Reference String : {ref_string} (Length: {len(ref_string)})")
    print(f"Available Frames : {num_frames} Page Frames")
    print("=" * 80)

    res_fifo = simulate_fifo(ref_string, num_frames)
    res_lru = simulate_lru(ref_string, num_frames)
    res_opt = simulate_optimal(ref_string, num_frames)

    print_step_trace(res_fifo, num_frames)
    print_step_trace(res_lru, num_frames)
    print_step_trace(res_opt, num_frames)

    print("\n" + "=" * 80)
    print("COMPARATIVE SUMMARY ACROSS PAGE REPLACEMENT POLICIES")
    print("=" * 80)
    print(f"{'Algorithm':<18} | {'Total Faults':<14} | {'Total Hits':<12} | {'Fault Ratio':<14} | {'Hit Ratio':<12}")
    print("-" * 80)
    for res in [res_fifo, res_lru, res_opt]:
        n = len(ref_string)
        fr = (res['faults'] / n) * 100
        hr = (res['hits'] / n) * 100
        print(f"{res['algo']:<18} | {res['faults']:<14} | {res['hits']:<12} | {fr:<13.1f}% | {hr:<11.1f}%")

    print("=" * 80)
    print("KEY INSIGHTS & PLATFORM ARCHITECTURAL JUSTIFICATION:")
    print("• FIFO suffers 10 page faults (83.3% fault rate) because it blindly evicts heavily-used")
    print("  early pages (like 4 and 5) that represent hot core catalog/order state.")
    print("• LRU reduces faults to 8 (33.3% hit rate), capitalizing on temporal locality.")
    print("• Optimal sets the theoretical lower bound at 6 faults (50.0% hit rate).")
    print("• In production Linux (and our Food Delivery Platform), kernel uses Clock / Two-Handed Clock (2Q),")
    print("  an O(1) approximation of LRU that protects hot caching pages without hardware timestamp overhead.")
    print("=" * 80)

    # Demonstrate Thrashing Mitigation Engine
    sample_pff = [0.83, 0.67, 0.50, 0.15, 0.35]
    evaluate_thrashing_logic(sample_pff)

if __name__ == "__main__":
    run_virtual_memory_lab()
