# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define t = Character("???")

default feedChoice = False

image DuckSnake animated:
    nearest True
    zoom 10
    "DuckSnake/no1.png"
    pause 0.75
    "DuckSnake/no2.png"
    pause 0.75
    repeat

label main_menu:
    return

# The game starts here.

label start:
    scene bg room

    play music "audio/DesertAmbience.ogg"

    # These display lines of dialogue.

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

    # This ends the game.

    jump mainLoop
