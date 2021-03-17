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


# Library Functions
init -20 python:
    class timeInferenceLibrary:
        secSinceOriginalVisit = -1
        secSinceLastVisit = -1
        startupTs = datetime.now()

        def getSecondsFromDateTime(self, dt):
            return ((dt - datetime(1970, 1, 1)).total_seconds())
        def getHoursSinceFirstVisit(self):
            return ((dt - persistent.originalVisitTimestamp).total_hours)
        def getDaysSinceFirstVisit(self, dt = datetime.now()):
            return ((dt - persistent.originalVisitTimestamp).days)
        def getDateHour(self, time = datetime.now()):
            return time.hour
        # ## Possible values: Morning, Afternoon, Evening, Night
        def getTimeOfDay(self, time = datetime.now()):
            if time.hour >= 6 and time.hour <= 11:
                return "Morning"
            if time.hour >= 12 and time.hour <= 16:
                return "Afternoon"
            if time.hour >= 17 and time.hour <= 19:
                return "Evening"
            if time.hour >= 20 or time.hour <= 5:
                return "Night"
    timeInference = timeInferenceLibrary()

# First startup: run time inference
init -10 python:
    # If we have no original visit timestamp, this is a brand-new session!
    now = datetime.now()
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
