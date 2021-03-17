# Derived time variables
# default secSinceOriginalVisit = 0
# default secSinceLastVisit = 0
# default tdFromOriginal = None
# default tdFromLast = None
# default timeOfDay = ""

# Imports & Convenience Definitions
init -30 python:
    from datetime import datetime
    from datetime import timedelta

    now = datetime.now()

# Library Functions
init -20 python:
    class timeInferenceLibrary:
        secSinceOriginalVisit = -1
        secSinceLastVisit = -1

        def getSecondsFromDateTime(self, dt):
            return ((dt - datetime(1970, 1, 1)).total_seconds())
        def getHoursSinceFirstVisit(self):
            return ((dt - persistent.originalVisitTimestamp).total_hours)
        def getDaysSinceFirstVisit(self, dt = now):
            return ((dt - persistent.originalVisitTimestamp).days)
        def getDateHour(self, time = now.time()):
            return time.hour
        # ## Possible values: Morning, Afternoon, Evening, Night
        def getTimeOfDay(self, time = now.time()):
            if time.hour >= 6 and time.hour <= 11:
                return "Morning"
            if time.hour >= 12 and time.hour <= 16:
                return "Afternoon"
            if time.hour >= 17 and time.hour <= 19:
                return "Evening"
            if time.hour >= 20 or time.hour <= 5:
                return "Night"
    timeInference = timeInferenceLibrary()

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
    if persistent.originalVisitTimestamp is None:
        print("Initializing first timestamp")
        persistent.originalVisitTimestamp = now
        persistent.lastVisitTimestamp = now
        applyDefaults()

    tdFromOriginal = (now - persistent.originalVisitTimestamp)
    tdFromLast = (now - persistent.lastVisitTimestamp)

    timeInference.secSinceOriginalVisit = tdFromOriginal.total_seconds()
    timeInference.secSinceLastVisit = tdFromLast.total_seconds()
    print("Last lastVisitTimestamp =", persistent.lastVisitTimestamp)
    persistent.lastVisitTimestamp = now
    print("now =", now)
    print("Current Time =", now.strftime("%H:%M:%S"))
    print("Time since first launch =", timeInference.secSinceOriginalVisit)
    print("Time since last launch =", timeInference.secSinceLastVisit)


## Flow control overrides

# Skip the main menu that Ren'Py normally shows and jump straight to the creature's greeting
label main_menu:
    return
