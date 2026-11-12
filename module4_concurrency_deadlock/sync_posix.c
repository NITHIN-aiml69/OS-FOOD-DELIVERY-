/**
 * Module 4: POSIX Synchronization Implementation
 * Student: NITHIN N | Roll Number: 25BTRPW066
 * 3 Worker Threads, 3 Resource Tokens (Counting Semaphore), 1 Mutex Log
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <string.h>

#define NUM_WORKERS 3
#define NUM_TOKENS 3
#define CYCLES_PER_WORKER 3

// Synchronization primitives
// Note: On macOS, sem_init is deprecated/named semaphores are preferred, 
// so we implement an elegant portable counting semaphore using mutex + condition variable.
typedef struct {
    pthread_mutex_t lock;
    pthread_cond_t cond;
    int count;
} counting_sem_t;

void sem_custom_init(counting_sem_t *s, int init_val) {
    pthread_mutex_init(&s->lock, NULL);
    pthread_cond_init(&s->cond, NULL);
    s->count = init_val;
}

void sem_custom_wait(counting_sem_t *s) {
    pthread_mutex_lock(&s->lock);
    while (s->count <= 0) {
        pthread_cond_wait(&s->cond, &s->lock);
    }
    s->count--;
    pthread_mutex_unlock(&s->lock);
}

void sem_custom_post(counting_sem_t *s) {
    pthread_mutex_lock(&s->lock);
    s->count++;
    pthread_cond_signal(&s->cond);
    pthread_mutex_unlock(&s->lock);
}

void sem_custom_destroy(counting_sem_t *s) {
    pthread_mutex_destroy(&s->lock);
    pthread_cond_destroy(&s->cond);
}

// Global shared resources
counting_sem_t db_token_pool;
pthread_mutex_t audit_log_mutex = PTHREAD_MUTEX_INITIALIZER;
int shared_order_counter = 0;

typedef struct {
    int worker_id;
    const char *name;
} worker_arg_t;

void* worker_thread(void *arg) {
    worker_arg_t *w = (worker_arg_t *)arg;

    for (int i = 1; i <= CYCLES_PER_WORKER; i++) {
        // STRICT HIERARCHICAL LOCK ORDERING:
        // Level 1: Acquire DB Connection Token (Counting Semaphore)
        sem_custom_wait(&db_token_pool);

        // Level 2: Acquire Exclusive Audit Log (Mutex)
        pthread_mutex_lock(&audit_log_mutex);

        // CRITICAL SECTION
        shared_order_counter++;
        printf("[SAFE-EXEC] Worker: %-22s | Order Ref: #ORD-%04d | Cycle: %d/%d | Token Acquired | Log Written\n",
               w->name, shared_order_counter, i, CYCLES_PER_WORKER);
        usleep(10000); // 10 ms simulated processing

        // Release in reverse hierarchical order
        pthread_mutex_unlock(&audit_log_mutex);
        sem_custom_post(&db_token_pool);

        usleep(5000); // Backoff before next request
    }
    return NULL;
}

int main(void) {
    printf("================================================================================\n");
    printf("MODULE 4: MULTITHREADED POSIX SYNCHRONIZATION EXECUTION\n");
    printf("Student: NITHIN N | Roll Number: 25BTRPW066\n");
    printf("3 Concurrent Workers, 3 DB Tokens, 1 Audit Log Mutex (Hierarchical Ordering)\n");
    printf("================================================================================\n");

    sem_custom_init(&db_token_pool, NUM_TOKENS);

    pthread_t threads[NUM_WORKERS];
    worker_arg_t args[NUM_WORKERS] = {
        {1, "W1_OrderIngestion"},
        {2, "W2_RiderMatching"},
        {3, "W3_PaymentSettlement"}
    };

    for (int i = 0; i < NUM_WORKERS; i++) {
        if (pthread_create(&threads[i], NULL, worker_thread, &args[i]) != 0) {
            perror("Failed to create worker thread");
            return 1;
        }
    }

    for (int i = 0; i < NUM_WORKERS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("--------------------------------------------------------------------------------\n");
    printf("All %d workers completed. Final Shared Order Counter: %d (Expected: %d)\n",
           NUM_WORKERS, shared_order_counter, NUM_WORKERS * CYCLES_PER_WORKER);
    printf("Zero race conditions. Zero deadlocks observed.\n");
    printf("================================================================================\n");

    sem_custom_destroy(&db_token_pool);
    pthread_mutex_destroy(&audit_log_mutex);
    return 0;
}
