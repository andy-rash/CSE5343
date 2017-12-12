# CSE5343 - Semester Project: CPU Scheduler

Simulate a CPU scheduler using either Shortest Job First (SJF) or Non-preemptive Priority (NPP) Scheduling.

## Environment

It is recommended to install dependencies using [Pipenv](https://github.com/pypa/pipenv), an easy-to-use dependency manager and virtual environment manager for Python.

This project uses Python 2.7. To get started, just clone the repo and run the following commands
```bash
pipenv --two
pipenv install
```

## Usage

Basic usage requires the following command line arguments:
* `-f` (optional) -- path to file with process information (syntax described below)
* `-p` (optional) -- number of processes
* `-a` -- scheduling algorithm to use, either `sjf` for Shortest Job First or `npp` for Non-preemptive Priority

One of either the `-f` option or `-p` option must be provided.

Output is in the form of a table listing the process ID (PID), the burst time, the arrival time, the priority, the completion time, the turn around time, and the waiting time, as well as the average waiting time and turn around time (see examples below).

### File input

File input is the preferred option for process simulation, as the syntax is simple and the process is less arduous than manual entry.

The file syntax follows that of CSV syntax, where the columns are
* process ID (PID)
* arrival time
* burst time
* priority

All values are of integer type.

Comment lines begin with `#`.

#### Example
_res/processes.txt_
```csv
# process_id,arrival_time,burst_time,priority
2760,0,16,1
2750,0,9,2
2740,2,10,3
2730,3,1,1
2720,4,2,4
2710,5,1,4
2700,5,5,2
```

command: `python src/Scheduler.py -f res/processes.txt -a sjf`

![Output](https://i.imgur.com/LOTLBMQ.png)

### Manual input

It's possible to input the process information manually, but this is not recommended as it's tedious and prone to error.

The `-p` flag takes an integer in the range [2,10). After this, the user is prompted for each of the process data values for each of the processes that the user specified with the `-p` flag.

#### Example

command: `python src/Scheduler.py -p 2 -a sjf`

![Output](https://i.imgur.com/OpRDYzK.png)
