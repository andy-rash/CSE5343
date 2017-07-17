
class NodeBase(object):

    def __init__(self, next=None, prev=None):
        self._next = next
        self._prev = prev

    # Getters

    @property
    def next(self):
        return self._next

    @property
    def prev(self):
        return self._prev

    # Setters

    @next.setter
    def next(self, val):
        self._next = val

    @prev.setter
    def prev(self, val):
        self._prev = val

    # Utility functions

    def __repr__(self):
        return '<NodeBase object>'

class Node(NodeBase):

    def __init__(self, value=None, next=None, prev=None):
        super(Node, self).__init__(next=next, prev=prev)
        self._value = value

    # Getters

    @property
    def value(self):
        return self._value

    # Setters 

    @value.setter
    def value(self, val):
        self._value = val

    # Utitlity functions

    def __repr__(self):
        return '<Node object: %r>' % self._value 

    def __eq__(self, comp):
        return self._next == comp.next()

class List(object):

    def __init__(self):
        self._head = NodeBase() 
        self._size = 0
        self._tail = NodeBase()

        self._head.next = self._tail
        self._tail.prev = self._head

    @property
    def empty(self):
        return self._size == 0

    @property
    def first(self):
        first = self._head.next
        last = self._tail
        return first if first is not last else None 

    @property
    def last(self):
        last = self._tail.prev
        first = self._head
        return last if last is not first else None 

    @property
    def size(self):
        return self._size

    def at(self, loc=0):
        count = 0 
        itr = self.first
        while count < loc and itr != self._tail:
            count += 1
            itr = itr._next

        return itr if isinstance(itr, Node) else None

    def clear(self):
        while self.size > 0:
            self.pop_back()

    def delete(self, val):
        itr = self.find(val)
        if itr is not None:
     
            itr.next.prev = itr.prev
            itr.prev.next = itr.next
            del itr
            self._size -=  1

    def find(self, val): 
        itr = self.first
        while itr != self._tail:

            if itr.value == val:
                break

            itr = itr.next

        return itr if  isinstance(itr, Node) else None

    def insert(self, val, loc=-1):
        if self._size == 0 or loc == -1:
            self.push_back(val)
        elif self._size > 0:
            if loc >= self._size:
                self.push_back(val)
            elif loc < self._size and loc >= 0:
                itr = self.at(loc)
                new_node = Node(value=val, next=itr, prev=itr.prev)
                itr.prev.next = new_node
                itr.prev = new_node
                self._size += 1

    def pop_back(self):
        if self._size > 0:
            last = self.last
            new_last = last.prev

            new_last.next = self._tail
            self._tail.prev = new_last

            del last 
            self._size -= 1

    def pop_front(self):
        if self._size > 0:

            first = self.first
            new_first = first.next

            new_first.prev = self._head
            self._head.next = new_first

            del first
            self._size -= 1

    def push_back(self, value):
        if self._size == 0:
            first = Node(value=value, next=self._tail, prev=self._head)
            self._head.next = first
            self._tail.prev = first

            self._size += 1
        elif self._size > 0:
            
            last = self.last
            new_node = Node(value=value, next=self._tail, prev=last)
            last.next = new_node 
            self._tail.prev = new_node

            self._size += 1

    def push_front(self, value):
        if self._size == 0:
            first = Node(value=value, next=self._tail, prev=self._head)
            self._head.next = first
            self._tail.prev = first

            self._size += 1
        elif self._size > 0:

            first = self.first
            new_node = Node(value=value, next=first, prev=first.prev)
            first.prev = new_node
            self._head.next = new_node
            
            self._size += 1

    def __repr__(self):       
        if not self.size > 0 :
            return ''

        count = 0
        itr = self.first
        rep = ''
        while itr != self._tail:

            if count == 0:
                rep += str(itr.value)
            elif count == self.size - 1:
                rep += ' <-> ' + str(itr.value)
            else:
                rep += ' <-> ' + str(itr.value)

            itr = itr.next
            count += 1

        return rep

