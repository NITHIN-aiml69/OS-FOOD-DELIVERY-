/**
 * Module 2: POSIX Monolithic Process Lifecycle (fork-exec-wait)
 * Student: NITHIN N | Roll Number: 25BTRPW066
 * Operating Systems Experimental Lab - Food Delivery Platform
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <stdint.h>

static inline uint64_t get_nanoseconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

int main(void) {
    printf("================================================================================\n");
    printf("MODULE 2: POSIX MONOLITHIC PROCESS CREATION TRACE (FORK-EXEC-WAIT)\n");
    printf("Student: NITHIN N | Roll: 25BTRPW066\n");
    printf("Platform Worker: Spawning Restaurant Notification Dispatcher\n");
    printf("================================================================================\n");

    pid_t parent_pid = getpid();
    printf("[PARENT] Master Dispatcher Process PID: %d\n", parent_pid);

    uint64_t t_start = get_nanoseconds();

    pid_t child_pid = fork();

    if (child_pid < 0) {
        perror("fork failed");
        return 1;
    } else if (child_pid == 0) {
        // Child Process
        printf("  [CHILD] Created child worker PID: %d, Parent PID: %d\n", getpid(), getppid());
        printf("  [CHILD] Executing 'echo' via execvp to simulate task handoff...\n");

        char *args[] = {"echo", "  [CHILD-TASK] Order #ORD-9823 Dispatch Notification Sent to Kitchen!", NULL};
        execvp(args[0], args);

        // If execvp returns, error occurred
        perror("execvp failed");
        exit(1);
    } else {
        // Parent Process
        printf("[PARENT] Forked Child PID: %d. Calling waitpid()...\n", child_pid);

        int status;
        pid_t reaped_pid = waitpid(child_pid, &status, 0);
        uint64_t t_end = get_nanoseconds();

        if (WIFEXITED(status)) {
            printf("[PARENT] Child PID %d reaped successfully with exit code: %d\n", 
                   reaped_pid, WEXITSTATUS(status));
        }

        double elapsed_us = (double)(t_end - t_start) / 1000.0;
        printf("[PARENT] Total roundtrip fork-exec-wait elapsed time: %.2f µs (%.3f ms)\n", 
               elapsed_us, elapsed_us / 1000.0);
        printf("================================================================================\n");
    }

    return 0;
}
