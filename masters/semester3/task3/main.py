import os
import prime
import tkinter as tk

from context import Context
from threads import Threads

def update_labels(threads: 'Threads', context: 'Context'):
    threads_label.config(text=f"Current Threads: {threads.current_thread_count}\nDesired Threads: {threads._desired_thread_count}")
    files_to_process_label.config(text=f"Files to Process: {context.files_to_process}")
    files_processed_label.config(text=f"Files Processed: {context.files_processed}")
    smallest_prime_label.config(text=f"Smallest Prime Found: {context.smallest_prime}")
    largest_prime_label.config(text=f"Largest Prime Found: {context.largest_prime}")

def increase_threads(threads: 'Threads', context: 'Context'):
    threads.increase_thread_count()
    update_labels(threads, context)

def decrease_threads(threads: 'Threads', context: 'Context'):
    threads.decrease_thread_count()
    update_labels(threads, context)

def process_file(context: 'Context'):
    if context.files_to_process == 0:
        return
    
    file_path = os.path.join(FILE_DIRECTORY, context.next_file())
    primes = []
    with open(file_path, "r") as primes_file:
        numbers = [
            int(number) 
            for number 
            in primes_file.readlines()
        ]
        for number in numbers:
            if prime.is_prime(number):
                primes.append(number)
    
    if len(primes) == 0:
        return
    
    min_prime, max_prime = min(primes), max(primes)
    context.update_smallest_prime(min_prime)
    context.update_largest_prime(max_prime)


FILE_DIRECTORY = "./rand_files"
context = Context(FILE_DIRECTORY)
threads = Threads(context, lambda: process_file(context))

root = tk.Tk()
root.title("Thread UI")

files_to_process_label = tk.Label(root, text="Files to Process:")
files_to_process_label.pack()

files_processed_label = tk.Label(root, text="Files Processed:")
files_processed_label.pack()

largest_prime_label = tk.Label(root, text="Largest Prime Found:")
largest_prime_label.pack()


smallest_prime_label = tk.Label(root, text="Smallest Prime Found:")
smallest_prime_label.pack()

threads_label = tk.Label(root, text="")
threads_label.pack()

increase_button = tk.Button(root, text="Increase Threads", command=lambda: increase_threads(threads, context))
increase_button.pack(side=tk.LEFT)

decrease_button = tk.Button(root, text="Decrease Threads", command=lambda: decrease_threads(threads, context))
decrease_button.pack(side=tk.RIGHT)

def update():
    threads.update()
    update_labels(threads, context)
    root.after(50, update)

root.after(0, update)
root.mainloop()
