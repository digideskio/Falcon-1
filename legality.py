from datetime import timedelta

import flight

def thirty_in_seven(this):
    def total(ls):
        return reduce(lambda x, y: x + y, ls)

    seven_days = timedelta(days=7)

    last_7_days = flight.get_flights(after=this.dept_time - seven_days,
                                     before=this.arr_time)
    total_time = total([f.length() for f in last_7_days])
    return (
        total_time < timedelta(hours=30),
        '%s hours, %s minutes flight time in last 7 days' % (
            int(total_time.total_seconds() // 3600),
            int((total_time.total_seconds() % 3600) // 60),
        )
    )

requirements = [
    thirty_in_seven,
]
