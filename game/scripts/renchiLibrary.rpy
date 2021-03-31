## This is Version 2.0 of the Tamagotchi Demo!

# Imports & Convenience Definitions
init -30 python:
    from datetime import datetime
    from datetime import timedelta
    from calendar import monthrange


# Library Functions
init -20 python:
    # On initializing, cook the time spoof data into a datetime
    if (not timeSpoofData is None) and timeSpoofData.USE_TIMESPOOFING:
        realNow = datetime.now()
        
        # Clean up spoofed values to prevent argument errors
        numDaysInMonth = monthrange(realNow.year, timeSpoofData.month)[1]
        timeSpoofData.day = max(1, min(numDaysInMonth, timeSpoofData.day))
        timeSpoofData.hour = max(0, min(23, timeSpoofData.hour))
        timeSpoofData.minute = max(0, min(59, timeSpoofData.minute))

        # Use the actual current year and month with a spoofed day, hour, and minute
        timeSpoofData.spoofedStartupTs = datetime(year = realNow.year, month = timeSpoofData.month,
            day = timeSpoofData.day, hour = timeSpoofData.hour, minute = timeSpoofData.minute)

    # Appointments are an easy way to set target dates in the future that you can react to!
    class appointment():
        name = ""
        timestamp = None
        def __init__(self, name, timestamp):
            self.name = name
            self.timestamp = timestamp

        ## Returns the number of minutes that the current timestamp is within the appointment.
        ##  Output is signed; a return value of "30" means "30 minutes late", -30 means "30 minutes early"
        ##  By comparing this value to user-set thresholds, you can determine earlyness, lateness, etc.
        def getMinutesWithinAppointment(self):
            global timeInference
            return (timeInference.getCurrentDateTime() - self.timestamp).total_seconds() / 60

        ## Save the appointment name and time into the "persistent" variable, so that any changes are reflected in the next play session
        def saveToDisk(self):
            # WORKAROUND: Ren'Py seems to have some trouble saving this class directly, so instead we serialize
            #  to disk as a value tuple
            # If there's an existing appointment data with my name, update it with my timestamp and save
            for i in range(len(persistent.storedAppointments)):
                if (persistent.storedAppointments[i][0] == self.name):
                    persistent.storedAppointments[i][1] = self.timestamp
                    return
            # Otherwise, add a new appointment data
            persistent.storedAppointments.append([self.name, self.timestamp])
        
        ## Delete this appointment from the list of scheduled appointments
        def unschedule(self):
            self.timestamp = datetime.max
            indexToDelete = -1
            for i in range(len(persistent.storedAppointments)):
                if (persistent.storedAppointments[i][0] == self.name):
                    indexToDelete = i
            if (indexToDelete >= 0):
                del persistent.storedAppointments[indexToDelete]

    # The time inference library is a one-stop-shop for Ren'Py code that needs to reference the passage of time
    #  outside the app.
    class timeInferenceLibrary:
        secSinceOriginalVisit = -1
        secSinceLastVisit = -1
        realStartupTs = datetime.now()
        isFirstEverVisit = False

        ## Returns the actual current date, or, if time spoofing is being used, the spoofed date.
        ##  Use this instead of datetime.now() to make your project compatible with spoofing
        def getCurrentDateTime(self):
            global timeSpoofData
            if (not timeSpoofData is None) and timeSpoofData.USE_TIMESPOOFING:
                # If spoofing, use the spoofed startup time plus the amount of real time that has ellapsed since opening the app
                timeEllapsedSinceOpening = datetime.now() - self.realStartupTs
                return timeSpoofData.spoofedStartupTs + timeEllapsedSinceOpening
            else:
                return datetime.now()

        ## Return the number of hours since the first visit
        def getHoursSinceFirstVisit(self):
            return ((self.getCurrentDateTime() - persistent.originalVisitTimestamp).total_seconds() / (60 * 60))

        ## Return the numbered day of the companionship period; 1 is the first day you opened the creature, 2 is the day after, etc.
        def getCompanionshipPeriodDay(self):
            now = self.getCurrentDateTime()
            firstVisit = persistent.originalVisitTimestamp
            
            output = 0
            # Handle the case where the current month is different from the month you first opened the creature (we don't handle year loops, don't @ me)
            if now.month > firstVisit.month:
                monthCounter = firstVisit.month
                while now.month > monthCounter:
                    mr = monthrange(firstVisit.year, monthCounter)
                    if monthCounter == firstVisit.month:
                        output += mr[1] - firstVisit.day
                    else:
                        output += mr[1]
                    monthCounter += 1
                output += now.day
            else:
                output = now.day - firstVisit.day
            # Add 1 to output so that the 1st day is 1 instead of 0
            output += 1
            return output
        
        ## Return the time of day as a readable string. Possible values: Morning, Afternoon, Evening, Night
        def getTimeOfDay(self):
            time = self.getCurrentDateTime()
            if time.hour >= 6 and time.hour <= 11:
                return "Morning"
            if time.hour >= 12 and time.hour <= 16:
                return "Afternoon"
            if time.hour >= 17 and time.hour <= 19:
                return "Evening"
            if time.hour >= 20 or time.hour <= 5:
                return "Night"
        
        ## If we have a scheduled appointment labeled as appointmentName, return it
        def getScheduledAppointment(self, appointmentName):
            for aptData in persistent.storedAppointments:
                if (aptData[0] == appointmentName):
                    return appointment(aptData[0], aptData[1])
            return None

        ## Returns True or False depending on whether we have a scheduled appointment registered under the provided name
        def hasScheduledAppointment(self, appointmentName):
            return not self.getScheduledAppointment(appointmentName) is None
        
        ## Schedule an appointment to take place at a specified time delta from the current time (e.g. "in 15 minutes")
        def scheduleAppointmentWithDelta(self, appointmentName, deltaToAppointment):
            global timeInference
            return self.scheduleAppointmentWithTimestamp(appointmentName, timeInference.getCurrentDateTime() + deltaToAppointment)
        
        ## Schedule an appointment to take place at absolute timestamp
        def scheduleAppointmentWithTimestamp(self, appointmentName, timestamp):
            # If we already have an appointment with this name, just modify its timestamp 
            existingAppointment = self.getScheduledAppointment(appointmentName)
            if not existingAppointment is None:
                existingAppointment.timestamp = timestamp
                existingAppointment.saveToDisk()
                return existingAppointment;
            # Otherwise, create and save a new appointment!
            newAppointment = appointment(appointmentName, timestamp)
            newAppointment.saveToDisk()
            return newAppointment
    
        ## Delete a scheduled appointment
        def unscheduleAppointment(self, appointmentName):
            apt = self.getScheduledAppointment(appointmentName)
            if not apt is None:
                apt.unschedule()

    # Initialize library instance
    timeInference = timeInferenceLibrary()

# First startup: run time inference ocde
init -10 python:
    # If we have no original visit timestamp, this is a brand-new session!
    #  Set up some initial values
    now = timeInference.getCurrentDateTime()
    if persistent.isInitialized is None:
        print("No persistent data: running first-time initialization")
        persistent.isInitialized = True
        persistent.originalVisitTimestamp = now
        persistent.lastVisitTimestamp = now
        persistent.storedAppointments = []
        if not initializeDefaultPersistentState is None:
            initializeDefaultPersistentState() # This is defined in the main script.rpy file
        timeInference.isFirstEverVisit = True

    # Calculate how long it's been since the last visit, and since the original visit
    tdFromOriginal = (now - persistent.originalVisitTimestamp)
    tdFromLast = (now - persistent.lastVisitTimestamp)
    timeInference.secSinceOriginalVisit = tdFromOriginal.total_seconds()
    timeInference.secSinceLastVisit = tdFromLast.total_seconds()

    # Check for backwards time travel, which could put us in a bad state
    if timeInference.secSinceLastVisit < -1:
        timeInference.hasDoneBackwardsTimeTravel = True
    else:
        timeInference.hasDoneBackwardsTimeTravel = False
        print("Last lastVisitTimestamp =", persistent.lastVisitTimestamp)
        persistent.lastVisitTimestamp = now
        print("now =", now)
        print("Current Time =", now.strftime("%H:%M:%S"))
        print("Time since first launch =", timeInference.secSinceOriginalVisit)
        print("Time since last launch =", timeInference.secSinceLastVisit)


## Flow control overrides:
# Skip the main menu that Ren'Py normally shows and jump straight to the creature's greeting
label main_menu:
    # If the user has accidentally done backwards time travel, show an error message and quit
    if timeInference.hasDoneBackwardsTimeTravel:
        $ minuteDelta = timeInference.secSinceLastVisit / 60 
        "ERROR: detected a negative time delta of [minuteDelta] minutes, meaning that you have 'traveled back in time' through time spoofing."
        "This is invalid; either move your spoofed timestamp forward, or clear persistent data to create a new starting timestamp"
        $ renpy.quit()
    return
