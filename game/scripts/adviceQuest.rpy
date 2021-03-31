## Advice quest constants: 
#   These are various string constants used to track progress in the "advice quest"
define dateUpdateAppointment = "DateUpdateAppointment"
define adviceMilestoneFirstDate = "DidFirstDate"
define adviceMilestoneSecondDate = "DidSecondDate"
define adviceMilestoneMarriage = "GotMarried"
define adviceMilestoneFinishedQuest = "Finished"
define adviceChoiceHike = "Hike"
define adviceChoiceDinner = "Fancy Dinner"

init python:
    ## Returns the name of a the menu option to go to the next "date advice label," or "None"
    #   if there is no available date advice label
    def tryGetAdviceMenuOption():
        # No dating option on the first visit
        if timeInference.isFirstEverVisit:
            return None
        # If we haven't started the dating quest, go to the first date conversation
        if persistent.adviceQuestMilestone is None:
            return "You look far away. Is there something on your mind?"

        # If we're awaiting a date result, check to see if we have a pending date appointment and if we've passed its timestamp gate
        dateApt = timeInference.getScheduledAppointment(dateUpdateAppointment)
        # Appointment must exist, and we must be past the appointment time
        if dateApt is None or dateApt.getMinutesWithinAppointment() <= -0.5:
            return None
        # Return a menu option appropriate to the current progress in the advice "quest"
        if persistent.adviceQuestMilestone == adviceMilestoneFirstDate:
            return "How did your first date go??"
        elif persistent.adviceQuestMilestone == adviceMilestoneSecondDate:
            return "How did your second date go??"
        elif persistent.adviceQuestMilestone == adviceMilestoneMarriage:
            return "So...... what did they say?"
        return None

    ## Jump to the label of the next date. Make sure you use tryGetDateMenuOption first to make sure that this is allowed!
    def jumpToNextAdviceLabel():
        # Jump to the label appropriate to the current progress in the advice quest
        if persistent.adviceQuestMilestone is None:
            renpy.jump("firstDateAdvice")
        elif persistent.adviceQuestMilestone == adviceMilestoneFirstDate:
            renpy.jump("secondDateAdvice")
        elif persistent.adviceQuestMilestone == adviceMilestoneSecondDate:
            renpy.jump("marriageAdvice")
        elif persistent.adviceQuestMilestone == adviceMilestoneMarriage:
            renpy.jump("marriageSuccess")


label firstDateAdvice: 
    $ applyNeutralSprite()
    t "Hey!! So this is a little silly, but, uh"
    t "..."
    t "I need some advice."
    t "There's this other creature, and, uh, I think I really like them"
    $ setSprite("Sheepish")
    t "Like a lot."
    t "We've always just been really good friends, y'know, but I really think there's something there!"
    $ applyNeutralSprite()
    t "I don't know..."
    $ setSprite("Sheepish")
    t "We both just make each other laugh in a way that feels really special"
    $ applyNeutralSprite()
    t "What do you think I should do?"
    menu:
        "Ask them out":
            $ setSprite("Sheepish")
            t "Aaaaaaaaaaaaaaa"
            t "..."
            t "Hooo."
            t "Okay you are definitely right"
            t "I feel like nursing a secret crush is a little juvenile"
            $ hourAge = timeInference.getHoursSinceFirstVisit()
            $ applyNeutralSprite()
            t "I'm a whole [hourAge] hours old!! Time to rip off the band-aid"
            t "Carpe that diem, you know?"
        "Hold your peace, even if you regret it for the rest of your life":
            $ applyNeutralSprite()
            t "Uh."
            t "Wow you kind of put that really severely"
            t "Was that reverse psychology??"
            t "Ok whatever anyway I think bizarrely you have help me make up my mind. I'm going to do it!!"
    $ setSprite("Sheepish")
    t "Anyway ok wish me luck. I will report back in a bit!"
    # Update the date progress, and schedule an appointment to check back in on the date in 3 hours
    $ persistent.adviceQuestMilestone = adviceMilestoneFirstDate 
    $ timeInference.scheduleAppointmentWithDelta(dateUpdateAppointment, timedelta(hours = 3))
    jump mainLoop

label secondDateAdvice: 
    $ applyNeutralSprite()
    $ setSprite("Happy")
    t "OK wow I am so glad you asked"
    t "Honestly it went great. "
    t "I, as you know, am a gentle carefree spirit, but this friend of mine has always been very serious and sardonic"
    $ applyNeutralSprite()
    t "Sometimes we get on each other's nerves"
    t "But our date was just fantastic!! it feels like we just balance each other out well. Each giving something the other needs"
    $ setSprite("Sheepish")
    t "Just like a rom-com!!!! The tired cynical Business Man falls in love with an easygoing florist"
    t "The Oldest Story"
    $ applyNeutralSprite()
    t "Anyway I'd love your opinion on what to do next"
    menu:
        "Go on a hike":
            $ persistent.secondDateChoice = adviceChoiceHike
            $ setSprite("Happy")
            t "Ooh a hike is a good idea for a date."
            t "An outdoor activity is a great way to get to know somebody!"
            t "There's a great advantage in the combination of uninterrupted time to socialize, but also cool stuff to look at that allows for moments of silence without awkwardness"
            t "I will go out and let you know the report!"
        "Go out to a fancy restaurant":
            $ persistent.secondDateChoice = adviceChoiceDinner
            t "A restaurant??"
            $ setSprite("Happy")
            t "I like it baby."
            t "Go big or go home! Romantic intentions require romantic gestures"
            t "Life is short. At any point I could be tracked down and killed instantly by one of the many people I have Wronged in the past"
            t "I will go out and let you know the report!"
    # Update the date progress, and schedule an appointment to check back in on the date in 3 hours
    $ persistent.adviceQuestMilestone = adviceMilestoneSecondDate
    $ timeInference.scheduleAppointmentWithDelta(dateUpdateAppointment, timedelta(hours = 3))
    $ applyNeutralSprite()
    jump mainLoop

label marriageAdvice: 
    t "Ok so the second date went great"
    if persistent.secondDateChoice == adviceChoiceHike:
        $ setSprite("Happy")
        t "The hike was so good!"
        t "It was hot outside, which was good because we both got really sweaty and so there was no pressure or expection to look composed"
        t "I learned a lot about them! Apparently they are wanted in 10 different jurisdictions for crimes committed against the state, in the name of the people"
        t "But they'll never get caught >:)"
        t "I think..."
        $ setSprite("Sheepish")
        t "I think I'm in love"
    if persistent.secondDateChoice == adviceChoiceDinner:
        $ setSprite("Happy")
        t "Dinner was great!!"
        t "I learned so much about them. They have a pet pigeon!"
        $ applyNeutralSprite()
        t "Like a straight-up feral pigeon that you'd see on the street"
        t "While normally owning a wild animal is inappropriate, this is a case where the animal is considered 'non-releasable' due to wing damage"
        t "Additionally, feral pigeons are descended from a domestic animal, so it's not quite so unnatural for them to live with people"
        t "Did you know that pigeons were some of the first-ever domesticated animals?"
        $ setSprite("Happy")
        t "Anyway they just seem really conscientious and loving and just all the ideal qualities in any person"
    $ setSprite("Sheepish")
    t "I've been thinking..."
    t "I am going to ask them to marry me."
    t "No hesitation. This is what feels right."
    t "What do you think?"
    menu:
        "Go for it":
            t "Hell yeah!!! I knew you'd understand"
        "Obviously go for it":
            t "Hell to the yes. We are doing this."
    t "No fear!!! I am going to carpe the shit out of that diem"
    t "I will report back once I have put a ring on it :)))))))"
    # Update the date progress, and schedule an appointment to check back in on the date in 3 hours
    $ persistent.adviceQuestMilestone = adviceMilestoneMarriage
    $ timeInference.scheduleAppointmentWithDelta(dateUpdateAppointment, timedelta(hours = 3))
    $ applyNeutralSprite()
    jump mainLoop

label marriageSuccess: 
    $ setSprite("Happy")
    t "GUESSSS WHATTTTTT"
    t "They said yes :)"
    t ":))))))))))))"
    t "I am beyond psyched!!!!! Holy shit my friend it is happening"
    $ setSprite("Sheepish")
    t "I know it's maybe archaic and this is a choice everybody must navigate on their own, but I am going to take their last name"
    t "I just like the idea of it, you know?"
    t "I feel like your name is the word for the type of thing that you are, and now that I have my ring I feel like a different type of thing"
    $ setSprite("Happy")
    t "Thank you for all your advice :)"
    t "AAAAAAAAaaaaaAAAAAAaaaqaaa"
    t ":)"
    # Update the date progress, and clear the date update appointment because there are no further updates!
    $ applyNeutralSprite()
    $ timeInference.unscheduleAppointment(dateUpdateAppointment)
    $ persistent.adviceQuestMilestone = adviceMilestoneFinishedQuest
    jump mainLoop