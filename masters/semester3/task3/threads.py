import threading

class Threads:

    def __init__(self: 'Threads', producer: 'any') -> 'None':
        self.threads = []
        self.producer = producer
        self.desired_thread_count = 0

    def increase_thread_count(self: 'Threads') -> 'None':
        if self.desired_thread_count < 16:
            self.desired_thread_count += 1
        self.update()
    
    def decrease_thread_count(self: 'Threads') -> 'None':
        if self.desired_thread_count > 0:
            self.desired_thread_count -= 1
        self.update()

    def update(self: 'Threads') -> 'None':
        self._remove_threads()
        while self.current_thread_count < self.desired_thread_count:
            self._create_thread()

    @property
    def current_thread_count(self: 'Threads') -> 'int':
        return len(self.threads)
    
    def _create_thread(self: 'Threads') -> 'None':
        thread = threading.Thread(target=self.producer)
        thread.start()
        self.threads.append(thread)

    def _remove_threads(self: 'Threads') -> 'None':
        self.threads = [thread for thread in self.threads if thread.is_alive()]