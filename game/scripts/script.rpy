## Note from Robin: ###
#  When beginning to go through this example, I recommend starting at the "label introGreeting" section halfway below. Then, come back and read
#   this file from the top. "label introGreeting" is the start of where game content and behavior is run, whereas this first section is where
#   we define core functionality and handle initialization

### Character Definitions: ###
##############################
# A Ren'Py character for the tamagotchi
define t = Character("???")


### Local State Definitions: ###
## These variables will *not* be saved when the game is opened and closed; only those saved in 'persistent' will
################################
# A flag for whether a new poop has been created on the startup of this session
default hasNewPoop = False


### Animation & Transform Definitions: ###
##########################################
# Robin: don't worry too much about understanding the animation definitions here; they make the duck-snake animate between two sprites
#  instead of the default static image, which is cute, but it's not core Ren'Py functionality you need to understand.

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

# Display a poop and make it flip back and forth to give the sense of animation
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


### Initialization ###
######################
init -11 python:
    # initializeDefaultPersistentState must be declared here, specificially in "init -11" so that it will be called from 
    #  the time inference libary initialization which is in init -10. Could probably stand to organize this a little more cleanly
    # Runs exactly once, the first time the user opens the program. Initializes default values for persisetent state
    def initializeDefaultPersistentState():
        persistent.hunger = 100
        persistent.hasPoop = False
        scheduleNextPoop()

    # Schedule a poop 1 minute from the current time
    def scheduleNextPoop():
        persistent.nextPoopTs = datetime.now() + timedelta(minutes = 1)


init python:
    ### Character API: ###
    # Change the character's active body sprite for both frames of animation
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
        renpy.show("DuckSnake animated")

    # Change the character's active body sprite to a "neutral" face, which will depend on my level of hunger
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
        # Atrophy hunger ("hunger") based on how much time has passed since last opening the app
        hungerDelta = timeInference.secSinceLastVisit / 10
        persistent.hunger = max(persistent.hunger - hungerDelta, 0)
        print("hunger atrophied by ", hungerDelta, " hunger, hunger is now ", persistent.hunger)

        # Check to see if there's poop, or if we have hit our new poop timestamp and should create a new poop
        if persistent.hasPoop:
            setPoop(True)
        elif timeInference.startupTs > persistent.nextPoopTs:
            setPoop(True)
            hasNewPoop = True
        
        # Display the creature with a sprite appropriate to their current state (hunger, etc.)
        applyNeutralSprite()

    # Show the hunger bar
    show screen hungerBar

    # Play Music!
    play music "audio/DesertAmbience.ogg"

    show DuckSnake animated at truecenter

    jump introGreeting

# Choose an introductory greeting to give the player:
label introGreeting:
    # Remark on time passed since last visit:
    if timeInference.secSinceLastVisit > 30:
        t "Oh wow, you again? It's been a minute. Precisely, [timeInference.secSinceLastVisit] seconds"
    if hasNewPoop:
        $ hasNewPoop = False
        t "Guess what I pooped???"
    # Remark on stats:
    if persistent.hunger <= 10:
        t "Where the hell were you?? I'm starving!"
    elif persistent.hunger <= 50:
        t "Yoooo just in the nick of time, I've started to get a little hungry"
    # If no hunger remark, just say something random
    else:
        $ possibleWelcomes = ["Nice to see you again", "You again!", "Ayyyyy, there's my favorite human", "What's up losers guess who's in the HOUSE"]
        $ welcome = renpy.random.choice(possibleWelcomes)
        t "[welcome]"
    jump mainLoop

# This is the main "loop" containing menu actions that are always available. It will always run in a cycle.
label mainLoop:
    menu:
        "Feed the creature":
            if (persistent.hunger < 100):
                $ persistent.hunger = min(persistent.hunger + 20, 100)
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

    "As above, so below"
    jump mainLoop
