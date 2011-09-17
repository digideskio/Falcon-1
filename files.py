import os
import bisect

DEFAULT_NUM_FLIGHTS = 10

# TODO: use files
all_flights = []

def get_flights(first=DEFAULT_NUM_FLIGHTS, after=None):
    return reversed(all_flights[-first:]) # TODO: implement after

def get_flight(n):
    return all_flights[-(n + 1)]

def add_flight(flight):
    bisect.insort(all_flights, Flight(flight))

class Flight:
    def __init__(self, *args, **kwargs):
        arg_names = ('date', 'departs', 'dept_time', 'arrives', 'arr_time')
        if len(args) == 1:
            self._init_str(args[0])
        elif 'str' in kwargs:
            self._init_str(kwargs['str'])
        elif len(args) == 4:
            self._init_arr_dept(*args)
        elif reduce(lambda x, y: x and y, 
                    [(name in kwargs) for name in arg_names]):
            self._init_arr_dept(**kwargs)
        else:
            raise TypeError('Flight constructor takes either a string or ' +
                            'the arguments (date, departs, dept_time, ' +
                            'arrives, arr_time)')

    def _init_str(self, str):
        (
            self.date,
            self.departs, 
            self.dept_time, 
            self.arrives, 
            self.arr_time,
        ) = str.split(' ') # TODO: make this a lot more robust
        
    def _init_dept_arr(self, departs, dept_time, arrives, arr_time):
        self.departs = departs
        self.dept_time = dept_time
        self.arrives = arrives
        self.arr_time = arr_time
    
    def __str__(self):
        return '%s %s %s %s %s' % (
            self.date,
            self.departs, 
            self.dept_time, 
            self.arrives, 
            self.arr_time
        )
    
    def __repr__(self):
        return "Flight('%s')" % str(self) 
    
    def __cmp__(self, other):
        return cmp(self.date, other.date) or \
               cmp(self.dept_time, other.dept_time)
