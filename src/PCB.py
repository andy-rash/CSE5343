
class PCB(object):

    def __init__(self, pid):
        self._pid = pid

    def __repr__(self):
        return '<PCB PID=%r>' % self._pid

l = PCB(2470)
print l
