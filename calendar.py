

import time
import datetime
import collections
import re, random
import sys, itertools

history={}
class Date(datetime.datetime):
    def __new__(cls, *arg, **kwargs):
        return datetime.datetime.__new__(cls, *arg, **kwargs)
    def __str__(self):
        return self.strftime("%B").center(6+(7*3))
    @property
    def yday(s):
        j=s.strftime("%d")
        ts=int(s.timestamp ())
        try:
            x=history[ts]
            k="\033[48;5;%dm%3d\033[0m"%(16+x if x<5 else 21, int(j),)
        except KeyError:
            k="%3d"%(int(j),)
        return show_day(k)
    pass
pass
def count(n):
    return sum(1 for _ in n)
def change_back(t):
    res=Date.fromtimestamp(t)
    return Date(res.year, res.month, res.day).timestamp()
def groupby(cb, itr):
    x={}
    for i in itr:
        k=cb(i)
        if k not in x:
            x[k]=[i]
        else:
            x[k].append(i)
    yield from x.items()

for i in groupby(lambda x: x, map(change_back, sys.history)):
    history[int(i[0])]=len (i[1])

def show_day_func(reg):
    r=re.compile(reg)
    def sub(x):
        nonlocal r
        return x
    return sub

show_day=show_day_func(r"^0+")
class Year(list):
    pass
class Week_Vector(list):
    def __init__(self):
        for _ in range(7):
            self.append("   ")

def month_mem(start, end):
    def _giveday ():
        nonlocal start
        if start>end:
            return None
        day=start
        start+=datetime.timedelta(days=1,)
        return day

    return _giveday
def calculate_each_and_every_month_s_max(y=None):
    if not y:
        y=Date.now().year
    def _cal():
        nonlocal y
        i=Date(y, 1, 1)
        while True:
            j=i
            i+=datetime.timedelta(days=1,)
            if i.month!=j.month:
                yield j.month, 1, j.day
            if j.year!=y:
                break

    for month, start, end in _cal():
        s=Date(y, month, start)
        e=Date(y, month, end)
        yield (s, month_mem(s, e))

def render_month(m):
    def _render_month(m):
        ms=[]
        sarr=Week_Vector()
        wd=0
        yield list(map(lambda x: f"{x}", "Mon Tue Wed Thu Fri Sat Sun".split(" ")))
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
def pack(ya):
    return [
        [str(month_i), *render_month(month_blob)]
        for month_i, month_blob in calculate_each_and_every_month_s_max(ya)
    ]
def x_x(arr, j):
    i=iter(arr)
    try:
        while True:
            yield [next(i) for _ in range(j)]
    except StopIteration:
        pass
def display_cal(y):
    print(("%d"%(y,)).center((2+6+(7*3))*3))
    for j in x_x(pack(y), 3):
        for i in zip(*j):
            print("  ".join(i))
        print("\n")

try:
    for i in range(2018, 2022):
        display_cal(i)
except OverflowError:
    pass
sys.exit (0)
