#include <stdio.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/mman.h>
#include <unistd.h>

void* shmaddr(int sz) {
   int shm_fd = shm_open("/gem5", O_CREAT | O_RDWR, 0666);
   if (shm_fd == -1) {
      printf("Shared memory failed\n");
      return NULL;
   }
   void* pmem = mmap(NULL, sz,
                     PROT_READ | PROT_WRITE,
                     MAP_SHARED, shm_fd, 0);
   return pmem;
}

