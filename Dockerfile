# Multi-stage Dockerfile for Food Delivery Platform OS Runtime
# Student: NITHIN N | Roll Number: 25BTRPW066

# Stage 1: Build C benchmarks and binaries
FROM gcc:12-bullseye AS builder
WORKDIR /build
COPY module1_io_dma/dma_trace.c ./
COPY module2_kernel_arch/fork_exec_monolithic.c ./
COPY module4_concurrency_deadlock/sync_posix.c ./

RUN gcc -O2 dma_trace.c -o dma_trace && \
    gcc -O2 fork_exec_monolithic.c -o fork_exec_monolithic && \
    gcc -O2 -pthread sync_posix.c -o sync_posix

# Stage 2: Final lightweight runtime container
FROM python:3.11-slim-bullseye
WORKDIR /app

# Install system utilities for Linux performance telemetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    sysstat \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir flask

# Copy project files and compiled binaries
COPY . /app/
COPY --from=builder /build/dma_trace /app/module1_io_dma/
COPY --from=builder /build/fork_exec_monolithic /app/module2_kernel_arch/
COPY --from=builder /build/sync_posix /app/module4_concurrency_deadlock/

# Grant execute permissions
RUN chmod +x /app/run_all_experiments.py /app/deploy.sh

# Expose HTTP API & Dashboard Port
EXPOSE 8080

# Configure Healthchecks
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8080/healthz || exit 1

# Environment variables
ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PLATFORM_ENV=production \
    CONCURRENT_USERS=349

CMD ["python3", "platform_server.py"]
