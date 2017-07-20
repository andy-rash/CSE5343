import argparse
import re
from List import List
from PCB import PCB

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

class Scheduler(object):

    def __init__(self):
        super(Scheduler, self).__init__()
        self._ready = List()
        self._waiting = List()

if __name__ == '__main__':

    processes = []

    if __args__.processes:
        try:
            num_processes = int(vars(__args__)['processes'][0])
        except ValueError:
            __parser__.error('Number of processes must be an integer.')

        if num_processes <= 1:
            raise RuntimeError('Must have number of processes > 1.')
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
                    
# Example of finding a PCB in the List structure
#    it = l.find(2760, lambda x,y: x.pid == y)
#    print it.value

