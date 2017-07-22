import argparse
import re
from List import List
from PCB import PCB
from tabulate import tabulate

__parser__ = argparse.ArgumentParser('Simulate a CPU scheduler using either Shortest Job First (SJF) or Non-preemptive Priority Scheduling.')
__parser__.add_argument('-f', '--file',
                        type=argparse.FileType('r'))
__parser__.add_argument('-p', '--processes',
                        nargs=1)
__parser__.add_argument('-a', '--algorithm',
                        nargs=1, metavar='(sjf|npp)')
__args__ = __parser__.parse_args()

if __args__.file and __args__.processes:
    __parser__.error('Must provide either file with process data or number of processes to be entered manually.')
if not __args__.file and not __args__.processes:
    __parser__.error('Must provide either file with process data or number of processes to be entered manually.')
if not __args__.algorithm:
    __parser__.error('Must provide type of scheduling algorithm to be used.')
if vars(__args__)['algorithm'][0] != 'sjf' and \
   vars(__args__)['algorithm'][0] != 'npp':
    __parser__.error('Invalid scheduling algorithm. Must be one of: sjf or npp.')

class NPP(object):

    def __init__(self, processes=[]):
        super(NPP, self).__init__()
        self._complete = List()
        self._processes = processes
        self._ready = List()
        self._waiting = List()

        self._processes = sorted(self._processes, key=lambda x: x.arrival)
        for process in self._processes:
            process.state = 011
            self._waiting.push_back(process)

    def output(self):
        """ Output information gathered from running scheduler. """
        self._complete.sort(key=lambda x: (x.value.priority, x.value.pid))

        headers = ['PID', 'Burst Time', 'Arrival Time',
                   'Priority', 'Completion Time', 'Turn Around Time',
                   'Waiting Time']

        
        avg_turn_around = sum(c.value.turn_around for c in self._complete) / \
                          (self._complete.size * 1.0)
        avg_wait = sum(c.value.waiting for c in self._complete) / \
                   (self._complete.size * 1.0)
        
        data = [[x.value.pid, x.value.burst, x.value.arrival, \
                 x.value.priority, x.value.completion, x.value.turn_around, \
                 x.value.waiting] for x in self._complete] 
       
        print 'Non-Preemptive Priority (NPP)'
        print tabulate(data, headers=headers, tablefmt='orgtbl') 
        print 'Avg. Turn Around Time: ', avg_turn_around
        print 'Avg. Waiting Time: ', avg_wait

    def run(self): 
        """ Run the scheduling algorithm. """
        active_process = None
        system_time = 0
        total_time = sum(c.burst for c in self._processes)
        while system_time <= total_time:
            
            for proc in self._waiting:
                if proc.value.arrival == system_time:
                    if proc.value.state != 001:
                        proc.value.state = 001
                        self._ready.push_back(proc.value)

            # this is the essence of NPP: sorting by priority
            # change to sort by burst-time for SJF
            self._ready.sort(key=lambda x: x.value.priority)

            if active_process is None:
                if self._ready.size > 0:
                    active_process = self._ready.first.value
                    active_process.start = system_time
                    self._ready.pop_front()
                else:
                    total_time += 1
            else:
                if active_process.start + active_process.burst == system_time:
                    # update ending process's timing info
                    active_process.completion = system_time
                    active_process.turn_around = system_time - active_process.arrival
                    active_process.waiting = active_process.start - active_process.arrival

                    # end the process by changing state and pushing
                    # process into 'complete' queue
                    active_process.state = 100
                    self._complete.push_back(active_process)

                    # set new active process
                    if self._ready.size > 0:
                        active_process = self._ready.first.value
                        active_process.start = system_time
                        self._ready.pop_front()

            # print out an "execution trace"
            # make sure that self.output() is not called simultaneously
#            print system_time, repr(active_process)

            system_time += 1

class SJF(object):

    def __init__(self, processes=[]):
        super(SJF, self).__init__()
        self._complete = List()
        self._processes = processes
        self._ready = List()
        self._waiting = List()

        self._processes = sorted(self._processes, key=lambda x: x.arrival)
        for process in self._processes:
            process.state = 011
            self._waiting.push_back(process)

    def output(self):
        """ Output information gathered from running scheduler. """
        self._complete.sort(key=lambda x: (x.value.burst, x.value.pid))

        headers = ['PID', 'Burst Time', 'Arrival Time',
                   'Priority', 'Completion Time', 'Turn Around Time',
                   'Waiting Time']

        
        avg_turn_around = sum(c.value.turn_around for c in self._complete) / \
                          (self._complete.size * 1.0)
        avg_wait = sum(c.value.waiting for c in self._complete) / \
                   (self._complete.size * 1.0)
        
        data = [[x.value.pid, x.value.burst, x.value.arrival, \
                 x.value.priority, x.value.completion, x.value.turn_around, \
                 x.value.waiting] for x in self._complete] 
       
        print 'Shortest Job First (SJF)'
        print tabulate(data, headers=headers, tablefmt='orgtbl') 
        print 'Avg. Turn Around Time: ', avg_turn_around
        print 'Avg. Waiting Time: ', avg_wait

    def run(self): 
        """ Run the scheduling algorithm. """
        active_process = None
        system_time = 0
        total_time = sum(c.burst for c in self._processes)
        while system_time <= total_time:
            
            for proc in self._waiting:
                if proc.value.arrival == system_time:
                    if proc.value.state != 001:
                        proc.value.state = 001
                        self._ready.push_back(proc.value)

            # this is the essence of SJF: sorting by burst-time
            # change to sort by priority for NPP
            self._ready.sort(key=lambda x: x.value.burst)

            if active_process is None:
                if self._ready.size > 0:
                    active_process = self._ready.first.value
                    active_process.start = system_time
                    self._ready.pop_front()
                else:
                    total_time += 1
            else:
                if active_process.start + active_process.burst == system_time:
                    # update ending process's timing info
                    active_process.completion = system_time
                    active_process.turn_around = system_time - active_process.arrival
                    active_process.waiting = active_process.start - active_process.arrival

                    # end the process by changing state and pushing
                    # process into 'complete' queue
                    active_process.state = 100
                    self._complete.push_back(active_process)

                    # set new active process
                    if self._ready.size > 0:
                        active_process = self._ready.first.value
                        active_process.start = system_time
                        self._ready.pop_front()

            # print out an "execution trace"
            # make sure that self.output() is not called simultaneously
#            print system_time, repr(active_process)
            
            system_time += 1

if __name__ == '__main__':

    processes = []

    if __args__.processes:
        try:
            num_processes = int(vars(__args__)['processes'][0])
        except ValueError:
            __parser__.error('Number of processes must be an integer.')

        if num_processes < 1:
            raise RuntimeError('Must have number of processes >= 1.')
        if num_processes > 10:
            raise RuntimeError('Number of user-entered processes limited to 10.')

        count = 1
        while num_processes > 0:
            print 'Process #', count 
            print '----------'

            _pid = raw_input('Enter a PID: ')
            _arrival = raw_input('Enter an arrival time: ')
            _burst = raw_input('Enter a burst time: ')
            _priority = raw_input('Enter a priority: ')
            try:
                _pid = int(_pid)
                _arrival = int(_arrival)
                _burst = int(_burst)
                _priority = int(_priority)
            except ValueError:
                raise RuntimeError('Given values must be integers.') 

            print ''

            processes.append(PCB(dict(pid=_pid, arrival=_arrival,
                                      burst=_burst, priority=_priority)))

            count += 1
            num_processes -= 1

    if __args__.file:
        
        filename = __args__.file.name 
        PROCESS_REGEX = re.compile('[\d]+,[\d]+,[\d]+,[\d]+')
        with open(filename, 'r') as f:
            for line in f:
                if PROCESS_REGEX.match(line):
                    info = line.strip().split(',')
                    processes.append(PCB(dict(pid=info[0], arrival=info[1],
                                         burst=info[2], priority=info[3])))

        if len(processes) < 1:
            raise RuntimeError('No processes created from given file.')

    if __args__.algorithm:
        algo = vars(__args__)['algorithm'][0]

        if algo == 'sjf':
            sched = SJF(processes=processes)
            sched.run()

            sched.output() 

        elif algo == 'npp':
            sched = NPP(processes=processes)
            sched.run()

            sched.output()

