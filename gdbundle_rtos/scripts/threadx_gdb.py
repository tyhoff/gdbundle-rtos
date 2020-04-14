import gdb


class ThreadXThread:
    thread_ptr = None
    name = None

    def state(self):
        # From tx_api.h
        TX_READY = 0
        TX_COMPLETED = 1
        TX_TERMINATED = 2
        TX_SUSPENDED = 3
        TX_SLEEP = 4
        TX_QUEUE_SUSP = 5
        TX_SEMAPHORE_SUSP = 6
        TX_EVENT_FLAG = 7
        TX_BLOCK_MEMORY = 8
        TX_BYTE_MEMORY = 9
        TX_IO_DRIVER = 10
        TX_FILE = 11
        TX_TCP_IP = 12
        TX_MUTEX_SUSP = 13
        # NOTE: Pseudo state ... not sure if a 'Ready' thread is always 'Running'
        TX_RUNNING = 0xFFFF
        TX_UNKNOWN = None

        STATE_NAMES = {
            TX_RUNNING: "Running",
            TX_READY: "Ready",
            TX_COMPLETED: "Completed",
            TX_TERMINATED: "Terminated",
            TX_SUSPENDED: "Suspended",
            TX_SLEEP: "Sleeping",
            TX_QUEUE_SUSP: "Waiting on Queue",
            TX_SEMAPHORE_SUSP: "Waiting on Semaphore",
            TX_EVENT_FLAG: "Waiting on Event Flag",
            TX_BLOCK_MEMORY: "Waiting on block pool",
            TX_BYTE_MEMORY: "Waiting on byte pool",
            TX_IO_DRIVER: "Waiting on I/O",
            TX_FILE: "Waiting on FileX",
            TX_TCP_IP: "Waiting on NetX",
            TX_MUTEX_SUSP: "Waiting on Mutex",
            TX_UNKNOWN: "Unknown",
        }

        thread_state_int = int(self.thread_ptr['tx_thread_state'])
        return STATE_NAMES[thread_state_int]
        

    def __init__(self, thread_ptr):
        self.thread_ptr = thread_ptr

        self.name = thread_ptr['tx_thread_name'].string()
    
    def __str__(self):
        return self.name + " (" + self.state() + ")"


class ThreadXMutex:
    mutex_ptr = None
    name = None

    def __init__(self, mutex_ptr):
        self.mutex_ptr = mutex_ptr
        self.name = mutex_ptr['tx_mutex_name'].string()
        self.owner = mutex_ptr['tx_mutex_owner']
    
    def __str__(self):
        return self.name + " (owner=" + str(self.owner) + ")"


class ThreadXThreadList:
    threads = None

    # Accepts a `* k_thread` gdb.Value
    def __init__(self, thread_ptr):
        thread_iter = thread_ptr

        threads = []
        while True:
            t = ThreadXThread(thread_iter)
            threads.append(t)
            thread_iter = thread_iter['tx_thread_created_next']
            if thread_iter == thread_ptr:
                break

        self.threads = threads

    def __str__(self):
        return str([str(t) for t in self.threads])


class ThreadXMutexList:
    mutexes = None

    # Accepts a `* k_thread` gdb.Value
    def __init__(self, mutex_ptr):
        it = mutex_ptr

        mutexes = []
        while True:

            t = ThreadXMutex(it)
            mutexes.append(t)
            
            it = it['tx_mutex_created_next']
            if it == mutex_ptr:
                break

        self.mutexes = mutexes

    def __str__(self):
        return str([str(t) for t in self.mutexes])


class ThreadXThreads(gdb.Command):
    """Prints Hello"""

    def __init__(self):
        super(ThreadXThreads, self).__init__('tx_threads', gdb.COMMAND_USER)

    def invoke(self, _unicode_args, _from_tty):
        thread_list_ptr = gdb.parse_and_eval("_tx_thread_created_ptr")
        threads = ThreadXThreadList(thread_list_ptr)
        print(threads)

class ThreadXMutexes(gdb.Command):
    """Prints Hello"""

    def __init__(self):
        super(ThreadXMutexes, self).__init__('tx_mutexes', gdb.COMMAND_USER)

    def invoke(self, _unicode_args, _from_tty):
        mutex_list_ptr = gdb.parse_and_eval("(TX_MUTEX *)_tx_mutex_created_ptr")
        mutexes = ThreadXMutexList(mutex_list_ptr)
        print(mutexes)
        
        

ThreadXThreads()
ThreadXMutexes()
