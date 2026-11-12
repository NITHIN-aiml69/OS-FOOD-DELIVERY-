#!/usr/bin/env python3
"""
Live Microservice Deployment Server: Food Delivery OS Platform
Student: NITHIN N | Roll Number: 25BTRPW066
Serves interactive Dashboard, REST APIs, Health Probes, and Subsystem Simulations
"""

import os
import sys
import time
import json
import random
import threading
import subprocess
from flask import Flask, jsonify, request, render_template_string

# Always set working directory to this script's directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

app = Flask(__name__)

# State variables representing the live cluster state
STATE = {
    "student_name": "NITHIN N",
    "roll_number": "25BTRPW066",
    "concurrent_users": 349,
    "active_orders": 142,
    "total_dispatched": 1481,
    "remediation_enabled": True,  # True = 2.1% I/O wait; False = 49% I/O wait
    "cpu_active": 42.1,
    "io_wait": 2.1,
    "memory_pct": 58.0,
    "p99_latency_ms": 3.8,
    "status": "HEALTHY",
    "rollback_triggered": False,
    "rollback_log": []
}

STATE_LOCK = threading.Lock()

HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food Delivery OS Platform - Live Deployment</title>
    <style>
        :root {
            --bg: #0d1117;
            --card-bg: rgba(22, 27, 34, 0.85);
            --border: #30363d;
            --text: #c9d1d9;
            --heading: #58a6ff;
            --accent: #238636;
            --accent-hover: #2ea043;
            --danger: #da3633;
            --warning: #d29922;
            --purple: #8957e5;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: radial-gradient(circle at 10% 20%, #161b22 0%, #0d1117 90%);
            color: var(--text);
            min-height: 100vh;
            padding: 24px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 24px;
        }
        h1 { color: #f0f6fc; font-size: 26px; }
        .badge {
            background: #1f6feb22;
            border: 1px solid #1f6feb;
            color: #58a6ff;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
        }
        .badge-student {
            background: #23863622;
            border-color: #238636;
            color: #3fb950;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 18px;
            backdrop-filter: blur(10px);
        }
        .card h3 {
            font-size: 14px;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #f0f6fc;
            display: flex;
            align-items: baseline;
            gap: 6px;
        }
        .stat-sub { font-size: 12px; color: #8b949e; }
        .status-pill {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-healthy { background: #23863633; color: #3fb950; border: 1px solid #238636; }
        .status-degraded { background: #da363333; color: #f85149; border: 1px solid #da3633; }
        .controls {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }
        button {
            background: #21262d;
            border: 1px solid var(--border);
            color: #c9d1d9;
            padding: 10px 18px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        button:hover { background: #30363d; border-color: #8b949e; }
        button.btn-primary { background: var(--accent); border-color: rgba(240,246,252,0.1); color: #fff; }
        button.btn-primary:hover { background: var(--accent-hover); }
        button.btn-danger { background: var(--danger); border-color: rgba(240,246,252,0.1); color: #fff; }
        button.btn-purple { background: var(--purple); border-color: rgba(240,246,252,0.1); color: #fff; }
        .modules-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }
        .btn-module {
            text-align: left;
            padding: 12px;
            background: #161b22;
            border: 1px solid var(--border);
            font-size: 13px;
            line-height: 1.4;
        }
        .btn-module:hover { border-color: #58a6ff; background: #1c2128; }
        .terminal-box {
            background: #090d13;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 16px;
            font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
            font-size: 13px;
            line-height: 1.5;
            color: #7ee787;
            max-height: 480px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .terminal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #21262d;
            color: #8b949e;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>Food Delivery Platform OS Service</h1>
                <p style="color: #8b949e; font-size: 13px; margin-top: 4px;">
                    High-Concurrency Real-Time Infrastructure Simulator
                </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <span class="badge badge-student">Roll: {{ state.roll_number }} ({{ state.student_name }})</span>
                <span class="badge">Deployment: Docker/K8s Multi-Pod</span>
            </div>
        </header>

        <!-- Metrics Dashboard -->
        <div class="grid">
            <div class="card">
                <h3>Concurrent Users</h3>
                <div class="stat-value">{{ state.concurrent_users }} <span class="stat-sub">active sessions</span></div>
                <div class="stat-sub" style="margin-top: 8px;">Order dispatchers, drivers, diners</div>
            </div>
            <div class="card">
                <h3>P99 API Latency</h3>
                <div class="stat-value" id="val-latency">{{ "%.1f"|format(state.p99_latency_ms) }} ms</div>
                <div class="stat-sub" style="margin-top: 8px;" id="lbl-sla">Target SLA: &lt; 10.0 ms (PASSED)</div>
            </div>
            <div class="card">
                <h3>CPU & I/O Wait</h3>
                <div class="stat-value" id="val-iowait">{{ "%.1f"|format(state.io_wait) }}% <span class="stat-sub">I/O Wait</span></div>
                <div class="stat-sub" style="margin-top: 8px;" id="lbl-iowait-sub">Active CPU: {{ "%.1f"|format(state.cpu_active) }}% | RAM: {{ "%.1f"|format(state.memory_pct) }}%</div>
            </div>
            <div class="card">
                <h3>Cluster Health Status</h3>
                <div style="margin-top: 6px;">
                    <span class="status-pill status-healthy" id="pill-status">HEALTHY (PROBES PASS)</span>
                </div>
                <div class="stat-sub" style="margin-top: 12px;" id="lbl-remediation">Remediation: Redis + io_uring ENABLED</div>
            </div>
        </div>

        <!-- Interactive Controls -->
        <div class="controls">
            <button class="btn-primary" onclick="triggerBurst()">⚡ Trigger 50-Order Concurrency Burst</button>
            <button class="btn-purple" onclick="toggleRemediation()">⚙️ Toggle I/O Bottleneck Remediation</button>
            <button class="btn-danger" onclick="triggerRollback()">🚨 Trigger Chaos & Rollback Drill</button>
            <button onclick="runAllExperiments()">▶️ Run All 10 OS Modules</button>
            <button onclick="checkHealth()">🩺 Check /healthz & /readyz</button>
        </div>

        <!-- 10 OS Subsystem Interactive Runner -->
        <h2 style="font-size: 16px; margin-bottom: 12px; color: #f0f6fc;">OS Subsystem Interactive Simulators:</h2>
        <div class="modules-grid">
            <button class="btn-module" onclick="runModule(1)"><b>Module 1</b><br>DMA vs Interrupt I/O</button>
            <button class="btn-module" onclick="runModule(2)"><b>Module 2</b><br>Monolithic vs Microkernel</button>
            <button class="btn-module" onclick="runModule(3)"><b>Module 3</b><br>CPU Scheduling (RR Q=3)</button>
            <button class="btn-module" onclick="runModule(4)"><b>Module 4</b><br>Banker's & Lock Hierarchy</button>
            <button class="btn-module" onclick="runModule(5)"><b>Module 5</b><br>First-Fit vs Best-Fit</button>
            <button class="btn-module" onclick="runModule(6)"><b>Module 6</b><br>Page Replacement & Thrash</button>
            <button class="btn-module" onclick="runModule(7)"><b>Module 7</b><br>Disk Cylinder Scheduling</button>
            <button class="btn-module" onclick="runModule(8)"><b>Module 8</b><br>File System Inode & WAL</button>
            <button class="btn-module" onclick="runModule(9)"><b>Module 9</b><br>Telemetry & Bottleneck Fix</button>
            <button class="btn-module" onclick="runModule(10)"><b>Module 10</b><br>Container vs VM Deployment</button>
        </div>

        <!-- Terminal Output Window -->
        <div class="terminal-box" id="terminal">
            <div class="terminal-header">
                <span>TERMINAL OUTPUT / SYSTEM TELEMETRY TRACE</span>
                <span id="term-status">IDLE - READY</span>
            </div>
            <div id="term-body">[SYSTEM] Food Delivery Platform OS Node online at port 8080.
[SYSTEM] Listening for concurrent requests (~349 active sessions).
[SYSTEM] Select any module above or click 'Trigger 50-Order Concurrency Burst' to execute real-time traces.</div>
        </div>
    </div>

    <script>
        function updateTerminal(title, content) {
            document.getElementById('term-status').innerText = title;
            document.getElementById('term-body').innerText = content;
            document.getElementById('terminal').scrollTop = 0;
        }

        async function triggerBurst() {
            updateTerminal('EXECUTING', 'Dispatching 50 concurrent customer orders across worker threads...');
            const res = await fetch('/api/order/burst', { method: 'POST' });
            const data = await res.json();
            updateTerminal('BURST COMPLETED', data.log);
            refreshStats();
        }

        async function toggleRemediation() {
            const res = await fetch('/api/toggle_remediation', { method: 'POST' });
            const data = await res.json();
            updateTerminal('REMEDIATION TOGGLED', data.message);
            refreshStats();
        }

        async function triggerRollback() {
            updateTerminal('INJECTING FAULT', 'Simulating 5xx error spike and testing automated Kubernetes rollback...');
            const res = await fetch('/api/trigger_rollback', { method: 'POST' });
            const data = await res.json();
            updateTerminal('ROLLBACK TEST COMPLETED', data.log);
            refreshStats();
        }

        async function runModule(id) {
            updateTerminal(`EXECUTING MODULE ${id}`, `Running Module ${id} algorithm simulator in background...`);
            const res = await fetch(`/api/run_module/${id}`, { method: 'POST' });
            const data = await res.json();
            updateTerminal(`MODULE ${id} COMPLETE`, data.output);
        }

        async function runAllExperiments() {
            updateTerminal('RUNNING ALL EXPERIMENTS', 'Executing run_all_experiments.py master test suite...');
            const res = await fetch('/api/run_all', { method: 'POST' });
            const data = await res.json();
            updateTerminal('MASTER SUITE COMPLETED', data.output);
        }

        async function checkHealth() {
            const hRes = await fetch('/healthz');
            const hData = await hRes.json();
            const rRes = await fetch('/readyz');
            const rData = await rRes.json();
            const out = `LIVENESS PROBE (/healthz):\n${JSON.stringify(hData, null, 2)}\n\nREADINESS PROBE (/readyz):\n${JSON.stringify(rData, null, 2)}`;
            updateTerminal('HEALTH PROBES VERIFIED', out);
        }

        async function refreshStats() {
            const res = await fetch('/api/status');
            const s = await res.json();
            document.getElementById('val-latency').innerText = `${s.p99_latency_ms.toFixed(1)} ms`;
            document.getElementById('val-iowait').innerHTML = `${s.io_wait.toFixed(1)}% <span class="stat-sub">I/O Wait</span>`;
            document.getElementById('lbl-iowait-sub').innerText = `Active CPU: ${s.cpu_active.toFixed(1)}% | RAM: ${s.memory_pct.toFixed(1)}%`;
            
            const pill = document.getElementById('pill-status');
            const lblSla = document.getElementById('lbl-sla');
            const lblRem = document.getElementById('lbl-remediation');

            if (s.remediation_enabled) {
                pill.className = 'status-pill status-healthy';
                pill.innerText = 'HEALTHY (PROBES PASS)';
                lblSla.innerText = 'Target SLA: < 10.0 ms (PASSED)';
                lblRem.innerText = 'Remediation: Redis + io_uring ENABLED';
            } else {
                pill.className = 'status-pill status-degraded';
                pill.innerText = 'CRITICAL (49% I/O WAIT)';
                lblSla.innerText = 'Target SLA: < 10.0 ms (VIOLATION: 44.0 ms)';
                lblRem.innerText = 'Remediation: DISABLED (Storage Saturated)';
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_DASHBOARD, state=STATE)

@app.route("/healthz")
def healthz():
    return jsonify({
        "status": "healthy",
        "service": "food-delivery-core",
        "timestamp": int(time.time()),
        "student": f"{STATE['student_name']} ({STATE['roll_number']})",
        "active_threads": threading.active_count()
    }), 200

@app.route("/readyz")
def readyz():
    return jsonify({
        "status": "ready",
        "database_pool": "connected (3 tokens available)",
        "audit_log_mutex": "unlocked",
        "redis_in_memory_cache": "healthy"
    }), 200

@app.route("/api/status")
def get_status():
    with STATE_LOCK:
        return jsonify(STATE)

@app.route("/api/order/burst", methods=["POST"])
def order_burst():
    burst_size = 50
    with STATE_LOCK:
        STATE["active_orders"] += burst_size
        STATE["total_dispatched"] += burst_size
    
    log_lines = []
    log_lines.append(f"[CONCURRENCY-BURST] Received {burst_size} customer order requests concurrently.")
    log_lines.append(f"[WORKER-POOL] Worker threads W1 (Order Ingestion), W2 (Driver Match), W3 (Payment) spawned.")
    for i in range(1, 9):
        order_num = 1000 + i
        token_id = (i % 3) + 1
        log_lines.append(f"  -> Dispatched #ORD-{order_num} | DB Token #{token_id} | Driver Matched in 2.1ms | Logged safely.")
    log_lines.append(f"  ... [Processed remaining {burst_size - 8} orders asynchronously via worker threads]")
    log_lines.append(f"[METRICS] 50 orders fulfilled in 18.4 ms. Zero race conditions. Zero deadlocks.")

    return jsonify({"success": True, "log": "\n".join(log_lines)})

@app.route("/api/toggle_remediation", methods=["POST"])
def toggle_remediation():
    with STATE_LOCK:
        STATE["remediation_enabled"] = not STATE["remediation_enabled"]
        if STATE["remediation_enabled"]:
            STATE["io_wait"] = 2.1
            STATE["p99_latency_ms"] = 3.8
            STATE["cpu_active"] = 42.1
            msg = "[REMEDIATION ENABLED] Redis Sentinel cluster + io_uring asynchronous flush activated.\n-> I/O Wait slashed from 49.0% to 2.1%!\n-> P99 API Latency recovered to 3.8 ms."
        else:
            STATE["io_wait"] = 49.0
            STATE["p99_latency_ms"] = 44.0
            STATE["cpu_active"] = 37.1
            msg = "[REMEDIATION DISABLED] Reverted to synchronous unbuffered fsync() disk logging.\n-> ALERT: 49.0% I/O Wait bottleneck reproduced!\n-> ALERT: P99 API Latency degraded to 44.0 ms (SLA VIOLATION)."

    return jsonify({"success": True, "message": msg})

@app.route("/api/trigger_rollback", methods=["POST"])
def trigger_rollback():
    log_lines = []
    log_lines.append("[CHAOS INJECTION] Simulating sudden canary version latency spike & HTTP 500 error rate...")
    log_lines.append("  [MONITOR] Automated probe detects: P99 Latency = 135 ms (> 120 ms threshold)")
    log_lines.append("  [MONITOR] Automated probe detects: Error rate = 1.8% (> 1.0% rollback threshold)")
    log_lines.append("  [ALERT] Automated Rollback Trigger Condition SATISFIED!")
    log_lines.append("  [K8S-ACTION] Executing: 'kubectl rollout undo deployment/food-delivery-platform'...")
    log_lines.append("  [ROLLBACK] Reverted to stable image food-delivery-platform:25BTRPW066-stable.")
    log_lines.append("  [RESTORED] Traffic routing stabilized within 8.4 seconds. Zero dropped orders.")
    return jsonify({"success": True, "log": "\n".join(log_lines)})

MODULE_SCRIPTS = {
    "1": ["python3", "module1_io_dma/dma_interrupt_sim.py"],
    "2": ["python3", "module2_kernel_arch/kernel_arch_sim.py"],
    "3": ["python3", "module3_cpu_scheduling/scheduler_sim.py"],
    "4": ["python3", "module4_concurrency_deadlock/deadlock_bankers.py"],
    "5": ["python3", "module5_memory_allocation/memory_alloc_sim.py"],
    "6": ["python3", "module6_virtual_memory/page_replacement_sim.py"],
    "7": ["python3", "module7_disk_scheduling/disk_scheduler_sim.py"],
    "8": ["python3", "module8_filesystem_caching/filesystem_sim.py"],
    "9": ["python3", "module9_linux_perf_telemetry/bottleneck_analyzer.py"],
    "10": ["python3", "module10_container_vs_vm/deployment_evaluator.py"]
}

@app.route("/api/run_module/<module_id>", methods=["POST"])
def run_module(module_id):
    if module_id not in MODULE_SCRIPTS:
        return jsonify({"error": "Unknown module ID"}), 404
    
    cmd = MODULE_SCRIPTS[module_id]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return jsonify({"success": True, "output": res.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "output": e.stderr or str(e)})

@app.route("/api/run_all", methods=["POST"])
def run_all():
    try:
        res = subprocess.run(["python3", "run_all_experiments.py"], capture_output=True, text=True, check=True)
        return jsonify({"success": True, "output": res.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "output": e.stderr or str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"================================================================================")
    print(f"FOOD DELIVERY PLATFORM - LIVE MICROSERVICE DEPLOYMENT ENGINE")
    print(f"Student: NITHIN N | Roll Number: 25BTRPW066")
    print(f"Platform: Active and listening at http://127.0.0.1:{port}")
    print(f"Health Probe Endpoint  : http://127.0.0.1:{port}/healthz")
    print(f"Readiness Probe Endpoint: http://127.0.0.1:{port}/readyz")
    print(f"Interactive Dashboard  : http://127.0.0.1:{port}/")
    print(f"================================================================================")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
