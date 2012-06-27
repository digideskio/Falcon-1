from datetime import timedelta


def thirty_in_seven(this, schedule):
    def total(collection):
        return reduce(lambda x, y: x + y, collection)

    seven_days = timedelta(days=7)

    last_7_days = schedule.get_range(after=this.dept_time - seven_days,
                                     before=this.arr_time)
    total_time = total([f.length() for f in last_7_days])
    return (
        total_time < timedelta(hours=30),
        '%s hours, %s minutes flight time in last 7 days' % (
            int(total_time.total_seconds() // 3600),
            int((total_time.total_seconds() % 3600) // 60),
        )
    )

REQUIREMENTS = [
    thirty_in_seven,
]


def check(this, schedule):
    legal = True
    status = []

    for requirement in REQUIREMENTS:
        req_legal, req_status = requirement(this, schedule)
        if not req_legal:
            legal = False
            status.append(req_status)

    return legal, status
