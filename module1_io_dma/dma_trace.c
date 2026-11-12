/**
 * Module 1: C/Linux Diagnostic Simulation of Interrupt vs. DMA
 * Student: NITHIN N | Roll Number: 25BTRPW066
 * Operating Systems Experimental Lab - Food Delivery Platform
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

#define TOTAL_MB 47
#define TOTAL_BYTES ((size_t)TOTAL_MB * 1024 * 1024)
#define PROMPT_INTERRUPT_COUNT 100
#define CHUNK_SIZE (TOTAL_BYTES / PROMPT_INTERRUPT_COUNT)

static inline uint64_t get_nanoseconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

// Simulates an Interrupt Service Routine (ISR) with register saves, buffer copy, and EOI signaling
void isr_handler(uint8_t *dest, const uint8_t *src, size_t len, int irq_id) {
    // Mimic volatile hardware I/O copy
    volatile uint8_t dummy = 0;
    for (size_t i = 0; i < len; i += 64) {
        dummy ^= src[i];
    }
    memcpy(dest, src, len);
    (void)dummy;
    (void)irq_id;
}

int main(void) {
    printf("================================================================================\n");
    printf("MODULE 1: C-BASED I/O TRANSFER & DIAGNOSTIC EMULATION\n");
    printf("Student: NITHIN N | Roll: 25BTRPW066\n");
    printf("Testing 47 MB Data Buffer Transfer: Interrupt Emulation vs Direct Bus (DMA)\n");
    printf("================================================================================\n");

    uint8_t *source_buffer = (uint8_t *)malloc(TOTAL_BYTES);
    uint8_t *dest_buffer = (uint8_t *)malloc(TOTAL_BYTES);

    if (!source_buffer || !dest_buffer) {
        fprintf(stderr, "Failed to allocate 47 MB buffer.\n");
        return 1;
    }

    // Initialize with order payload mock data
    memset(source_buffer, 0xAB, TOTAL_BYTES);

    printf("[1] Simulating 100-Interrupt Block-Buffered Transfer (470 KB/IRQ)...\n");
    uint64_t start_time = get_nanoseconds();
    for (int i = 0; i < PROMPT_INTERRUPT_COUNT; i++) {
        size_t offset = (size_t)i * CHUNK_SIZE;
        isr_handler(dest_buffer + offset, source_buffer + offset, CHUNK_SIZE, 42);
    }
    uint64_t interrupt_sim_time = get_nanoseconds() - start_time;

    printf("    -> Handled %d interrupts across %lu bytes.\n", PROMPT_INTERRUPT_COUNT, (unsigned long)TOTAL_BYTES);
    printf("    -> Elapsed CPU processing time: %.3f ms\n", (double)interrupt_sim_time / 1e6);

    printf("\n[2] Simulating Hardware DMA Engine (Single Completion IRQ)...\n");
    memset(dest_buffer, 0, TOTAL_BYTES);
    start_time = get_nanoseconds();
    // DMA transfers directly in hardware; CPU merely programs DMAC and waits for single interrupt
    memcpy(dest_buffer, source_buffer, TOTAL_BYTES); // Hardware bus-mastered burst copy
    uint64_t dma_sim_time = get_nanoseconds() - start_time;

    printf("    -> DMA Transfer complete with 1 completion interrupt.\n");
    printf("    -> Elapsed Hardware/Bus memory transfer time: %.3f ms\n", (double)dma_sim_time / 1e6);

    printf("\n[3] Diagnostic Summary:\n");
    printf("    -> Block-Buffered IRQ Model Time : %.3f ms (Requires %d kernel crossings)\n", 
           (double)interrupt_sim_time / 1e6, PROMPT_INTERRUPT_COUNT);
    printf("    -> Simulated DMA Direct Bus Time  : %.3f ms (Requires 1 IRQ at completion)\n", 
           (double)dma_sim_time / 1e6);
    printf("    -> DMA eliminates CPU interrupt processing by 99.00%% compared to 100 IRQs,\n");
    printf("       and by 99.999998%% compared to byte-level programmed I/O.\n");
    printf("================================================================================\n");

    free(source_buffer);
    free(dest_buffer);
    return 0;
}
