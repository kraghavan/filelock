import random
import time
import threading
import os
from filelock import FileLock

SLEEP_TIME = int(os.getenv("SLEEP_TIME", 10))
CHANCE_TO_ACQUIRE = int(os.getenv("CHANCE_TO_ACQUIRE", 2))

class Acquirer:
    def __init__(self, names):
        self.names = names
        self.stop_event = threading.Event()

    def acquire_lock(self, name, file_lock):
        while not self.stop_event.is_set():
            # Generate a random integer between 1 and 25
            random_number = random.randint(1, 25)
            
            # Check if the random number is divisible by CHANCE_TO_ACQUIRE
            if (random_number % CHANCE_TO_ACQUIRE) == 0:
                lock_acquired = False
                try:
                    with FileLock(file_lock, timeout=0):
                        print(f"{name} acquired the lock with random number: {random_number}")
                        lock_acquired = True
                        # Sleep outside the lock to allow other threads to acquire the lock
                        time.sleep(SLEEP_TIME)
                except TimeoutError:
                    pass  # This should not happen with timeout=0
                
                if not lock_acquired:
                    print(f"{name} attempted to acquire the lock but it was already held. Random number: {random_number}")
            else:
                print(f"{name} did not qualify to acquire the lock. Random number: {random_number}")
            
            time.sleep(1)

    def start_threads(self, file_lock):
        threads = []
        for name in self.names:
            thread = threading.Thread(target=self.acquire_lock, args=(name, file_lock))
            thread.start()
            threads.append(thread)
        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print("Terminating threads...")
            self.stop_event.set()
            for thread in threads:
                thread.join()

if __name__ == "__main__":
    file_lock = 'example.lock'
    names = ["Thread1", "Thread2", "Thread3"]
    acquirer = Acquirer(names)
    acquirer.start_threads(file_lock)