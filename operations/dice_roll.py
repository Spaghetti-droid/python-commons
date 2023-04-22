# For all code linked to dice rolling and calculation

import re
import random
import calcultation as c

DICE_REGEXP = r"(\d+)d(\d+)"    #TODO Add (NOT .) OR start condition

def rollAndCalculate(expr:str) -> tuple:
    """Execute expression, first resolving all dice rolls, then calculating a result

    Args:
        expr (str): The expression to evaluate

    Returns:
        tuple: (The expression with dice replaced by their rolls, the result of the evaluation)
    """
    expr = rollDice(expr)
    val = c.calculate(expr)
    return (expr, val)

def rollDice(expr: str) -> str: 
    """Replaces all NdN parts of expr with a sum of dice roll values

    Args:
        expr (str): The expression to evaluate

    Returns:
        str: the expression with dice rolls subbed out for their results
    """
    return re.sub(DICE_REGEXP, lambda x: roll(int(x.group(1)), int(x.group(2))), expr)

def roll(numberOfDice: int, limit:int) -> str:
    """Performs a dice roll and returns all roll values seperated by + and between parentheses

    Args:
        numberOfDice (int): Number of dice to throw
        limit (int): Value of said dice

    Returns:
        str: Rolls in the following format (v1 + v2 + ... + vn)
    """
    return '(' + ' + '.join(str(random.randint(1, limit)) for r in range(numberOfDice)) + ')'
                
        
