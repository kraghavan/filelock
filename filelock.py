import os
import time

class Timeout(Exception):
    pass

class FileLock:
    def __init__(self, file_path, timeout=10):
        """
        Initializes the FileLock instance.

        This method sets up the file lock with the specified file path and timeout.
        It also determines the lock file name based on whether the provided file path
        ends with '.lock'. If it does not, '.lock' is appended to the file path.

        Args:
            file_path (str): The path to the file to be locked.
            timeout (int, optional): The timeout in seconds for acquiring the lock. Defaults to 10.

        Attributes:
            file_path (str): The path to the file to be locked.
            timeout (int): The timeout in seconds for acquiring the lock.
            fd (int or None): The file descriptor for the lock file. Initialized to None.
            lock_file (str): The name of the lock file.
        """
        self.file_path = file_path
        self.timeout = timeout
        self.fd = None
        if file_path.endswith('.lock'):
            self.lock_file = file_path
        else:
            self.lock_file = file_path + '.lock'

    def acquire(self):
        """
        Attempts to acquire the file lock.

        This method tries to create a lock file. If the lock file already exists,
        it will keep trying until the specified timeout is reached. If the lock
        is successfully acquired, it returns True. If the timeout is reached
        without acquiring the lock, it prints a timeout message and returns False.

        Returns:
            bool: True if the lock is successfully acquired, False if the timeout is reached.

        Raises:
            FileExistsError: If the lock file already exists and the timeout is not reached.
        """
        start_time = time.time()
        while True:
            try:
                # Try to create the lock file
                self.fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                break
            except FileExistsError:
                # If the lock file already exists, check the timeout
                if (time.time() - start_time) >= self.timeout:
                    print(f"Timeout occurred while trying to acquire lock on {self.file_path}")
                    return False
                time.sleep(0.1)
        return True

    def release(self):
        """
        Releases the file lock.

        This method closes the file descriptor and removes the lock file if the
        file descriptor is set. It also sets the file descriptor to None.
        """
        if self.fd:
            os.close(self.fd)
            os.remove(self.lock_file)
            self.fd = None

    def __enter__(self):
        """
        Acquires the file lock when entering a with statement.

        This method attempts to acquire the lock by calling the acquire method.
        If the lock is not acquired, it returns None. Otherwise, it returns self.

        Returns:
            FileLock or None: The FileLock instance if the lock is acquired, None otherwise.
        """
        if not self.acquire():
            return None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the file lock when exiting a with statement.

        This method calls the release method to release the lock.
        """
        self.release()