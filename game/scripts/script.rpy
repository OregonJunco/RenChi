﻿# The script of the game goes in this file.

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

image DuckSnake animated:
    nearest True
    zoom 10
    "DuckSnake/no1.png"
    pause 0.75
    "DuckSnake/no2.png"
    pause 0.75
    repeat


# Skip the main menu and jump straight to the creature's greeting
label main_menu:
    return

init python:
    # Calculate how long it's been since I last visited the creature
    from datetime import datetime
    p = persistent
    def getSecondsFromDateTime(dt):
        return ((dt - datetime(1970, 1, 1)).total_seconds())

    now = datetime.now()
    if p.originalVisitTimestamp is None:
        print("Initializing first timestamp")
        p.originalVisitTimestamp = now
        p.lastVisitTimestamp = now
    
    secSinceFirstVisit = (now - p.originalVisitTimestamp).total_seconds()
    secSinceLastVisit = (now - p.lastVisitTimestamp).total_seconds()
    print("Last lastVisitTimestamp =", p.lastVisitTimestamp)
    p.lastVisitTimestamp = now
    print("now =", now)
    print("Current Time =", now.strftime("%H:%M:%S"))
    print("Time since first launch =", secSinceFirstVisit)
    print("Time since last launch =", secSinceLastVisit)

label start:
    scene bg room

    play music "audio/DesertAmbience.ogg"

    if secSinceLastVisit > 60:
        t "Oh wow, you again? It's been a minute. Precisely, [p.originalVisitTimestamp]"

    t "I'm hungry"
    
    show DuckSnake animated at truecenter

    jump mainLoop

label mainLoop:
    t "I'm hungry!!!"

    menu:
        "Feed the creature":
            t "Thank you for feeding me"
            t "Such is the fate of all creatures, to suck nutrients from the earth until the earth reclaims them"
            $ feedChoice = True
        "Apologize":
            t "You apologize too much"
            t "It's strange, I asked for help, and you apologized. Why the guilt?"
            $ feedChoice = False

    "As above, so below"
    if feedChoice:
        "Remember that time you fed me?"
    else:
        "Instead of apologizing, I find it helpful to say 'thank you'"

    jump mainLoop

# label quit:
#     "This menu will now autosave"
#     $ renpy.save(slotname)
#     return