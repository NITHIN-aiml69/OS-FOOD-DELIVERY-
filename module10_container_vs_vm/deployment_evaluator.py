#!/usr/bin/env python3
"""
Module 10: Containerization vs. Virtual Machines Deployment Evaluator
Student: NITHIN N | Roll No: 25BTRPW066
Workload: ~349 Concurrent Users Across Mobile Clients & Backend Services
Includes: Weighted Scoring Engine, Multi-Tier Service Mapping, IPC Analysis, Rollback Triggers
"""

def evaluate_deployment():
    print("=" * 85)
    print("MODULE 10: CONTAINERIZATION VS. VIRTUAL MACHINES ARCHITECTURAL EVALUATOR")
    print("Student: NITHIN N | Roll Number: 25BTRPW066")
    print("Platform Scale: ~349 Concurrent Active Users (Customers, Riders, Restaurants)")
    print("=" * 85)

    # 1. Weighted Scoring Framework
    criteria = [
        {"name": "Cold Startup Time", "weight": 0.15, "vm": 3, "container": 10, "notes": "Containers boot in <1s; VMs take 30-60s"},
        {"name": "Memory Overhead", "weight": 0.20, "vm": 4, "container": 10, "notes": "Containers share host kernel (~50MB/pod vs 2GB/VM)"},
        {"name": "CPU / Syscall Latency", "weight": 0.15, "vm": 6, "container": 9, "notes": "No hypervisor VM-exit penalties in containers"},
        {"name": "Storage Density", "weight": 0.10, "vm": 4, "container": 9, "notes": "Layered OCI overlayfs vs heavy VM disk images"},
        {"name": "Isolation & Multi-Tenancy", "weight": 0.15, "vm": 10, "container": 6, "notes": "VM hypervisors provide hardware ring-0 isolation"},
        {"name": "CI/CD & Rolling Deployments", "weight": 0.15, "vm": 5, "container": 10, "notes": "Zero-downtime blue/green rollouts via Kubernetes"},
        {"name": "Resource Utilization for 349 Users", "weight": 0.10, "vm": 4, "container": 10, "notes": "349 users easily fit in 3-4 small container pods"}
    ]

    print("\n[A] WEIGHTED MULTI-CRITERIA SCORING MATRIX")
    print("-" * 85)
    print(f"{'Evaluation Criterion':<28} | {'Weight':<7} | {'VM (1-10)':<9} | {'Container':<10} | {'Justification'}")
    print("-" * 85)

    total_vm_score = 0.0
    total_container_score = 0.0

    for c in criteria:
        vm_weighted = c['weight'] * c['vm']
        cont_weighted = c['weight'] * c['container']
        total_vm_score += vm_weighted
        total_container_score += cont_weighted
        print(f"{c['name']:<28} | {c['weight']:<7.2f} | {c['vm']:<9} | {c['container']:<10} | {c['notes']}")

    print("-" * 85)
    print(f"{'FINAL COMPOSITE SCORE (out of 10)':<28} | {'1.00':<7} | {total_vm_score:<9.2f} | {total_container_score:<10.2f} | WINNER: CONTAINERS")
    print("=" * 85)

    # 2. Service Tier & IPC Mapping
    print("\n[B] MICROSERVICES TOPOLOGY & IPC MECHANISM MAPPING (~349 USERS)")
    print("-" * 85)
    services = [
        {"tier": "Edge / Ingress", "service": "Envoy / NGINX Ingress", "ipc": "HTTPS / TLS termination, HTTP/2 to internal services"},
        {"tier": "Core Logic", "service": "Order Dispatcher Pod", "ipc": "gRPC over HTTP/2 (Protobuf serialization, low latency)"},
        {"tier": "Core Logic", "service": "Rider Matching Engine", "ipc": "Shared Memory (/dev/shm) for matrix route caching"},
        {"tier": "Financial Tier", "service": "Payment Settlement Pod", "ipc": "mTLS gRPC + Dedicated PCI-DSS isolated network namespace"},
        {"tier": "Streaming Tier", "service": "Rider Telemetry (GPS)", "ipc": "Unix Domain Socket (UDS) to local FluentBit / Kafka agent"}
    ]
    print(f"{'Service Tier':<18} | {'Service Name':<24} | {'Optimal IPC Protocol & Rationale'}")
    print("-" * 85)
    for s in services:
        print(f"{s['tier']:<18} | {s['service']:<24} | {s['ipc']}")
    print("-" * 85)

    # 3. Health Validation & Automated Rollback Triggers
    print("\n[C] VALIDATION SUITE & AUTOMATED ROLLBACK TRIGGERS")
    print("-" * 85)
    print("• Readiness & Liveness Probes:")
    print("  - Liveness  : GET /healthz (responds in < 200 ms; failure threshold: 3 checks)")
    print("  - Readiness : GET /readyz   (validates DB connection pool + Redis ping)")
    print("• Automated Production Rollback Triggers (Kubernetes Auto-Rollback):")
    print("  1. Trigger 1 (Error Rate): HTTP 5xx responses > 1.0% over any 60-second sliding window.")
    print("  2. Trigger 2 (Latency Spike): P99 latency exceeding 120 ms for > 90 seconds.")
    print("  3. Trigger 3 (Pod Stability): OOMKilled restart count >= 2 within 300 seconds.")
    print("  4. Trigger 4 (Rider Location Drift): GPS telemetry stream drop > 5% packets.")
    print("• Rollback Action:")
    print("  -> Automatically execute 'kubectl rollout undo deployment/order-dispatch' within 12 seconds,")
    print("     re-routing all traffic to the previously verified healthy replica set.")
    print("=" * 85)

if __name__ == "__main__":
    evaluate_deployment()
