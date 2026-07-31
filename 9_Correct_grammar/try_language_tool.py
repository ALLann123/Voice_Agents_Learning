import language_tool_python

tool = language_tool_python.LanguageTool("en-US")

text = "I lov programming pythn"

matches = tool.check(text)

corrected = language_tool_python.utils.correct(text, matches)

print(corrected)

"""
>python try_language_tool.py
I love programming Python
"""