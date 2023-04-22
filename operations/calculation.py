# Parsing and calculating an expression

import re
import commons.operations.operations as ops
import commons.utility as utils

# Matches a (positive or negative) number, followed by an operator
PARSE_REGEXP = r"\s*(\-?\d+(?:\.\d+)?)\s*(\*\*|[+\-\/*])?"

def calculate(expr:str) -> float:
    """Takes a mathematical expression and calculates it. Recognises **, *, /, +, and - operations as well as parentheses.
    Currently ignores all characters it doesn't recognise

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
        
    # Split string into numbers and operations. Link them together into a chain of alternating Numbers and Operations
    
    priorityToOp = {}
    previousOp = None
    noOpInPreviousMatch = False
    for numGroup, opGroup in re.findall(PARSE_REGEXP, expr):
        if noOpInPreviousMatch:
            raise ValueError('Malformed expression: ' + expr)
        
        num = ops.Number(numGroup)        
        if previousOp:
            previousOp.setRightNumber(num)
        
        if opGroup:
            op = toOperation(opGroup)
            previousOp = op
            op.setLeftNumber(num)
            utils.addToDicList(priorityToOp, op.priority, op)
        else:
            # This should always happen at the end of the expression
            noOpInPreviousMatch = True
    
    if not noOpInPreviousMatch:
        raise ValueError('Malformed expression: ' + expr)            
    
    # Execute the operations
    
    previousNum = num
    for priority in range(ops.HIGHEST_PRIORITY,ops.LOWEST_PRIORITY+1):
        if priority in priorityToOp:
            opList = priorityToOp[priority]
            for o in opList:            
                previousNum = o.apply()
    
    # The final previousNum is the last item left and also the result
    
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
            

def toOperation(token:str) -> ops.Operation:
    """Takes the input token and outputs the corresponding operation, 
    or converts the token to a float if none is found

    Args:
        token (str): Should be **,*,/,+,- or a number

    Returns:
        any: An op.Operation or a float
    """
    token = token.strip()
    match token:
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
            raise ValueError('Operation not recognised: ' + token)