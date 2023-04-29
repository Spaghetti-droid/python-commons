# For all code linked to dice rolling

# TODO Optimise memory use and add safeguards for very big rolls (ie N>10^6)

import re
import random
import commons.operations.calculation as c

# Deliberately capture '.'s because it allows us to handle the error or ignore it more easily
DICE_REGEXP = r"([\d\.]+)d([\d\.]+)" 
# The label returned by rollAndCalculate should be limited in size
DEFAULT_MAX_LABEL_LENGTH = 2000

def rollAndCalculate(expr:str, maxLabelLength: int = DEFAULT_MAX_LABEL_LENGTH) -> tuple:
    """Execute expression, first resolving all dice rolls, then calculating a result

    Args:
        expr (str): The expression to evaluate

    Returns:
        tuple: (The expression with dice replaced by their rolls, the result of the evaluation)
    """
    expr = expandLabelPrefix(expr, maxLabelLength)
    expr = rollDice(expr)
    val = c.calculate(expr)
    return (expr, val)

def expandLabelPrefix(expr:str, maxLabelLength: int = DEFAULT_MAX_LABEL_LENGTH) -> str:
    """Takes all NdN expressions in the start or the expression and expands them until the
    resolved part of expr has length over maxLabelLength.
    For example: If expr = '6d2' and maxLabelLength = 7, this function will return someting like
        '( 1 + 2 + 4d2 )'
    where remaining rolls are not performed after the limit

    Args:
        expr (str): The expression to expand
        maxLabelLength (int, optional): How many characters in expr to expand. Measured from the start of the string. Defaults to DEFAULT_MAX_LABEL_LENGTH.

    Returns:
        str: The expanded expression
    """
    possibleLabel = expr[:maxLabelLength]
    for m in re.finditer(DICE_REGEXP, possibleLabel):
        start, end = m.span()
        labelDone, expandedRolls = expandRoll(m, maxLabelLength-start)
        expr = expr[:start] + expandedRolls + expr[end:]
        if labelDone:
            return expr
    
    return expr
        
def expandRoll(rollMatch: re.Match[str], maxLength: int) -> tuple:
    """Expand a NdN expression until it hits max length.
    For example: If rollMatch is for '6d2' and maxLength = 7, this function will return someting like
        (True, '( 1 + 2 + 4d2 )')
    where remaining rolls are not performed after the limit
    
    Args:
        rollMatch (re.Match[str]): A match object for the NdN expression. This is expected to contain
            2 groups; the first for number of dice, the second for the size of the dice
        maxLength (int): Expansion will stop if the resulting string is bigger than this limit

    Returns:
        tuple(bool, str): ( True if expansion went past limit, Expanded expression )
    """
    nDice = int(rollMatch.group(1))
    limit = int(rollMatch.group(2))
    if nDice == 0 or limit == 0:
        return (False, '( 0 )')
    
    remaining = 0
    expandedString = '( '
    for r in range(nDice-1, -1, -1):
        expandedString += str(random.randint(1, limit))
        if(len(expandedString)>maxLength):
            remaining = r
            break
        if r != 0:
            expandedString += ' + '
    
    if remaining:
        expandedString += ' + ' + str(remaining) + 'd' + str(limit)
    
    expandedString += ' )'
    
    return (remaining > 0, expandedString)           
    

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
    except ValueError:
        raise ValueError('\'' + numberOfDice + 'd' + limit + '\' is not in NdN format!')
    return str(sum(random.randint(1, intLimit) for r in range(intNumberOfDice)))
        
    
    

def main():
    import time
    start = time.perf_counter()
    print(rollAndCalculate('100000000d2', 7))
    end = time.perf_counter()
    print('Done in', end - start, 'seconds')
if __name__ == '__main__':
    main()
                
        
