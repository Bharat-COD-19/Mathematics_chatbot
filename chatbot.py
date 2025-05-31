from sympy import sympify, solve
from sympy.abc import x

def ask_math_bot(question):
    try:
        expression = sympify(question)
        if expression.free_symbols:
            return str(solve(expression))
        return str(expression)
    except Exception as e:
        return f"Sorry, I couldn't understand that math expression. Error: {e}"
