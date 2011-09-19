import os
import bisect
import re

DEFAULT_NUM_FLIGHTS = 10

# TODO: use files
all_flights = []

def get_num_flights(first=DEFAULT_NUM_FLIGHTS, after=None):
    return len(all_flights[-first:]) # TODO: implement after

def get_flight(n):
    return all_flights[-(n + 1)]

def add_flight(flight):
    bisect.insort(all_flights, Flight(flight))

class Flight:
    def __init__(self, *args, **kwargs):
        arg_names = ('departs', 'dept_time', 'arrives', 'arr_time')
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
                            'the arguments (departs, dept_time, ' +
                            'arrives, arr_time)')

    def _init_str(self, str):
        date = r'\d{1,2}/\d{1,2}(/\d{4})?'
        time = r'\d{1,2}:?\d{2}'
        airport_code = r'[A-Za-z]{3}'
        flight_number = r'\d{2,5}'

        departs = r'(?P<departs>' + airport_code + r')'
        arrives = r'(?P<arrives>' + airport_code + r')'
        dept_date = r'(?P<dept_date>' + date + r')'
        dept_time = r'(?P<dept_time>' + time + r')'
        arr_date = r'(?P<arr_date>' + date + r')'
        arr_time = r'(?P<arr_time>' + time + r')'

        formats = [
            ' '.join((dept_date, departs, dept_time, arrives, arr_time)),
            ' '.join((departs, dept_date, dept_time, arrives, arr_date,
                      arr_time)),
            ' '.join((departs, dept_date, dept_time, arrives, arr_time)),
            ' '.join((dept_date, flight_number, departs, dept_time, arrives,
                      arr_time)),
        ]
        formats = [re.compile(f) for f in formats]

        for format in formats:
            match = format.match(str)
            if match:
                self._init_re(match)
                return
        
        raise ValueError('"%s" doesn\'t match any of the accepted formats.' %
                         str)

    def _init_re(self, match):
        departs = match.group('departs')
        arrives = match.group('arrives')
        dept_time = ' '.join((match.group('dept_date'),
                              match.group('dept_time')))
        try:
            arr_time = ' '.join((match.group('arr_date'),
                                 match.group('arr_time')))
        except IndexError:
            arr_time = ' '.join((match.group('dept_date'),
                                 match.group('arr_time'))) 
        self._init_dept_arr(departs, dept_time, arrives, arr_time)

    def _init_dept_arr(self, departs, dept_time, arrives, arr_time):
        self.departs = departs
        self.dept_time = dept_time
        self.arrives = arrives
        self.arr_time = arr_time
    
    def __str__(self):
        return '%s&ndash;%s departs <b>%s</b> arrives <b>%s</b>' % (
            self.departs,
            self.arrives,
            self.dept_time,
            self.arr_time,
        )
    
    def __repr__(self):
        return "Flight('%s')" % str(self) 
    
    def __cmp__(self, other):
        return cmp(self.dept_time, other.dept_time)
