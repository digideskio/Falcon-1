import os.path

import pytz

DATA_PATH = os.path.join(os.path.expanduser('~'), '.falcon')
AIRPORTS_NAME = 'airports.txt'
AIRPORTS_PATH = os.path.join(DATA_PATH, AIRPORTS_NAME)


class FileError(Exception):
    pass


def check_file(name):
    if os.path.isfile(name):
        return

    dirname = os.path.dirname(name)
    if os.path.isdir(dirname):
        if os.path.exists(name):
            raise FileError(name + ' already exists and is not a ' +
                            'file.  Cannot create data files.')
        else:
            touch(name)
    elif os.path.exists(dirname):
        raise FileError(dirname + ' already exists and is not a directory.' +
                        '  Cannot create data files.')
    else:
        os.mkdir(dirname)
        touch(name)


def touch(name):
    touched = open(name, 'w')
    touched.close()

all_airports = {}


def load_airports():
    if not os.path.isfile(AIRPORTS_PATH):
        return

    airports_file = open(AIRPORTS_PATH, 'r')
    for line in airports_file:
        airport = Airport(line[:-1])
        all_airports[airport.code] = airport
    airports_file.close()


def save_airports():
    check_file(AIRPORTS_PATH)
    airports_file = open(AIRPORTS_PATH, 'w')
    for airport_id in all_airports:
        airports_file.write(all_airports[airport_id].line() + '\n')
    airports_file.close()


def add_airport(airport):
    all_airports[airport.code] = airport
    save_airports()


class Airport:
    def __init__(self, *args, **kwargs):
        arg_names = ('code', 'timezone')
        if len(args) == 1:
            self._init_line(args[0])
        elif 'line' in kwargs:
            self._init_line(kwargs['line'])
        elif len(args) == len(arg_names):
            self._init_args(*args)
        elif reduce(lambda x, y: x and y,
                    [(name in kwargs) for name in arg_names]):
            self._init_args(**kwargs)
        else:
            raise TypeError('Airport constructor takes either a string or ' +
                            'the arguments (code, timezone)')

    def _init_line(self, line):
        self._init_args(*line.split(' '))

    def _init_args(self, code, timezone):
        self.code = code
        self.timezone = pytz.timezone(timezone)

    def __repr__(self):
        return self.line()

    def line(self):
        return ' '.join([self.code, self.timezone.zone])

load_airports()
