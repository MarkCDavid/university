import os
import threading
from queue import Queue


class Context:
    
    def __init__(self: 'Context', directory: 'str') -> 'None':
        self._queue = self._get_files(directory)
        
        self.total_files = self._queue.qsize()
        
        self._smallest_prime = None
        self._smallest_prime_lock = threading.Lock()
        
        self._largest_prime = None
        self._largest_prime_lock = threading.Lock()

    def next_file(self: 'Context') -> 'str':
        return self._queue.get()
    
    def update_smallest_prime(self: 'Context', value: 'int') -> 'None':
        with self._smallest_prime_lock:
            if self._smallest_prime > value:
                self._smallest_prime = value
    
    def update_largest_prime(self: 'Context', value: 'int') -> 'None':
        with self._largest_prime_lock:
            if self._largest_prime < value:
                self._largest_prime = value
    
    @property
    def smallest_prime(self: 'Context') -> 'int | None':
        with self._smallest_prime_lock:
            return self._smallest_prime
    
    @property
    def largest_prime(self: 'Context') -> 'int | None':
        with self._largest_prime_lock:
            return self._largest_prime
    
    @property
    def files_processed(self: 'Context') -> 'int':
        return self.total_files - self._queue.qsize()
    
    @property
    def files_to_process(self: 'Context') -> 'int':
        return self._queue.qsize()

    def _get_files(self: 'Context', path: 'str') -> 'Queue[str]':
        queue = Queue()
        for filename in os.listdir(path):
            queue.put(filename)
        return queue

