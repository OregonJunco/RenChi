# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define t = Character("???")
default feedChoice = False

image BabySnake animated:
    nearest True
    zoom 10
    "BabySnake/no1.png"
    pause 0.75
    "BabySnake/no2.png"
    pause 0.75
    repeat

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

image poop:
    nearest True
    xzoom 20
    yzoom 20
    "Objects/obj poop.png"
    pause 0.75
    xzoom -20
    pause 0.75
    repeat

transform poopPos:
    xpos 900
    yalign 0.6

init -11 python:
    def updatePoopStamp():
        p.nextPoopTs = now + timedelta(minutes = 1)

    def applyDefaults():
        p.satiation = 100
        p.hasPoop = False
        updatePoopStamp()

    def setPoop(hasPoop):
        if hasPoop:
            renpy.show(name="poop", at_list=[poopPos()])
            p.nextPoopTs = datetime.max
            p.hasPoop = True
        else:
            updatePoopStamp()
            renpy.hide("poop")
            p.hasPoop = False
    def getSprite():
        return bodySprite1

init python:
    # Character API:
    firstShowSkipFlag = True
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
        global firstShowSkipFlag
        if not firstShowSkipFlag:
            renpy.show("DuckSnake animated")
        else:
            firstShowSkipFlag = False

    def updateSpriteByState():
        if p.satiation < 10:
            setSprite("Sad")
        elif p.satiation < 50:
            setSprite("Hungry")
        else:
            setSprite("Default")

    # Execute time passage consequences
    hungerDelta = secSinceLastVisit / 10
    p.satiation = max(p.satiation - hungerDelta, 0)
    print("Satiation atrophied by ", hungerDelta, " satiation, satiation is now ", p.satiation)


label start:
    show screen healthbar
    if getTimeOfDay() == "Morning":
        scene bg morning
    elif getTimeOfDay() == "Afternoon":
        scene bg afternoon
    elif getTimeOfDay() == "Evening":
        scene bg evening
    elif getTimeOfDay() == "Night":
        scene bg night

    play music "audio/DesertAmbience.ogg"

    # Load any existing poop
    python:
        if p.hasPoop:
            setPoop(True)
        elif now > p.nextPoopTs:
            setPoop(True)
            hasNewPoop = True
        updateSpriteByState()
    show DuckSnake animated at truecenter

    jump introGreeting

default hasNewPoop = False
label introGreeting:
    # Remark on time passed since last visit:
    if secSinceLastVisit > 30:
        t "Oh wow, you again? It's been a minute. Precisely, [secSinceLastVisit] seconds"
    if hasNewPoop:
        $ hasNewPoop = False
        t "Guess what I pooped???"
    # Remark on stats:
    if p.satiation <= 10:
        t "Where the hell were you?? I'm starving!"
    elif p.satiation <= 50:
        t "Yoooo just in the nick of time, I've started to get a little hungry"
    # No other remark, just say something random
    else:
        $ possibleWelcomes = ["Nice to see you again", "You again!", "Ayyyyy, there's my favorite human", "What's up mothafuckas guess who's in the HOUSE"]
        $ welcome = renpy.random.choice(possibleWelcomes)
        t "[welcome]"
    jump mainLoop

label mainLoop:
    menu:
        "Feed the creature":
            if (p.satiation < 100):
                $ p.satiation = min(p.satiation + 20, 100)
                $ setSprite("Eating")
                t "Thank you for feeding me"
                t "Such is the fate of all creatures, to suck nutrients from the earth until the earth reclaims them"
                $ setSprite("Happy")
                if p.satiation < 100:
                    t "Still feeling a little peckish tho tbh"
                else:
                    t "I'm feeling all fed up! Which is to say, very satisfied"
                $ updateSpriteByState()
            else:
                t "I appreciate that, but I'm actually quite full. Thanks though!"
        "Apologize":
            if p.hasPoop:
                t "That's okay!"
                t "Yes, it's gross that there's poop, but that's really on me as much as it is on you"
                t "Let's just take care of the situation instead than dwelling on it"
            elif p.satiation < 50:
                t "Hey, well thanks for saying sorry"
                t "I got pretty hungry and I'm a little miffed that you left me for so long, but the acknnowledgement is appreciated"
                t "Could you maybe feed me?"
            else:
                t "You apologize too much"
                t "What is there to apologize for? I worry that you have a reflexive guilt complex. You should give yourself more credit"
                t "I often find it useful, when you feel the impulse to apologize, to say \"Thank you\" instead of \"I'm Sorry\""
        "Clean up poop" if p.hasPoop:
            $ setPoop (False)
            $ setSprite("Happy")
            t "Thanks!! God that was gross"
            $ updateSpriteByState()

    "As above, so below"

    jump mainLoop
