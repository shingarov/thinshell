#include <fcntl.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>

#include <stdio.h>

void* ro;
void* rw;

int shareMemory() {
    off_t guard  = 0x20000;
    off_t roSize = 0x100000;
    off_t rwSize = 120 * 1024 * 1024;

    int shm_fd = shm_open("/gem5", O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) return -1;
    printf("shm_open() good\n");
    ftruncate(shm_fd, guard+roSize+rwSize);
    printf("ftruncate() good\n");

    int map_flags = MAP_SHARED | MAP_FIXED;
    ro = mmap((void*)guard, roSize,
                PROT_READ | PROT_EXEC,
                map_flags, shm_fd, 0);
    if (ro != (void*)guard) return -1;
    printf("mapped RO chunk\n");

    rw = mmap((void*)(guard+roSize), rwSize,
                PROT_READ | PROT_WRITE | PROT_EXEC,
                map_flags, shm_fd, roSize);
    if (rw != (void*)(guard+roSize)) return -1;
    printf("mapped RW chunk\n");

    explicit_bzero(rw, rwSize);

    return 0;
}

int main() {
    if (shareMemory() != 0) return 1;

    char *x = (char*) ro;
    // this segfaults, returning control back to ULD.
    // Same purpose as the "int3" in squeak.s
    *x = 1;

    // will never reach here
    return 0;
}

