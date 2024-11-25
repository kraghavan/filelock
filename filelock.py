import os
import time

class Timeout(Exception):
    pass

class FileLock:
    def __init__(self, file_path, timeout=10):
        self.file_path = file_path
        self.timeout = timeout
        self.fd = None
        if file_path.endswith('.lock'):
            self.lock_file = file_path
        else:
            self.lock_file = file_path + '.lock'

    def acquire(self):
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
        if self.fd:
            os.close(self.fd)
            os.remove(self.lock_file)
            self.fd = None

    def __enter__(self):
        if not self.acquire():
            return None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()