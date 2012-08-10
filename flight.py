import re
import datetime
import wx

import airport


def string_to_datetime(string, context=datetime.datetime.now(),
                       airport=None):
    from pytz import utc

    components = string.split(' ')
    date = None
    time_str = None
    if len(components) == 1:
        date = context.date()
        time_str = components[0]
    elif len(components) == 2:
        time_str = components[1]
        if components[0].count('/') == 1:
            date = datetime.datetime.strptime(components[0], '%m/%d').\
                                     replace(year=context.year).date()
        elif components[0].count('/') == 2:
            year_len = len(components[0]) - components[0].rfind('/') - 1
            if year_len == 4:
                date = datetime.datetime.strptime(components[0],
                                                  '%m/%d/%Y').date()
            elif year_len == 2:
                date = datetime.datetime.strptime(components[0],
                                                  '%m/%d/%y').date()

    time = None
    if ':' in time_str:
        time = datetime.datetime.strptime(time_str, '%H:%M').time()
    else:
        time = datetime.datetime.strptime(time_str, '%H%M').time()

    result = datetime.datetime.combine(date, time)

    if airport:
        return airport.timezone.localize(result)
    else:
        return utc.localize(result)


def datetime_to_wx(date):
    return wx.DateTimeFromDMY(date.day, date.month - 1, date.year,
                              date.hour, date.minute, date.second,
                              date.microsecond / 1000)


def format_date(date):
    return date.Format('%m/%d/%y')


def format_time(time):
    return time.Format('%H%M')


def from_line(line, context=None):
    if context is None:
        context = datetime.datetime.now()

    return Flight(**_build_objects(parse_line(line), context))


def _build_objects(components, context):
    pairs = {'departs': 'dept_time', 'arrives': 'arr_time'}
    for key in pairs:
        components[key] = airport.get_airport(components[key])
        components[pairs[key]] = string_to_datetime(components[pairs[key]],
                                                    context, components[key])
    return components


def parse_line(line):
    date = r'\d{1,2}/\d{1,2}(/\d{2}(\d{2})?)?'
    time = r'\d{1,2}:?\d{2}'
    airport_code = r'[A-Za-z]{3}'
    flight_number = r'\d{2,5}'

    departs = r'(?P<departs>' + airport_code + r')'
    arrives = r'(?P<arrives>' + airport_code + r')'
    dept_date = r'(?P<dept_date>' + date + r')'
    dept_time = r'(?P<dept_time>' + time + r')'
    arr_date = r'(?P<arr_date>' + date + r')'
    arr_time = r'(?P<arr_time>' + time + r')'

    date_formats = [
        ' '.join((dept_date, departs, dept_time, arrives, arr_time)),
        ' '.join((departs, dept_date, dept_time, arrives, arr_date,
                  arr_time)),
        ' '.join((departs, dept_date, dept_time, arrives, arr_time)),
        ' '.join((dept_date, flight_number, departs, dept_time, arrives,
                  arr_time)),
    ]
    date_formats = [re.compile(f) for f in date_formats]

    for date_format in date_formats:
        match = date_format.match(line)
        if match:
            return _extract_from_match(match)

    raise ValueError('"%s" doesn\'t match any of the accepted formats.' %
                     line)


def _extract_from_match(match):
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
    return {
        'departs': departs,
        'arrives': arrives,
        'dept_time': dept_time,
        'arr_time': arr_time
    }


class Flight(object):
    def __init__(self, departs, dept_time, arrives, arr_time):
        self.departs = departs
        self.arrives = arrives
        self._dept_time = dept_time
        self._arr_time = arr_time
        self._listeners = []

    def _get_dept_time(self):
        return self._dept_time

    def _set_dept_time(self, dept_time):
        self._dept_time = dept_time
        self.update()

    dept_time = property(_get_dept_time, _set_dept_time)

    def _get_arr_time(self):
        return self._arr_time

    def _set_arr_time(self, arr_time):
        self._arr_time = arr_time
        self.update()

    arr_time = property(_get_arr_time, _set_arr_time)

    def assign(self, other):
        (self.arrives, self.departs,
         self.arr_time, self.dept_time) = (other.arrives, other.departs,
                                           other.arr_time, other.dept_time)

    def report(self, schedule):
        lines = [('%s&ndash;%s departs <b>%s</b> arrives <b>%s</b> ' +
               '<i>[%s]</i>') % (
            self.departs,
            self.arrives,
            self.dept_time.strftime('%x %H%M (%Z)'),
            self.arr_time.strftime('%x %H%M (%Z)'),
            self.length(),
        )]

        import legality
        legal, status = legality.check(self, schedule)

        for status_line in status:
            lines.append('&nbsp;&nbsp;&nbsp;<small>' + status_line +
                         '</small>')

        font_color = 'green' if legal else 'red'
        return '<font color="' + font_color + '">' + \
               '<br />'.join(lines) + '</font>'

    def length(self):
        return self.arr_time - self.dept_time

    def add_listener(self, listener):
        self._listeners.append(listener)

    def update(self):
        for listener in self._listeners:
            listener.update(self)

    def __repr__(self):
        return "Flight('%s')" % str(self)

    def __str__(self):
        return '%s %s %s %s' % (
            self.departs,
            self.dept_time.strftime('%x %H%M'),
            self.arrives,
            self.arr_time.strftime('%x %H%M'),
        )

    def __cmp__(self, other):
        return cmp(self.dept_time, other.dept_time)

    @classmethod
    def copy_of(cls, other):
        return Flight(other.departs, other.dept_time,
                      other.arrives, other.arr_time)
