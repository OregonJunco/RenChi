# Imports & Convenience Definitions
init -30 python:
    from datetime import datetime
    from datetime import timedelta


# Library Functions
init -20 python:
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
            return (datetime.now() - self.timestamp).total_seconds() / 60# * (1 if datetime.now() > self.timestamp else -1);

        ## Save the appointment name and time into the "persistent" variable, so that any changes are reflected in the next play session
        def saveToDisk(self):
            # WORKAROUND: Ren'Py seems to have some trouble saving this class directly, so instead we serialize
            #  to disk as a value tuple
            # If there's an existing appointment data with my name, update it with my timestamp and save
            for i in range(len(persistent.storedAppointments)):
                if (persistent.storedAppointments[i][0] == self.appointmentName):
                    persistent.storedAppointments[i][1] = self.timestamp
                    return
            # Otherwise, add a new appointment data
            persistent.storedAppointments.append((self.name, self.timestamp))
        
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
        startupTs = datetime.now()

        ## Return the number of hours since the first visit
        def getHoursSinceFirstVisit(self):
            return ((dt - persistent.originalVisitTimestamp).total_hours)

        ## Return the number of days since the first visit
        def getDaysSinceFirstVisit(self, dt = datetime.now()):
            return ((dt - persistent.originalVisitTimestamp).days)
        
        ## Return the time of day as a readable string. Possible values: Morning, Afternoon, Evening, Night
        def getTimeOfDay(self, time = datetime.now()):
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
            return self.scheduleAppointmentWithTimestamp(appointmentName, datetime.now() + deltaToAppointment)
        
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
    now = datetime.now()
    if persistent.isInitialized is None:
        print("No persistent data: running first-time initialization")
        persistent.isInitialized = True
        persistent.originalVisitTimestamp = now
        persistent.lastVisitTimestamp = now
        persistent.storedAppointments = []
        initializeDefaultPersistentState() # This is defined in the main script.rpy file

    # Calculate how long it's been since the last visit, and since the original visit
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


## Flow control overrides:
# Skip the main menu that Ren'Py normally shows and jump straight to the creature's greeting
label main_menu:
    return
