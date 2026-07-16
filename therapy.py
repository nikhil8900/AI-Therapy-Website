import os
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

# ----------------------------
# Emotion Detection Model
# ----------------------------

print("Loading CalmBridge Emotion Model...")

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

print("Emotion model loaded successfully!")

conversation_history = []

# ----------------------------
# Emotion Detection
# ----------------------------

def detect_emotion(text):

    try:

        result = emotion_classifier(text)[0][0]

        emotion = result["label"].lower()

        confidence = round(result["score"] * 100, 2)

        return emotion, confidence

    except Exception:

        return "neutral", 0


# ----------------------------
# Safety Check
# ----------------------------

def safety_check(text):

    text = text.lower()

    danger = [

        "suicide",
        "kill myself",
        "end my life",
        "don't want to live",
        "hurt myself",
        "self harm"

    ]

    return any(word in text for word in danger)


# ----------------------------
# Demo Therapist Responses
# ----------------------------

def local_response(user_message, emotion):

    message = user_message.lower()

    # ----------------------------
    # Exam Failure
    # ----------------------------

    if "failed" in message and "exam" in message:

        return """I'm really sorry you're going through this.

Failing an exam can feel incredibly discouraging, especially when you've put in effort.

Right now, I don't want to rush into advice.

I'd like to understand your experience first.

What hurt you the most today—the exam result itself, or how the people around you reacted?"""

    # ----------------------------
    # Parents
    # ----------------------------

    elif "parents" in message and (
        "scold" in message
        or "shout" in message
        or "yell" in message
    ):

        return """That sounds incredibly painful.

Getting disappointing results is already difficult.

Being scolded immediately afterwards can make that pain feel much heavier.

It sounds like today wasn't only about your marks.

It was also about feeling that you disappointed your parents.

What part of that conversation has stayed in your mind the most?"""

    # ----------------------------
    # Hopeless
    # ----------------------------

    elif (
        "lost all hope" in message
        or "disappointed everyone" in message
        or "hopeless" in message
    ):

        return """Thank you for trusting me enough to tell me that.

When we experience failure, our minds often convince us that we've disappointed everyone around us.

But disappointing someone in one situation doesn't make you a disappointment as a person.

Those are two very different things.

Can I ask you something?

If your closest friend were going through exactly what you're facing today, would you judge them the same way you're judging yourself?"""

    # ----------------------------
    # Lonely
    # ----------------------------

    elif "lonely" in message:

        return """Feeling lonely can be emotionally exhausting.

Sometimes loneliness isn't about being physically alone.

It's about feeling like nobody truly understands what you're carrying inside.

Would you like to tell me what has made these feelings stronger recently?"""

    # ----------------------------
    # Best Friend
    # ----------------------------

    elif "best friend" in message:

        return """Losing connection with someone you trust can be incredibly painful.

When someone suddenly becomes distant, it's natural to question yourself and wonder what went wrong.

Before assuming the worst, I'd like to understand more.

Have you had a chance to talk to your friend about what changed?"""

    # ----------------------------
    # Anxiety
    # ----------------------------

    elif (
        "future" in message
        or "anxious" in message
        or "worried" in message
        or "stress" in message
        or "overthinking" in message
    ):

        return """It sounds like your mind has been carrying a lot lately.

When anxiety takes over, our thoughts often imagine the worst possible outcome.

Let's slow things down together.

If you had to choose just one thing that's worrying you the most right now, what would it be?"""

    # ----------------------------
    # Happy
    # ----------------------------

    elif (
        "internship" in message
        or "happy" in message
        or "dream job" in message
        or "selected" in message
    ):

        return """That's wonderful news! 🎉

I'm genuinely happy for you.

Moments like these remind us that our hard work can pay off, even after difficult times.

What are you looking forward to the most in this new opportunity?"""

    # ----------------------------
    # Don't Feel Good
    # ----------------------------

    elif (
        "don't feel good" in message
        or "dont feel good" in message
        or "not feeling good" in message
    ):

        return """Thank you for telling me that.

Sometimes saying "I don't feel good" is the first step toward understanding what's really happening inside us.

There isn't any pressure to explain everything perfectly.

Can you tell me what has been weighing on your mind lately?"""

    # ----------------------------
    # Relationships
    # ----------------------------

    elif (
        "breakup" in message
        or "boyfriend" in message
        or "girlfriend" in message
        or "relationship" in message
    ):

        return """Heartbreak can leave us feeling confused, hurt and emotionally exhausted.

Healing doesn't happen overnight, and it's okay if you're still trying to make sense of everything.

Would you like to tell me what happened between the two of you?"""

    # ----------------------------
    # Motivation
    # ----------------------------

    elif (
        "motivate" in message
        or "motivation" in message
        or "confidence" in message
    ):

        return """I'm glad you're thinking about moving forward.

Building confidence isn't about becoming perfect.

It's about learning to trust yourself even when things don't go exactly as planned.

What's one area of your life where you'd like to feel more confident?"""

    # ----------------------------
    # Default
    # ----------------------------

    return """Thank you for sharing that with me.

I appreciate that you felt comfortable enough to talk about it.

I'm here to listen without judging you.

Could you tell me a little more about what's been happening and how it's been affecting you?"""


# ----------------------------------------------------
# Main AI Function
# ----------------------------------------------------

def get_ai_response(user_message):

    global conversation_history

    if safety_check(user_message):

        return (
            "Thank you for trusting me enough to share something so important.\n\n"
            "It sounds like you're going through an incredibly difficult time.\n\n"
            "You don't have to face this alone.\n\n"
            "If you feel you may act on these thoughts, please contact someone you trust or your local emergency services immediately.\n\n"
            "I'm here to continue talking with you."
        )

    emotion, confidence = detect_emotion(user_message)

    conversation_history.append(
        f"User: {user_message}"
    )

    conversation_history = conversation_history[-20:]

        # -----------------------------------------
    # DEMO MODE
    # -----------------------------------------

    reply = local_response(user_message, emotion)

    conversation_history.append(
        f"CalmBridge AI: {reply}"
    )

    return reply