# File Lock and Acquirer

This project demonstrates how to handle file locking in Python to prevent multiple processes or threads from accessing the same file simultaneously. It includes two main components: the `FileLock` class and the `Acquirer` class.

## FileLock Class

The `FileLock` class is used to create and manage file locks. It ensures that only one process or thread can hold the lock at a time.

### Usage

```python
from filelock import FileLock, Timeout

# Create a FileLock instance
file_lock = FileLock("example", timeout=5)

try:
    with file_lock:
        print("Lock acquired")
        # Perform operations while the lock is held
        time.sleep(10)
except Timeout as e:
    print(e)

## Acquirer Class

The `Acquirer` class demonstrates how to use the `FileLock` class in a multi-threaded environment. Each thread attempts to acquire the lock based on a random number.

### Usage

```python
from acquirer import Acquirer

# List of thread names
names = ["Thread1", "Thread2", "Thread3"]

# Create an Acquirer instance
acquirer = Acquirer(names)

# Start the threads
acquirer.start_threads("example.lock")