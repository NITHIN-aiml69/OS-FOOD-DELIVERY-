#!/usr/bin/env python3
"""
Module 4: Process Synchronization & Deadlocks Simulator
Student: NITHIN N | Roll No: 25BTRPW066
Scenario: 3 Concurrent Food Delivery Workers sharing 3 Resource Tokens and 1 Exclusive Log Resource
"""

import threading
import time
import random

class FoodDeliveryBanker:
    """
    Banker's Algorithm Deadlock Avoidance Simulator
    Resources:
      R0: Database Connection Tokens (Total = 3)
      R1: Exclusive Audit Log Mutex (Total = 1)
    """
    def __init__(self):
        self.workers = ["W1_OrderIngestion", "W2_RiderMatching", "W3_PaymentSettlement"]
        self.n_workers = len(self.workers)
        self.resource_names = ["DB_Tokens", "Audit_Log"]
        self.n_resources = len(self.resource_names)

        # Total system resources
        self.total_resources = [3, 1]

        # Max claims declared by each worker
        self.max_matrix = [
            [2, 1],  # W1 needs up to 2 DB tokens and Audit Log
            [2, 1],  # W2 needs up to 2 DB tokens and Audit Log
            [1, 1],  # W3 needs up to 1 DB token and Audit Log
        ]

        # Current allocation
        self.allocation = [
            [0, 0],
            [0, 0],
            [0, 0]
        ]

        # Need matrix = Max - Allocation
        self.need = [row[:] for row in self.max_matrix]

        # Available resources
        self.available = self.total_resources[:]

    def is_safe_state(self):
        work = self.available[:]
        finish = [False] * self.n_workers
        safe_sequence = []

        while len(safe_sequence) < self.n_workers:
            found = False
            for i in range(self.n_workers):
                if not finish[i]:
                    # Check if need[i] <= work
                    can_allocate = True
                    for j in range(self.n_resources):
                        if self.need[i][j] > work[j]:
                            can_allocate = False
                            break

                    if can_allocate:
                        for j in range(self.n_resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(self.workers[i])
                        found = True
                        break

            if not found:
                return False, []

        return True, safe_sequence

    def request_resources(self, worker_idx, request):
        worker_name = self.workers[worker_idx]
        print(f"\n[REQUEST] {worker_name} requesting {request} (Tokens={request[0]}, Log={request[1]})...")

        # Check 1: Request <= Need
        for j in range(self.n_resources):
            if request[j] > self.need[worker_idx][j]:
                print(f"  [ERROR] Worker {worker_name} exceeded its maximum declared claim!")
                return False

        # Check 2: Request <= Available
        for j in range(self.n_resources):
            if request[j] > self.available[j]:
                print(f"  [WAIT] Insufficient available resources. Available={self.available}. Worker must wait.")
                return False

        # Speculative Allocation
        for j in range(self.n_resources):
            self.available[j] -= request[j]
            self.allocation[worker_idx][j] += request[j]
            self.need[worker_idx][j] -= request[j]

        # Safety Check
        safe, seq = self.is_safe_state()
        if safe:
            print(f"  [APPROVED] Request Granted! State is SAFE.")
            print(f"  Safe Execution Sequence: {' -> '.join(seq)}")
            print(f"  Remaining Available: {self.available}")
            return True
        else:
            print(f"  [DENIED] Request Rejected! Allocating would lead to an UNSAFE / DEADLOCK-PRONE state.")
            # Rollback
            for j in range(self.n_resources):
                self.available[j] += request[j]
                self.allocation[worker_idx][j] -= request[j]
                self.need[worker_idx][j] += request[j]
            print(f"  Rolled back. Available remains: {self.available}")
            return False


def demonstrate_deadlock_condition():
    print("\n" + "=" * 80)
    print("DEMONSTRATION: UNCONTROLLED RESOURCE ACQUISITION CAUSING DEADLOCK")
    print("=" * 80)
    print("Scenario: Cross-locking between W1 (Order Ingestion) and W2 (Rider Matching)")
    print("• W1 acquires 2 DB Tokens, then attempts to acquire Audit Log.")
    print("• Concurrently, W2 acquires Audit Log, then attempts to acquire 2 DB Tokens.")
    print("• Only 1 DB Token remains available, but W2 requires 2 Tokens.")
    print("• RESULT: Coffman Conditions 1-4 satisfied (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait).")
    print("  -> DEADLOCK OCCURS: W1 waits indefinitely for Log; W2 waits indefinitely for Tokens!")
    print("-" * 80)


def demonstrate_bankers():
    print("=" * 80)
    print("MODULE 4: PROCESS SYNCHRONIZATION & DEADLOCK MITIGATION")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Shared Resources: 3 DB Connection Tokens, 1 Exclusive Audit Log Mutex")
    print("Workers: W1 (Order Ingestion), W2 (Rider Matching), W3 (Payment Settlement)")
    print("=" * 80)

    demonstrate_deadlock_condition()

    print("\n" + "=" * 80)
    print("SOLUTION 1: BANKER'S ALGORITHM DEADLOCK AVOIDANCE TRACE")
    print("=" * 80)
    banker = FoodDeliveryBanker()
    print(f"Initial Total Resources    : {banker.total_resources} (Tokens: 3, Log: 1)")
    print(f"Initial Available Resources: {banker.available}")
    print("Max Need Matrix:")
    for w, m in zip(banker.workers, banker.max_matrix):
        print(f"  {w:<22}: DB Tokens = {m[0]}, Log = {m[1]}")

    # Trace step 1: W3 requests [1, 0]
    banker.request_resources(2, [1, 0])

    # Trace step 2: W1 requests [1, 1]
    banker.request_resources(0, [1, 1])

    # Trace step 3: W2 requests [2, 0] (Should be evaluated or rejected/delayed if unsafe)
    banker.request_resources(1, [2, 0])

    # Trace step 4: W1 releases resources
    print("\n[RELEASE] W1 completed task and releases [1, 1]...")
    for j in range(2):
        banker.available[j] += banker.allocation[0][j]
        banker.allocation[0][j] = 0
        banker.need[0][j] = banker.max_matrix[0][j]
    print(f"  Updated Available: {banker.available}")

    # Trace step 5: W2 re-requests [2, 0]
    banker.request_resources(1, [2, 0])

    print("\n" + "=" * 80)
    print("SOLUTION 2: STRICT RESOURCE HIERARCHICAL ORDERING (PREVENTION)")
    print("=" * 80)
    print("• Rule: Impose a total order: R_Token (Order 1) < R_Log (Order 2).")
    print("• Protocol: Any worker requiring both resources MUST acquire R_Token before R_Log.")
    print("• Proof of Deadlock-Free Execution:")
    print("  - Let R(x) be the numeric priority of resource x.")
    print("  - Circular wait requires: W_A holds R1 waiting for R2 (R1 < R2), and W_B holds R2 waiting for R1 (R2 < R1).")
    print("  - This creates R1 < R2 < R1, a mathematical contradiction!")
    print("  - Thus, Circular Wait is strictly prevented under Havender's hierarchy.")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_bankers()
