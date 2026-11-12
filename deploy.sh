#!/usr/bin/env bash
# Master Deployment Automation Script: Food Delivery OS Platform
# Student: NITHIN N | Roll Number: 25BTRPW066

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "================================================================================"
echo "DEPLOYING HIGH-CONCURRENCY FOOD DELIVERY PLATFORM"
echo "Student: NITHIN N | Roll Number: 25BTRPW066"
echo "Target Platform: Cloud Microservice Pods (macOS / Linux POSIX)"
echo "================================================================================"

echo "[1/4] Compiling low-level POSIX and C simulation binaries..."
clang -O2 module1_io_dma/dma_trace.c -o module1_io_dma/dma_trace
clang -O2 module2_kernel_arch/fork_exec_monolithic.c -o module2_kernel_arch/fork_exec_monolithic
clang -O2 -pthread module4_concurrency_deadlock/sync_posix.c -o module4_concurrency_deadlock/sync_posix
echo "      -> C Binaries compiled successfully."

echo "[2/4] Verifying all 10 OS core subsystem components..."
python3 run_all_experiments.py > /dev/null
echo "      -> All 10 modules verified (100% test pass rate)."

echo "[3/4] Checking Containerization & Kubernetes Manifests..."
test -f Dockerfile && echo "      -> Dockerfile: OK"
test -f docker-compose.yml && echo "      -> docker-compose.yml: OK"
test -f k8s/deployment.yaml && echo "      -> k8s/deployment.yaml: OK"
test -f k8s/service.yaml && echo "      -> k8s/service.yaml: OK"
test -f k8s/hpa.yaml && echo "      -> k8s/hpa.yaml: OK"

echo "[4/4] Starting Live Platform Microservice Server at http://127.0.0.1:8080 ..."
echo "      -> Dashboard: http://127.0.0.1:8080"
echo "      -> Liveness Probe: http://127.0.0.1:8080/healthz"
echo "      -> Readiness Probe: http://127.0.0.1:8080/readyz"
echo "================================================================================"

exec python3 platform_server.py
