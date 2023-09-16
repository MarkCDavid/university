import threading

from context import Context

class Threads:

    def __init__(self: 'Threads', context: 'Context', producer: 'any') -> 'None':
        self._threads = []
        self._context = context;
        self._producer = producer
        self._desired_thread_count = 0

    def increase_thread_count(self: 'Threads',) -> 'None':
        if self._desired_thread_count < 16:
            self._desired_thread_count += 1
        self.update()
    
    def decrease_thread_count(self: 'Threads') -> 'None':
        if self._desired_thread_count > 0:
            self._desired_thread_count -= 1
        self.update()

    def update(self: 'Threads') -> 'None':
        self._remove_threads()

        if self._context.files_to_process == 0:
            return
        
        while self.current_thread_count < self._desired_thread_count:
            self._create_thread()

    @property
    def current_thread_count(self: 'Threads') -> 'int':
        return len(self._threads)
    
    @property
    def desired_thread_count(self: 'Threads') -> 'int':
        return self._desired_thread_count
    
    def _create_thread(self: 'Threads') -> 'None':
        thread = threading.Thread(target=self._producer)
        thread.start()
        self._threads.append(thread)

    def _remove_threads(self: 'Threads') -> 'None':
        self._threads = [thread for thread in self._threads if thread.is_alive()]