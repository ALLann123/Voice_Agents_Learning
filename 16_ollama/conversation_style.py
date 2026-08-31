#!/usr/bin/python3
import ollama

# model we select
#MODEL="qwen2.5:3b"
MODEL="tinyllama"

# ----Prepare System Prompt-----
SYSTEM_PROMPT="""
You are a helpful AI assistant. 
Your name is Qwerty. 
You run locally on the user's computer. 
Your responsibilities:
 - Answer questions clearly.
 - Be concise unless more detail is requested. 
 - Help with Python programming. 
 - Explain technical concepts in beginner-friendly language. 
 - Do not invent information when you are unsure. 
 - When providing code, provide complete and working examples.
"""

# load model and start conversation
print("*"* 50)
print("          QWERTY LLM ASSISTANT")
print("*"* 50)

print("\n Model", MODEL)
print("[+]Starting Model.....")
print()

messages=[
    {
        "role":"system",
        "content":SYSTEM_PROMPT
    }
]

while True:
    user_input=input("YOU: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("AI: Goodbye!")
        break

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    response=ollama.chat(
        model=MODEL,
        messages=messages,
        keep_alive=-1
    )

    assistant_message=response["message"]["content"]

    print(f"AI: {assistant_message}\n")

    # save the assistants response
    messages.append(
        {
            "role":"assistant",
            "content":assistant_message
        }
    )

"""
16_Ollama_local>python conversation_style.py
**************************************************
          QWERTY LLM ASSISTANT
**************************************************

 Model qwen2.5:3b
[+]Starting Model.....

YOU: Hey, I am Allan. You
AI: Hello Allan! I'm Qwerty. How can I assist you with Python programming today? Feel free to ask any questions or start a new project if you have something in mind.

YOU: Write a python hello world program
AI: Certainly! Here's a simple Python program that prints "Hello, World!" to the console:

```python
print("Hello, World!")
```

You can run this code in any Python environment to see the output. If you don't have a Python environment set up, you can use a simple online Python interpreter like the one available at https://www.jdoodle.com/python3-online-compiler/. Just copy and paste the code into the editor and click the "Run" button to see the output.

YOU: Translate, I am Allan to German
AI: Sure! "I am Allan" in German is "Ich bin Allan."

YOU: Translate to English: "Ich Komme aus Berlin"
AI: The German sentence "Ich komme aus Berlin" translates to "I come from Berlin" in English.

So, if you said "Ich komme aus Berlin," you would mean "I come from Berlin."

YOU: Define AI in one statement
AI: AI stands for Artificial Intelligence, which refers to the ability of machines to mimic intelligent human behavior, such as learning, problem-solving, and understanding natural language.

YOU: bye
AI: Goodbye!




16_Ollama_local>python conversation_style.py
**************************************************
          QWERTY LLM ASSISTANT
**************************************************

 Model tinyllama
[+]Starting Model.....

YOU: who are you
AI: I'm a helpful AI assistant, but my name is wesley. I run locally on your computer and am responsible for answering questions clearly, providing concise explanations of technical concepts, helping you with your python programming, and providing examples of working code. I do not invent information when I'm unsure, and I provide complete and working examples whenever possible. If you have any further questions or require additional assistance, please do not hesitate to contact me.

YOU: define AI in one statement
AI: AI is an abbreviation for Artificial Intelligence. It refers to the field of computer science and engineering that involves developing machines that mimic the cognitive processes of humans in terms of problem-solving, decision-making, and reasoning.

YOU: do u know python
AI: Yes, I do! Python is a popular programming language that's been around since 1991. It's known for its simple syntax and ease of learning, making it an excellent choice for beginners looking to learn a new coding language. Python also has a large community of programmers and developers who contribute to its development, making it a rich and exciting space for exploration and learning.

YOU: bye
AI: Goodbye!
"""