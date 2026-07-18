#!/usr/bin/python3
from simpleeval import simple_eval

def calculate(expression: str)-> str:
    """
    Safely evaluate a mathematical expression
    Returns a string suitable for an LLM
    """
    try:
        # pass in the expression by an llm
        result=simple_eval(expression)

        return f"""
Calculation

Expression: {expression}
Result:{result}
"""
    except Exception as e:
        return f"Calculation Error: {e}"

# Test
if __name__=="__main__":
    expression="25 * (18 + 7) / 5"

    # pass our expressopn
    answer=calculate(expression)

    print(f"Tool Answer: {answer}")

"""
(11_Voice_Assistant) J:\Voice_Assistant\Tools\Calculator>python main.py
Tool Answer:
Calculation

Expression: 25 * (18 + 7) / 5
Result:125.0
"""