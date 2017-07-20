
class PCB(object):
    """ Class representing a process control block (PCB). """

    def __init__(self, iterable=(), state=000, **kwargs): 
        """
        Constructor
        
            - creates new PCB object.
            - ex. :
                obj = PCB(dict(arrival=1, burst=16, pid=2760,
                               priority=1, state=000))

        Parameters
        ----------
        iterable : iterable
            - works to iterate through given keyword args
        **kwargs : dict
            - dictionary of initialization information
            - except where otherwise noted, the below options must be
              included for proper function
            - options:
                * arrival
                * burst
                * pid
                * priority
                * (optional) state

        """

        # set of all acceptable options
        self.__accepted = set(['arrival', 'burst', 'pid',
                               'priority', 'state'])

        # dictionary of all possible states
        self.__states = {000: 'new',
                         001: 'ready',
                         010: 'running',
                         011: 'waiting',
                         100: 'terminated'}
        self._state = state

        # set class attributes, with proper exception handling 
        for k,v in iterable.iteritems():
            if k == 'state':
                if v not in self.__states.keys():
                    raise KeyError('given state invalid')
            if k not in self.__accepted:
                raise ValueError('given variable not acceptable')
            setattr(self, '_'+k, v)

        # make sure that all options have been passed,
        # else, raise an exception
        for item in self.__accepted:
            if item == 'state':
                continue
            if '_'+item not in self.__dict__.keys():
                raise RuntimeError('incomplete PCB values')

    @property
    def arrival(self):
        """ Return process arrival time. """
        return self._arrival if self._arrival else None

    @property
    def burst(self):
        """ Return process burst time. """
        return self._burst if self._burst else None

    @property
    def pid(self):
        """ Return process id (PID). """
        return self._pid if self._pid else None

    @property
    def priority(self):
        """ Return process priority. """
        return self._priority if self._priority else None

    @property
    def state(self):
        """ Return current process state. """
        return self._state if self._state else None

    @state.setter
    def state(self, new_st):
        """ Set new state for a process. """
        if new_st in self.__states.keys():
            self._state = self.__states[new_st]

    def __eq__(self, comp):
        """ Compare equality of two PCBs. """
        return self._pid == comp.pid

    def __ge__(self, comp):
        """ Check greater than or equal to. """
        return not self.__lt__(comp)

    def __gt__(self, comp):
        """ Check greater than. """
        return self._pid > comp.pid

    def __le__(self, comp):
        """ Check less than or equal to. """
        return not self.__gt__(comp)

    def __lt__(self, comp):
        """ Check less than. """
        return self._pid < comp.pid

    def __ne__(self, comp):
        """ Compare inequality of two PCBs. """
        return not self.__eq__(comp)

    def __repr__(self):
        """ Return representation of PCB. """
        return '<PCB PID=%r state=%r>' % (self._pid, self._state)

    def __str__(self):
        """ Return string representation of PCB. """
        return str(self._pid)

