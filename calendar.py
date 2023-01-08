

import time
import datetime
import collections

def month_mem(start, end):
    def _giveday ():
        nonlocal start
        if start>end:
            return None
        day=start
        start+=datetime.timedelta(days=1,)
        return day
    return _giveday
    pass
def calculate_each_and_every_month_s_max(y=None):
    if not y:
        y=datetime.datetime.now().year
    months=[]
    def _cal():
        nonlocal y
        i=datetime.datetime(y, 1, 1)
        while True:
            j=i
            i+=datetime.timedelta(days=1,)
            if i.month!=j.month:
                yield j.month, 1, j.day
                pass
            if j.year!=y:
                break
    for month, start, end in _cal():
        s=datetime.datetime(y, month, start)
        e=datetime.datetime(y, month, end)
        months.append((s, month_mem(s, e)))
        pass
    return months
    pass

def render_month(m):
    def _render_month(m):
        ms=[]
        sarr=["  " for i in range(7)]
        wd=0
        yield list(map(lambda x: "\033[4;38;5;45m%s\033[0m"%(x,),
            "Mo Tu We Th Fr Sa Su".split(" ")))
        while True:
            for day in range(7):
                d=m()
                if not d:
                    yield sarr
                    yield None
                sta=time.localtime(d.timestamp())
                if wd==6:
                    yield sarr
                    sarr=["  " for i in range(7)]
                wd=sta.tm_wday
                if sta.tm_wday==0:
                    sarr[sta.tm_wday]="\033[32m%02d\033[0m" %(d.day,)
                elif sta.tm_wday==6:
                    sarr[sta.tm_wday]="\033[35;4m%02d\033[0m" %(d.day,)
                elif sta.tm_wday==5:
                    sarr[sta.tm_wday]="\033[38;5;34m%02d\033[0m" %(d.day,)
                else:
                    sarr[sta.tm_wday]="%02d" %(d.day,)
    c=collections.deque()
    c.rotate(1)
    for i in _render_month(m):
        if not i:
            break
        yield(" ".join(i))
        pass
    pass
def pack(ya):
    res=[]
    for month_i, month_blob in calculate_each_and_every_month_s_max(ya):
        month="*%s-"%(month_i.strftime("%B"),)
        month=month.center(22)
        month=month.replace("*", "\033[31;4m")
        month=month.replace("-", "\033[0m")
        res.append(list([month,
            *render_month(month_blob)]))
        pass
    return res
def x_x(arr, j):
    i=iter(arr)
    try:
        while True:
            yield [next(i) for _ in range(j)]
            pass
        pass
    except StopIteration:
        pass
    pass
def display_cal(y):
    print(("%d"%(y,)).center((21*3)))
    for j in x_x(pack(y), 3):
        for i in zip(*j):
            print("  ".join(i))
        print("\n")
        pass
    pass
for i in range(2022, 2025):
    display_cal(i)
