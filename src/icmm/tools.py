import datetime

__author__ = "mscholl"
__date__  = "$14.03.2014 11:51:25$"

def current_time_millis():
    now = datetime.datetime.utcnow()
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = now - epoch
    
    days = delta.days * 86400000        # 24 * 60 * 60 * 1000
    seconds = delta.seconds * 1000
    millis = delta.microseconds / 1000
    
    ctm = days + seconds + millis
    
    return ctm