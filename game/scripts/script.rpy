## Note from Robin: ###
#  When beginning to go through this example, I recommend starting at the "label introGreeting" section halfway below. Then, come back and read
#   this file from the top. "label introGreeting" is the start of where game content and behavior is run, whereas this first section is where
#   we define core functionality and handle initialization

## TODO:
# X Appointments:
#    - String helpers for appointments
# X "Fake timestamp" functionality
# X Permanent progress example
# X Backwards time travel warning / error
# X Day # functionality
# - Make time travel warning less horrible
# X "Days known" gates
# - Mumble sounds


### Character Definitions: ###
# A Ren'Py speaker definition for the tamagotchi
define t = Character("???")


### Local State Definitions: ###
## These variables will *not* be saved when the game is opened and closed; only those saved in 'persistent' will

# A flag which, if true, indicates that a new poop has been created on the startup of this session
default hasNewPoop = False
# Whether the player has pet the creature this session
default hasPetThisSession = False


### Constants ###
## These are unchanging variables which are defined here so that they can be used consistently
define partyPrepDurationMinutes = 2
define partyLateThresholdMinutes = 5


### Animation & Transform Definitions: ###
# Robin: don't worry too much about understanding the animation definitions here; they make the duck-snake animate between two sprites
#  instead of the static images you normally get from the "show" command, which is cute, but it's not core Ren'Py functionality you need 
#  to immediately understand.

# Display the duck snake, cycling between two frames of animation
default bodySprite1 = "DuckSnake/no1.png"
default bodySprite2 = "DuckSnake/no2.png"
image DuckSnake animated:
    nearest True
    zoom 10
    bodySprite1
    pause 0.75
    bodySprite2
    pause 0.75
    repeat

# Display a poop and make it flip back and forth to give a sense of animation
image poop:
    nearest True
    xzoom 20
    yzoom 20
    "Objects/obj poop.png"
    pause 0.75
    xzoom -20
    pause 0.75
    repeat

# The location for the poop to go, on the right-hand side of the screen
transform poopPos:
    xpos 900
    yalign 0.6


##### Initialization #####

init -11 python:
    # initializeDefaultPersistentState() must be declared here, specificially in "init -11." This is to ensure it is called from
    #  the time inference libary initialization, which is in init -10. I could probably stand to organize this a little more cleanly
    # Runs exactly once, the first time the user opens the program. Initializes default values for persistent state
    def initializeDefaultPersistentState():
        persistent.hunger = 100
        persistent.hasPoop = False
        scheduleNextPoop()

    # Schedule a poop 1 minute from the current time
    def scheduleNextPoop():
        global timeInference
        persistent.nextPoopTs = timeInference.getCurrentDateTime() + timedelta(minutes = 1)


init python:
    ### Character API: ###
    # Change the character's active body sprite according to an expression, making sure to update both frames referenced by the animation
    def setSprite(sprite):
        global bodySprite1
        global bodySprite2
        if sprite == "Default":
            bodySprite1 = "DuckSnake/no1.png"
            bodySprite2 = "DuckSnake/no2.png"
        elif sprite == "Hungry":
            bodySprite1 = "DuckSnake/drool1.png"
            bodySprite2 = "DuckSnake/drool2.png"
        elif sprite == "Eating":
            bodySprite1 = "DuckSnake/lick1.png"
            bodySprite2 = "DuckSnake/lick2.png"
        elif sprite == "Sad":
            bodySprite1 = "DuckSnake/sad1.png"
            bodySprite2 = "DuckSnake/sad2.png"
        elif sprite == "Happy":
            bodySprite1 = "DuckSnake/happy1.png"
            bodySprite2 = "DuckSnake/happy2.png"
        elif sprite == "Angry":
            bodySprite1 = "DuckSnake/angry1.png"
            bodySprite2 = "DuckSnake/angry2.png"
        elif sprite == "Sheepish":
            bodySprite1 = "DuckSnake/sheepish1.png"
            bodySprite2 = "DuckSnake/sheepish2.png"
        else:
            print("WARNING: received setSprite call with invalid sprite value \"", sprite, "\"")
        renpy.show("DuckSnake animated")

    # Change the character's active body sprite to a "neutral" face, which will change depending on my level of hunger
    def applyNeutralSprite():
        if persistent.hunger < 10:
            setSprite("Sad")
        elif persistent.hunger < 50:
            setSprite("Hungry")
        else:
            setSprite("Default")

    # Add or remove poop from the screen
    def setPoop(hasPoop):
        if hasPoop:
            renpy.show(name="poop", at_list=[poopPos()])
            persistent.nextPoopTs = datetime.max
            persistent.hasPoop = True
        else:
            scheduleNextPoop()
            renpy.hide("poop")
            persistent.hasPoop = False

####### Startup Initialization: #######
label start:
    # Disable right-click menu
    $ _game_menu_screen = None

    # Set the background appropriately to the real-world time of day
    if timeInference.getTimeOfDay() == "Morning":
        scene bg morning
    elif timeInference.getTimeOfDay() == "Afternoon":
        scene bg afternoon
    elif timeInference.getTimeOfDay() == "Evening":
        scene bg evening
    elif timeInference.getTimeOfDay() == "Night":
        scene bg night
    
    ## Execute consequences of the passage of time: ##
    python:
        # Atrophy hunger based on how much time has passed since last opening the app. Our creature gets hungry very quickly
        hungerDelta = timeInference.secSinceLastVisit / 10
        persistent.hunger = max(persistent.hunger - hungerDelta, 0)
        print("hunger atrophied by ", hungerDelta, ". hunger is now ", persistent.hunger)

        # Check to see if there's previously existing poop 
        if persistent.hasPoop:
            setPoop(True)
        # Check to see if we have reached a poop that was previously scheduled
        elif timeInference.getCurrentDateTime() > persistent.nextPoopTs:
            setPoop(True)
            hasNewPoop = True
        
        # Display the creature with a sprite appropriate to their current state (hunger, etc.)
        applyNeutralSprite()

    # Show the hunger bar
    show screen hungerBar

    # Play some background ambiance!
    play music "audio/DesertAmbience.ogg"

    show DuckSnake animated at truecenter

    jump introGreeting

# Choose an introductory greeting to give the player:
label introGreeting:

    # Remark on time passed since last visit:
    # If we have a scheduled party, react to that party:
    $ partyAppointment = timeInference.getScheduledAppointment("Test Party")
    if not partyAppointment is None:
        $ partyTimeliness = partyAppointment.getMinutesWithinAppointment()
        $ print("Party timeliness is ", partyTimeliness)
        # Case 1: early to the party:
        if partyTimeliness < 0:
            $ timeUntilParty = -1 * partyTimeliness
            t "Hey again! If you're here for the party, I'm still setting up. Please come back in [timeUntilParty] minutes"
        # Case 2: late to the party:
        elif partyTimeliness > partyLateThresholdMinutes:
            $ timeInference.unscheduleAppointment("Test Party")
            $ setSprite("Angry")
            t "Well look who came crawling in."
            t "You're late! I planned a whole party and you didn't even show up"
            play sound "audio/PartyBlower.wav"
            t "What the hell!!!"
            t "I get it, you're busy, it happens to the best of us, but maybe text me or something next time??? Jeez."
            t "Some people..."
            $ applyNeutralSprite()
        # Case 3: on time for the party!
        else:
            $ timeInference.unscheduleAppointment("Test Party")
            jump scheduledParty
    elif timeInference.secSinceLastVisit > 30:
        t "Oh wow, you again? It's been a minute. Precisely, [timeInference.secSinceLastVisit] seconds"

    if hasNewPoop:
        $ hasNewPoop = False
        t "Guess what I pooped???"

    # If first visit, say a special introductory line
    if timeInference.isFirstEverVisit:
        t "Hi there!! Welcome!!! It's great to finally meet you"
        t "I am a vulnerable creature in your care"
        t "I would like it very much if you could swing by around later to feed me."
    # Remark on hunger:
    elif persistent.hunger <= 10:
        t "Where the hell were you?? I'm starving!"
    elif persistent.hunger <= 50:
        t "Yoooo just in the nick of time, I've started to get a little hungry"
    # If no hunger remark, just say a normal greeting from a pool of random possibilities.
    else:
        $ possibleWelcomes = ["Nice to see you again", "You again!", "Ayyyyy, there's my favorite human", "What's up losers guess who's in the HOUSE"]
        $ welcome = renpy.random.choice(possibleWelcomes)
        t "[welcome]"
    jump mainLoop

# This is the main "loop" containing menu actions that are always available. It will always run in a cycle.
label mainLoop:
    # See if we have the menu option to ask the 
    python:
        adviceMenuOption = tryGetAdviceMenuOption()
        if adviceMenuOption is None:
            adviceMenuOption = ""
        print("Date Menu option returned ", adviceMenuOption)

    # Display the main menu of all options
    menu:
        "Feed the creature":
            if (persistent.hunger < 100):
                $ persistent.hunger = min(persistent.hunger + 35, 100)
                $ setSprite("Eating")
                t "Thank you for feeding me"
                t "Such is the fate of all creatures, to suck nutrients from the earth until the earth reclaims them"
                $ setSprite("Happy")
                if persistent.hunger < 100:
                    t "Still feeling a little peckish tho tbh"
                else:
                    t "I'm feeling all fed up! Which is to say, very satisfied"
                $ applyNeutralSprite()
            else:
                t "I appreciate that, but I'm actually quite full. Thanks though!"
        "Pet the creature" if hasPetThisSession == False:
            "You rub your hand along the top of the creature"
            t "Awww, that feels good!"
            "Their head is smoother than any material you have ever touched"
            t "Thank you :)"
            $ hasPetThisSession = True
        "Apologize":
            if persistent.hasPoop:
                t "That's okay!"
                t "Yes, it's gross that there's poop, but that's really on me as much as it is on you"
                t "Let's just take care of the situation instead of dwelling on it"
            elif persistent.hunger < 50:
                t "Hey, well thanks for saying sorry"
                t "I got pretty hungry and I'm a little miffed that you left me for so long, but the acknnowledgement is appreciated"
                t "Could you maybe feed me?"
            else:
                t "You apologize too much"
                t "What is there to apologize for? I worry that you have a reflexive guilt complex. You should give yourself more credit"
                t "I often find it useful, when you feel the impulse to apologize, to say \"Thank you\" instead of \"I'm Sorry\""
        "Clean up poop" if persistent.hasPoop:
            $ setPoop (False)
            $ setSprite("Happy")
            t "Thanks!! God that was gross"
            $ applyNeutralSprite()
        "Schedule party" if not timeInference.hasScheduledAppointment("Test Party"):
            t "Hey, I know! Let's schedule a party!"
            t "I will need a few minutes to prepare"
            t "Please meet me back here in [partyPrepDurationMinutes] minutes and I will have the party set up"
            t "Don't be early, and please dont be more than [partyLateThresholdMinutes] minutes late or else the appetizers will get cold"
            $ timeInference.scheduleAppointmentWithDelta("Test Party", timedelta(minutes = partyPrepDurationMinutes))
        "[adviceMenuOption]" if not adviceMenuOption == "":
            $ jumpToNextAdviceLabel()

    "As above, so below."
    jump mainLoop

label scheduledParty:
    show bg party
    play sound "audio/PartyBlower.wav"
    $ setSprite("Happy")
    t "Surprise!!!!"
    $ applyNeutralSprite()
    t "... Is what I would have said, had this not been an immaculately scheduled event for which I gave you significant advance notice"
    t "......"
    $ setSprite("Happy")
    t "Isn't this great!"
    t "Party time!!!"
    $ applyNeutralSprite()
    jump mainLoop

