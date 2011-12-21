import bisect
import flight

class Schedule:
    def __init__(self, *args, **kwargs):
        self.flights = []
        if len(args) == 1:
            self._init_file(args[0])
        elif len(args) == 0:
            if 'filename' in kwargs:
                self._init_file(kwargs[filename])
            elif kwargs:
                raise TypeError('Schedule constructor got an unexpected ' \
                        'keyword argument \'%s\'' % kwargs.keys()[0])
            else:
                self.filename = None
        else:
            raise TypeError('Schedule constructor takes 0 or 1 positional ' \
                    'argument (%d given)' % len(args)) 
        self.modified = False

    def _init_file(self, filename):
        infile = open(filename, 'r')
        for line in infile:
            if line:
                self.add(line[:-1])
        infile.close()
        self.filename = filename
    
    def num_flights(self, first=None, before=None, after=None):
        return len(self.get_range(first, after)) # TODO: make more efficient
    
    def get_range(self, index=None, first=None, before=None, after=None):
        # TODO: make WAY more efficient
        result = None
        if first is None:
            result = self.flights[:]
        else:
            result = self.flights[-first:]
    
        if after is not None:
            result = filter(lambda f: f.arr_time >= after, result)
    
        if before is not None:
            result = filter(lambda f: f.dept_time <= before, result)
    
        return result
    
    def get(self, index):
        return self.flights[-(index + 1)]
    
    def add(self, entry):
        if self.flights:
            bisect.insort(self.flights, flight.Flight(entry,
                    context=self.flights[-1].arr_time))
        else:
            bisect.insort(self.flights, flight.Flight(entry))
        self.modified = True

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        outfile = open(filename, 'w')
        for f in self.flights:
            outfile.write(str(f) + '\n')
        outfile.close()
        self.filename = filename
        self.modified = False
