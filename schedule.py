import bisect
import flight

class Schedule:
    def __init__(self, *args, **kwargs):
        self.flights = []
    
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
