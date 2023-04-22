# For all code linked to dice rolling

import re
import random
import commons.operations.calculation as c

# Deliberately capture '.'s because it allows us to handle the error or ignore it more easily
DICE_REGEXP = r"([\d\.]+)d([\d\.]+)" 

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
        expr (str): The expression to evaluate. 
            Note that floating point values for number of dice or limit will be cast as ints.

    Returns:
        str: the expression with dice rolls subbed out for their results
    """
    return re.sub(DICE_REGEXP, lambda x: roll(x.group(1), x.group(2)), expr)

def roll(numberOfDice, limit) -> str:
    """Performs a dice roll and returns all roll values seperated by + and between parentheses

    Args:
        numberOfDice (int): Number of dice to throw
        limit (int): Value of said dice

    Returns:
        str: Rolls in the following format (v1 + v2 + ... + vn)
    """
    try:
        intLimit = int(limit)
        intNumberOfDice = int(numberOfDice)
    except ValueError as e:
        raise ValueError('\'' + numberOfDice + 'd' + limit + '\' is not in NdN format!')
    return '(' + ' + '.join(str(random.randint(1, intLimit)) for r in range(intNumberOfDice)) + ')'

def main():
    print(rollAndCalculate('2d5-2'))
    print(rollAndCalculate('3'))
    print(rollAndCalculate('2**(9/3*4)+3--2*6/3'))
    print(rollAndCalculate('5*ddd6+dddd-2'))
if __name__ == '__main__':
    main()
                
        
