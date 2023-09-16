import tkinter as tk
import threading
import time

from threads import Threads

FILE_DIRECTORY = "./rand_files"
FILENAME_TEMPLATE = "file{}.txt"


def update_labels(threads: 'Threads'):
    threads_label.config(text=f"Current Threads: {threads.current_thread_count}\nDesired Threads: {threads.desired_thread_count}")

def increase_threads(threads: 'Threads'):
    threads.increase_thread_count()
    update_labels(threads)

def decrease_threads(threads: 'Threads'):
    threads.decrease_thread_count()
    update_labels(threads)

def thread_does_things():
    time.sleep(1)
    print("Thread completed.")


threads = Threads(thread_does_things)

root = tk.Tk()
root.title("Thread UI")

threads_label = tk.Label(root, text="")
threads_label.pack()

increase_button = tk.Button(root, text="Increase Threads", command=lambda: increase_threads(threads))
increase_button.pack(side=tk.LEFT)

decrease_button = tk.Button(root, text="Decrease Threads", command=lambda: decrease_threads(threads))
decrease_button.pack(side=tk.RIGHT)


def periodic_update():
    threads.update()
    update_labels(threads)
    root.after(100, periodic_update)

periodic_update()
root.after(100, periodic_update)

root.mainloop()
