from textblob import TextBlob

text = TextBlob("I lov progrmming in Pythn.")

corrected = text.correct()

print(corrected)

"""
>python trial_1.py
I love programming in Myth.
"""