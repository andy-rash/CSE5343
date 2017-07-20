
class NodeBase(object):
    """ Class representing the basic idea of a node in the list. """

    def __init__(self, next=None, prev=None):
        """
        Constructor

            - creates a new NodeBase object.
            - the only objects in the List that are solely NodeBase objects
              are the head and tail of the List.
            - in actual use, `next` and `prev` are usually not
              passed to the object on creation, but rather they're set
              using the respective setter methods
            - ex. :
                obj = NodeBase()

        Parameters
        ----------
        next : NodeBase
            - points to the next item in the List
        prev : NodeBase
            - points to the previous item in the List

        """
        self._next = next
        self._prev = prev

    @property
    def next(self):
        """ Return next NodeBase in List. """
        return self._next

    @property
    def prev(self):
        """ Return previous NodeBase in List. """
        return self._prev

    @next.setter
    def next(self, val):
        """ Set next NodeBase in List. """
        self._next = val

    @prev.setter
    def prev(self, val):
        """ Set previous NodeBase in List. """
        self._prev = val

    def __repr__(self):
        """ Return representation of NodeBase. """
        return '<NodeBase object>'

class Node(NodeBase):
    """ Class representing a true node in the list. """

    def __init__(self, value=None, next=None, prev=None):
        """
        Constructor

            - creates new Node object.
            - differs from NodeBase object in that it actually encapsulates
              data.
            - ex. where itr is a "pointer" to a Node found in the list:
                obj = Node(value=val, next=itr, prev=itr.prev)

        Parameters
        ----------
        value : <variable type>
            - value encapsulated by the Node.
        next : (Node|NodeBase)
            - "pointer" to the next Node in the List.    
            - points to Node when not near head or tail of List and
              points to NodeBase when in contact with head or tail of List
        prev : (Node|NodeBase)
            - "pointer" to the previous Node in the List.    
            - points to Node when not near head or tail of List and
              points to NodeBase when in contact with head or tail of List

        """
        super(Node, self).__init__(next=next, prev=prev)
        self._value = value

    @property
    def value(self):
        """ Return value encapsulated in Node. """
        return self._value

    @value.setter
    def value(self, val):
        """ Set value to be encapsulated by Node. """
        self._value = val

    def __repr__(self):
        """ Return representation of Node. """
        return '<Node object: %r>' % self._value 

    def __eq__(self, comp):
        """ Compare equality of two Nodes. """
        return self._next == comp.next and \
               self._prev == comp.prev and \
               self._value == comp.value

    def __ge__(self, comp):
        """ Check greater than or equal to. """
        return not self.__lt__(comp)

    def __gt__(self, comp):
        """ Check greater than. """
        return self._value > comp.value

    def __le__(self, comp):
        """ Check less than or equal to. """
        return not self.__gt__(comp)

    def __lt__(self, comp):
        """ Check less than. """
        return self._value < comp.value

    def __ne__(self, comp):
        """ Compare inequality of two Nodes. """
        return not self.__eq__(comp)

class List(object):
    """ Class implementing the linked list. """

    def __init__(self):
        """
        Constructor

            - creates new List object.
            - Lists are doubly-linked lists.
            - ex. :
                obj = List()

        """
        self._curr = None
        self._head = NodeBase() 
        self._itr = 0
        self._size = 0
        self._tail = NodeBase()

        self._head.next = self._tail
        self._tail.prev = self._head

    def __iter__(self):
        return self

    def at(self, loc=0):
        """ Return the Node at a given position in the List. """
        count = 0 
        itr = self.first
        while count < loc and itr.next is not None:
            count += 1
            itr = itr._next

        return itr if isinstance(itr, Node) else None

    def clear(self):
        """ Clear all items in the List. """
        while self.size > 0:
            self.pop_back()

    def delete(self, val):
        """ Delete the first instance of a given value. """
        itr = self.find(val)
        if itr is not None: 
            itr.next.prev = itr.prev
            itr.prev.next = itr.next
            self._size -=  1

    @property
    def empty(self):
        """ Return whether the List is empty. """
        return self._size == 0

    def find(self, val): 
        """ Find the first instance of a given value. """
        for item in self:
            if item.value == val:
                return item
        return None

    @property
    def first(self):
        """ Return the first Node in the List. """
        first = self._head.next
        last = self._tail
        return first if first is not last else None

    def insert(self, val, loc=-1):
        """ Insert a value into a given location in the List. """
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

    @property
    def last(self):
        """ Return the last Node in the List. """
        last = self._tail.prev
        first = self._head
        return last if last is not first else None

    def next(self):
        """ Return the next item for built-in iterable. """
        if self._curr is None:
            self._curr = self.first

        if self._itr < self._size:
            itr = self._curr
            self._curr = itr.next
            self._itr += 1
            return itr
        else:
            self._curr = None
            self._itr = 0
            raise StopIteration()

    def pop_back(self):
        """ Pop the last item from the List. """
        if self._size > 0:
            last = self.last
            new_last = last.prev

            new_last.next = self._tail
            self._tail.prev = new_last

            self._size -= 1

    def pop_front(self):
        """ Pop the first item from the List. """
        if self._size > 0:

            first = self.first
            new_first = first.next

            new_first.prev = self._head
            self._head.next = new_first

            self._size -= 1

    def push_back(self, value):
        """ Insert value at the tail of the List. """
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
        """ Insert value at the head of the List. """
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

    def sort(self):
        """ Sort the List. """
        l = sorted(self)
        self.clear()
        for item in l:
            self.push_back(item.value)

    @property
    def size(self):
        """ Return the size of the List. """
        return self._size
 
    def __repr__(self): 
        """ Return representation of List. """
        if not self.size > 0:
            return ''

        count = 0
        rep = ''
        for item in self:
            if count == 0:
                rep += str(item.value)
            elif count == self.size - 1:
                rep += ' <-> ' + str(item.value)
            else:
                rep += ' <-> ' + str(item.value)

            count += 1

        return rep

