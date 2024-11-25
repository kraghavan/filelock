import random
import time
import threading
import os
from filelock import FileLock

SLEEP_TIME = int(os.getenv("SLEEP_TIME", 10))
CHANCE_TO_ACQUIRE = int(os.getenv("CHANCE_TO_ACQUIRE", 2))

class Acquirer:
    def __init__(self, names):
        """
        Initializes the Acquirer instance.

        This method sets up the Acquirer with a list of thread names and initializes
        a threading event to signal when to stop the threads.

        Args:
            names (list): A list of thread names.

        Attributes:
            names (list): The list of thread names.
            stop_event (threading.Event): An event to signal when to stop the threads.
        """
        self.names = names
        self.stop_event = threading.Event()

    def acquire_lock(self, name, file_lock):
        """
        Attempts to acquire the file lock for a thread.

        This method generates a random number and checks if it is divisible by
        CHANCE_TO_ACQUIRE. If it is, the thread attempts to acquire the lock.
        If the lock is acquired, the thread sleeps for SLEEP_TIME. If the lock
        is already held, a message is printed.

        Args:
            name (str): The name of the thread.
            file_lock (str): The path to the lock file.
        """
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
        """
        Starts the threads and handles their termination.

        This method creates and starts threads for each name in the names list.
        Each thread attempts to acquire the lock by calling the acquire_lock method.
        The method also handles the termination of threads on a keyboard interrupt.

        Args:
            file_lock (str): The path to the lock file.
        """
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
    # Create an Acquirer instance and start the threads
    file_lock = 'example.lock'
    names = ["Thread1", "Thread2", "Thread3"]
    acquirer = Acquirer(names)
    # Start the threads
    acquirer.start_threads(file_lock)