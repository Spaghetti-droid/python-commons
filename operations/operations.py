# Classes used for operations. Namely Number and Operation, as well as Operation's descendants

HIGHEST_PRIORITY = 1
LOWEST_PRIORITY = 3

class Number:
    """Stores a number value as well as any neighbouring operations
    """
    def __init__(self, value) -> None:
        self.value = float(value)
        self.leftOp = None
        self.rightOp = None

class Operation:
    """Represents an operation and stores the neighbouring numbers it can act on
    """
    priority = -1
    
    def __init__(self, leftNumber=None, rightNumber=None) -> None:
        self.leftNumber = self.setLeftNumber(leftNumber)
        self.rightNumber = self.setRightNumber(rightNumber)
    
    def setRightNumber(self, number:Number) -> None:
        """Specify the number on the right of the operator
        Also updates the number's left operator to match self

        Args:
            number (Number)
        """
        if not number:
            return
        self.rightNumber = number
        number.leftOp = self
        
    def setLeftNumber(self, number:Number) -> None:
        """Specify the number on the left of the operator
        Also updates the number's right operator to match self

        Args:
            number (Number)
        """
        if not number:
            return
        self.leftNumber = number
        number.rightOp = self
        
    def getNewValue(self) -> float:
        """Calculates the result of the operation applied to left and right numbers

        Returns:
            float: The result of the operation
        """
        raise ValueError("Generic operation can't apply")
    
    def apply(self) -> Number:
        """Apply the operation on the two numbers and links the result to the remaining operators on either side of the operands

        Returns:
            Number: The result of the operation, linked to any surrounding operators
        """
        value = self.getNewValue()
        newLeftOp = self.leftNumber.leftOp
        newRightOp = self.rightNumber.rightOp
        newNumber = Number(value)
        if newLeftOp:
            newLeftOp.setRightNumber(newNumber)
        if newRightOp:
            newRightOp.setLeftNumber(newNumber)
        return newNumber
        
    
class Power(Operation):
    priority = 1
    
    def getNewValue(self) -> float:
        return self.leftNumber.value**self.rightNumber.value
    
class Multiply(Operation):
    priority=2
    
    def getNewValue(self) -> float:
        return self.leftNumber.value*self.rightNumber.value
    
class Divide(Operation):
    priority=2
    
    def getNewValue(self) -> float:
        return self.leftNumber.value/self.rightNumber.value
    
class Add(Operation):
    priority=3
    
    def getNewValue(self) -> float:
        return self.leftNumber.value+self.rightNumber.value
        
class Substract(Operation):
    priority=3
    
    def getNewValue(self) -> float:
        return self.leftNumber.value-self.rightNumber.value