from multiprocessing import Process, shared_memory, Lock, Queue
import numpy as np
import random
import time
import tensorflow as tf


nb_process = 2
weights = np.zeros([4])
ashape = weights.shape
adtype = weights.dtype

class Agent():
    def __init__(self, shm_name, lock, proc_nb, q):
        self.shm = shared_memory.SharedMemory(name=shm_name)
        self.weights = np.ndarray(ashape, dtype = adtype, buffer = shm.buf)
        self.lock = lock
        self.proc_nb = proc_nb
        self.q = q
        self.test = np.zeros(ashape)
        print(f"created process nb {self.proc_nb}")


    def create_grad(self):
        # print(f"Processing grad for proc nb {self.proc_nb}")
        # time.sleep(random.random())
        return (np.random.rand(*self.weights.shape))


    def push_grad(self, grad):
        if (self.q.full()):
            return (True)
        self.lock.acquire()
        # print(f"Pushing grad {self.proc_nb}\n{grad}")
        self.weights[:] = self.weights[:] + grad[:]
        self.test += grad
        self.lock.release()
        # print(f"{self.proc_nb}\n{self.test}")
        return (False)



def f(shm_name, lock, proc_nb, q):
    agent = Agent(shm_name, lock, proc_nb, q)
    while (True):
        grad = agent.create_grad()
        if (agent.push_grad(grad)):
            print("FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n\n\n\n\n")
            break


if __name__ == "__main__":
    processes = []
    shm = shared_memory.SharedMemory(create=True, size=weights.nbytes, name="Params")
    shared_weights = np.ndarray(ashape, dtype = adtype, buffer = shm.buf)
    print(shared_weights)
    lock = Lock()
    queue = Queue()
    for i in range(nb_process):
        p = Process(target = f, args=(shm.name, lock, i, queue))
        processes.append(p)

    for p in processes:
        p.start()

    time.sleep(0.7)
    
    for p in processes:
        p.terminate()
    
    time.sleep(1)
    
    print(f"Weights\n{shared_weights}")

    queue.close()
    shm.close()
    shm.unlink()
    
        
