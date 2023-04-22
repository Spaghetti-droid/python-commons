import re
import operations as ops
import utility

SPLIT_REGEXP = r"(\d+(?:\.\d+)?)"

def calculate(expr:str) -> float:
    """Takes a mathematical expression and calculates it. Recognises **, *, /, +, and - operations as well as parentheses

    Args:
        expr (str): The expression to evaluate

    Returns:
        float: The result of the calculation
    """
    
    expr = expr.strip()
    if not expr:
        raise ValueError('Empty expression')
    
    # First evaluate sub-expressions
    
    subExpressions = getSubexpressionIndices(expr)
    # Revert to avoid changing indices for SE's that haven't been processed yet
    subExpressions = sorted(subExpressions, key=lambda tup: tup[0], reverse=True)
    for subStart, subEnd in subExpressions:
        expr = expr[:subStart] + str(calculate(expr[subStart+1:subEnd-1])) + expr[subEnd:]
        
    # Split string into tokens and numbers. Convert the former to Operations and the latter to floats
    
    # Reverse the list so that we can go through the reversed list backwards.
    # We want to deal with operations from left to right in expr, but while avoiding changing the next indices 
    splitExpr = re.split(SPLIT_REGEXP, expr)
    # Remove empty strings -_-
    splitExpr = list(filter(None, splitExpr))
    priorityToOp = {}
    previousOp = None
    previousNum = None
    for i in range(len(splitExpr)):
        t = toOperationOrFloat(splitExpr[i])
        if i % 2:           # t is op - we are assuming here that there is a number - op - number - ... alternation
            previousOp = t
            t.setLeftNumber(previousNum)
            utility.addToDicList(priorityToOp, t.priority, t)
        else:               # t is a number
            previousNum = t
            if previousOp:
                previousOp.setRightNumber(t)
            
    
    # Execute the operations
    
    for priority in range(ops.HIGHEST_PRIORITY,ops.LOWEST_PRIORITY+1):
        if priority in priorityToOp:
            opList = priorityToOp[priority]
            for o in opList:            
                previousNum = o.apply()
    
    # remaining previousNum is the last item left and also the result
    
    return previousNum.value               
    
def getSubexpressionIndices(expr:str) -> list:
    """Finds the positions of any parts of the expression which are between brackets.
    Ignores nested parentheses, so that 5 + (2 * (3-6)) would only be considered to have 1 sub expression

    Args:
        expr (str): The expression which contains parentheses

    Raises:
        ValueError: If not all opening parentheses match a closing one and vice-versa

    Returns:
        list: containing the indices which enclose the parentheses of the subexpressions found
    """
    if '(' not in expr:
        return []
    openPs = 0
    subExpressions = []
    subStart = -1
    for i in range(len(expr)):
        c = expr[i]
        if c == '(':
            if openPs == 0:
                subStart = i
            openPs+=1
        elif c == ')':  
            openPs -= 1
            if openPs < 0:
                raise ValueError("')' found with no preceding '('") 
            elif openPs == 0:
                # i+1 to include ) in subexpression
                subExpressions.append((subStart, i+1))   
    
    if openPs != 0:
        raise ValueError("'(' not closed")
    
    return subExpressions       
            

def toOperationOrFloat(token:str) -> any:
    """Takes the input token and outputs the corresponding operation, 
    or converts the token to a float if none is found

    Args:
        token (str): Should be **,*,/,+,- or a number

    Returns:
        any: An op.Operation or a float
    """
    token = token.strip()
    match token:
        #case 'd':
        #    return Roll()
        case '**':
            return ops.Power()
        case '*':
            return ops.Multiply()
        case '/':
            return ops.Divide()
        case '+':
            return ops.Add()
        case '-':
            return ops.Substract()
        case _:
            try:
                return ops.Number(token)
            except Exception:
                raise ValueError('Operation not recognised: ' + token)