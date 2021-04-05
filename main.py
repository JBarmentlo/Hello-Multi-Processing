
from multiprocessing import Lock, Process, Queue, shared_memory
import numpy as np
# import time
# import queue # imported for using queue.Empty exception


def f(arr):
    print(type(arr))
    print(arr)

if __name__ == "__main__":
    a = np.zeros([3])
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
    b = np.ndarray(a.shape, dtype = a.dtype, buffer = shm.buf)
    b[:] = a[:]
    print(b)
    # shm2 = shared_memory.SharedMemory(name=shm.name)
    print(shm.buf)
    # shm2.close()
    shm.close()
    shm.unlink()
    # shm2.unlink()
