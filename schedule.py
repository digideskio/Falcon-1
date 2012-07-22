import bisect
import flight


class Schedule:
    def __init__(self, *args, **kwargs):
        self.flights = []
        if len(args) == 1:
            self._init_file(args[0])
        elif len(args) == 0:
            if 'filename' in kwargs:
                self._init_file(kwargs['filename'])
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
                self.add(flight.from_line(line[:-1],
                                          context=self.context()))
        infile.close()
        self.filename = filename

    def num_flights(self, first=None, before=None, after=None):
        # TODO: make more efficient
        return len(self.get_range(first, after))

    def get_range(self, index=None, first=None, before=None, after=None):
        # TODO: make WAY more efficient
        result = None
        if first is None:
            result = self.flights[:]
        else:
            result = self.flights[-first:]

        if after is not None:
            result = [f for f in result if f.arr_time >= after]

        if before is not None:
            result = [f for f in result if f.dept_time <= before]

        return result

    def get(self, index):
        return self.flights[-(index + 1)]

    def remove(self, index):
        del self.flights[-(index + 1)]
        self.modified = True

    def add(self, entry):
        bisect.insort(self.flights, entry)
        entry.add_listener(self)
        self.modified = True

    def context(self):
        if self.flights:
            return self.get(0).arr_time
        else:
            return None

    def update(self, _entry):
        self.flights.sort()
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
