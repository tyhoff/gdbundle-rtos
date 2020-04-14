import gdb


class ZephyrThread:
    thread_ptr = None
    name = None

    def state(self):
        # Representation of defines from "kernel/include/kernel_structs.h"
        NO_STATE = 0  # Seems like the "idle" thread appears in this state
        PENDING = 1 << 1
        PRESTART = 1 << 2
        DEAD = 1 << 3
        SUSPENDED = 1 << 4
        ABORTING = 1 << 5

        # For Zephyr < 2.2, bit 6 mean a task was ready
        # For 2.2 <= Zephyr < 2.5, bit 6 was used to signify the task was aborted
        #  from an ISR which is only possible in SMP configurations
        #
        # HACK: Since the abort from isr state is unlikely and only existed for
        # a few releases, we'll just assume bit 6 also means "ready".

        LEGACY_READY = 1 << 6
        READY = 1 << 7

        # A "special" state we using to represent "Running" which is the thread which is currently
        # running. Its actual "thread_state" should be READY
        RUNNING = 0xFFFFFFFF

        STATE_NAMES = {
            NO_STATE: "Ready",
            PENDING: "Pending",
            PRESTART: "Prestart",
            DEAD: "Dead",
            SUSPENDED: "Suspended",
            ABORTING: "Aborting",
            READY: "Ready",
            LEGACY_READY: "Ready",
            RUNNING: "Running",
        }

        thread_state_int = int(self.thread_ptr['base']['thread_state'])
        return STATE_NAMES[thread_state_int]
        

    def __init__(self, thread_ptr):
        self.thread_ptr = thread_ptr
        self.name = thread_ptr['name'].string()
    
    def __str__(self):
        return self.name + " (" + self.state() + ")"

class ZephyrThreadList:
    threads = None

    # Accepts a `* k_thread` gdb.Value
    def __init__(self, thread_ptr):
        thread_iter = thread_ptr

        threads = []
        while int(thread_iter) != 0:
            t = ZephyrThread(thread_iter)
            threads.append(t)
            thread_iter = thread_iter['next_thread']

        self.threads = threads

    def __str__(self):
        return str([str(t) for t in self.threads])




class ZephyrThreads(gdb.Command):
    """Prints Hello"""

    def __init__(self):
        super(ZephyrThreads, self).__init__('zephyr_threads', gdb.COMMAND_USER)

    def invoke(self, _unicode_args, _from_tty):
        kernel_threads_kthread_ptr = gdb.parse_and_eval("_kernel.threads")
        z_threads = ZephyrThreadList(kernel_threads_kthread_ptr)
        print(z_threads)
        
        

ZephyrThreads()
