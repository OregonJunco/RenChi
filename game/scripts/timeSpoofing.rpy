init -29 python:
    timeSpoofData = object()
    
    # Set this value to True to use a spoofed time and date rather than the actual date.
    #  This is useful for testing time passage without having to actually wait. Just be
    #  sure to set this to False before you ship!
    timeSpoofData.USE_TIMESPOOFING = False

    ## Change The below values to set the spoofed date!
    # The day of the month (minimum is 1, maximum is the number of days in the current month)
    timeSpoofData.day = 1
    # The hour of the day, using a 24 hour clock (13 is 1pm, etc.)
    timeSpoofData.hour = 12
    # The current minute within the hour of the day, from 0 to 59
    timeSpoofData.minute = 0

