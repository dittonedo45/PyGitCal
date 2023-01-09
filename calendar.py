

import time
import datetime
import collections

class Date(datetime.datetime):
    def __new__(s, *arg, **kwargs):
        return datetime.datetime.__new__(s, *arg, **kwargs)
    def __str__(s):
        return s.strftime("%B").center(19)
    pass
pass

class Week_Vector(list):
    def __setitem__(s, *arg, **kwargs):
        print(arg)
        return super().__setitem__(s, *arg, **kwargs)

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
        y=Date.now().year
    months=[]
    def _cal():
        nonlocal y
        i=Date(y, 1, 1)
        while True:
            j=i
            i+=datetime.timedelta(days=1,)
            if i.month!=j.month:
                yield j.month, 1, j.day
                pass
            if j.year!=y:
                break
    for month, start, end in _cal():
        s=Date(y, month, start)
        e=Date(y, month, end)
        months.append((s, month_mem(s, e)))
        pass
    return months
    pass

def render_month(m):
    def _render_month(m):
        ms=[]
        sarr=Week_Vector()
        wd=0
        yield list(map(lambda x: "%s"%(x,),
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
                    sarr=Week_Vector()
                wd=sta.tm_wday
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
        month=str(month_i)
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
    print(("%d"%(y,)).center((22*3)))
    for j in x_x(pack(y), 3):
        for i in zip(*j):
            print("  ".join(i))
        print("\n")
        pass
    pass
for i in range(2002, 2025):
    display_cal(i)
