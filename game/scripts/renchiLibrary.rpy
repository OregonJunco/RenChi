# Derived time variables
default secSinceOriginalVisit = 0
default secSinceLastVisit = 0
default tdFromOriginal = None
default tdFromLast = None
## Possible values: Morning, Afternoon, Evening, Night
default timeOfDay = ""

# Imports & Convenience Definitions
init -30 python:
    from datetime import datetime

    now = datetime.now()
    p = persistent

# Library Functions
init -20 python:
    def getSecondsFromDateTime(dt):
        return ((dt - datetime(1970, 1, 1)).total_seconds())
    def getHoursSinceFirstVisit():
        return secSinceOriginalVisit
    def getDateHour(time = now.time()):
        return time.hour
    def getDaysKnown(dt = now):
        return ((dt - p.originalVisitTimestamp).days)
    def getTimeOfDay(time = now.time()):
        hour = time.hour
        if hour >= 6 and hour <= 11:
            return "Morning"
        if hour >= 12 and hour <= 16:
            return "Afternoon"
        if hour >= 17 and hour <= 19:
            return "Evening"
        if hour >= 20 or hour <= 5:
            return "Night"

# tests
init -15 python:
    def runTests():
        allHours = range(24)
        for h in allHours:
            # fakeTime = datetime.time(hour = h)
            fakeTime = datetime(1970, 1, 1, h).time()
            # print("Testing with fakeTime" + fakeTime)
            print("hour ", h, " is ", getTimeOfDay(fakeTime))

# Infer time since the last visit:
init -10 python:
    if p.originalVisitTimestamp is None:
        print("Initializing first timestamp")
        p.originalVisitTimestamp = now
        p.lastVisitTimestamp = now

    tdFromOriginal = (now - p.originalVisitTimestamp)
    tdFromLast = (now - p.lastVisitTimestamp)
    
    secSinceOriginalVisit = tdFromOriginal.total_seconds()
    secSinceLastVisit = tdFromLast.total_seconds()
    print("Last lastVisitTimestamp =", p.lastVisitTimestamp)
    p.lastVisitTimestamp = now
    print("now =", now)
    print("Current Time =", now.strftime("%H:%M:%S"))
    print("Time since first launch =", secSinceOriginalVisit)
    print("Time since last launch =", secSinceLastVisit)

