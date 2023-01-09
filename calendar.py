

import time
import datetime
import collections
import re, random

def show_day_func(reg):
    r=re.compile(reg)
    def sub(x):
        nonlocal r
        return x
    return sub

show_day=show_day_func(r"^0+")
class Year(list):
    pass
class Date(datetime.datetime):
    def __new__(s, *arg, **kwargs):
        return datetime.datetime.__new__(s, *arg, **kwargs)
    def __str__(s):
        return s.strftime("%B").center(6+(7*3))
    @property
    def yday(s):
        j=s.strftime("%d")
        if random.randint(0,9)==7:
            k="\033[45m%03d\033[0m"%(int(j),)
        else:
            k="%03d"%(int(j),)
            pass
        print(s.timestamp())
        return show_day(k)
    pass
pass

class Week_Vector(list):
    def __init__(s):
        for _ in range(7):
            s.append ("\033[48;5;45m   \033[0m")

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
    months=Year()
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
            "Mon Tue Wed Thu Fri Sat Sun".split(" ")))
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
                sarr[sta.tm_wday]=d.yday
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
    print(("%d"%(y,)).center((2+6+(7*3))*3))
    for j in x_x(pack(y), 3):
        for i in zip(*j):
            print("  ".join(i))
        print("\n")
        pass
    pass
try:
    for i in range(2002, 2095):
        display_cal(i)
        pass
    pass
except OverflowError:
    pass
