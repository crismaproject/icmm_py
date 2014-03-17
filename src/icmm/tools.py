import datetime

__author__="mscholl"
__date__ ="$14.03.2014 11:51:25$"

def current_time_millis():
    now = datetime.datetime.now()
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = now - epoch
    
    return delta.total_seconds()