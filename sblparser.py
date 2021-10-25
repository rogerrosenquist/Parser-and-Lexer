from sly import Parser
from sbllexer import SblLexer

# Will need this for variable parsing later
variables = {}

# I could print it here, but I'll just pass for now
class SemanticError(Exception):
    pass

# Regular node class
class Node:

    def __init__(self):
        print("regular node")

    def evaluate(self):
        return 0

    def execute(self):
        return 0

# Node for a boolean value
class BooleanNode(Node):

    def __init__(self, a):
        if a == 'True':
            self.value = True

        elif a == 'False':
            self.value = False

    def evaluate(self):
        return self.value

# Node for a Number - could be an int or float
class NumberNode(Node):

    def __init__(self, a):
        if ('.' in a or 'e' in a):
            self.value = float(a)
            
        else:
            self.value = int(a)

    def evaluate(self):
        return self.value

    def setValue(self, value):
        self.value = value

# Node for a String
class StringNode(Node):
    def __init__(self, a):

        # Need to cut off quote parts of the input for a proper string
        self.a = a[1:len(a) - 1]

    def evaluate(self):
        return self.a

# Node class for lists
class ListNode(Node):

    def __init__(self, element):
        self.a = element

    # Need to be able to add to the beginning
    def preAppend(self, element):
        self.a = [element] + self.a

    # If the list isn't empty, create a list, add in values, return it
    # If it's empty, just return an empty list
    def evaluate(self):
        if self.a is not None:
            temp = []
            for b in self.a:
                temp.append(b.evaluate())
            return temp

        else:
            return []

# Class to index lists properly
class ListIndexNode(Node):

    def __init__(self, b, a):
        self.listValue = b
        self.index = a

    # Make sure that there are no semantic errors in the formatting, then return 
    def evaluate(self):
        if not (isinstance(self.listValue, ListNode) or isinstance(self.listValue, ListIndexNode)
            or isinstance(self.listValue, StringNode) ):
            raise SemanticError('Semantic Error!')

        if self.index.evaluate() >= len(self.listValue.evaluate()):
            raise SemanticError('Semantic Error!')

        if not isinstance(self.index.evaluate(), int):
            raise SemanticError('Semantic Error!')

        return self.listValue.evaluate()[self.index.evaluate()]

# For operations that only require one expression to execute
class OneOperation(Node):

    def __init__(self, operation, a):
        self.operation = operation
        self.a = a

    def evaluate(self):
        if self.operation == '-':

            # Make sure it's a number
            if not isinstance(self.a.evaluate(), (int, float)):
                raise SemanticError("Semantic Error!")

            return self.a.evaluate() * -1

        elif self.operation == 'not':

            # Make sure it's a boolean
            if not isinstance(self.a.evaluate(), bool):
                raise SemanticError("Semantic Error!")

            return not self.a.evaluate()

# Basically need to see what operation is being done, then check for all valid types of invoking it
# If it reaches the end of the if-else then throw semantic error
class TwoOperation(Node):

    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right
    
    def evaluate(self):
        if (self.operation == '+'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne + valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne + valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne + valueTwo

            elif isinstance(valueOne, list) and isinstance(valueTwo, list):
                return valueOne + valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne + valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne + valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == '-'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne - valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne - valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne - valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne - valueTwo

            else:
                raise SemanticError()

        elif (self.operation == '*'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne * valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne * valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne * valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne * valueTwo

            else:
                raise SemanticError()

        elif (self.operation == '/'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueTwo, int) or isinstance(valueTwo, int) and valueTwo == 0:
                raise SemanticError("Dividing by 0!")

            if isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne / valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne / valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne / valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne / valueTwo

            else:
                raise SemanticError("Semantic Error!")

        elif (self.operation == 'div'):
            return self.left.evaluate() // self.right.evaluate()

        elif (self.operation == 'mod'):
            return self.left.evaluate() % self.right.evaluate()

        elif (self.operation == '>'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne > valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne > valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne > valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne > valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne > valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == '<'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne < valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne < valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne < valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne < valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne < valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == '<='):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne <= valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne <= valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne <= valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne <= valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne <= valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == '>='):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne >= valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne >= valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne >= valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne >= valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne >= valueTwo

            else:
                raise SemanticError('Semantic Error!')
            
        elif (self.operation == '<>'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne != valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne != valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne != valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne != valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne != valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == '**'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne ** valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne ** valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne ** valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne ** valueTwo
            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == '=='):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, str) and isinstance(valueTwo, str):
                return valueOne == valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, int):
                return valueOne == valueTwo

            elif isinstance(valueOne, float) and isinstance(valueTwo, float):
                return valueOne == valueTwo

            elif isinstance(valueOne, int) and isinstance(valueTwo, float):
                return valueOne == valueTwo
                
            elif isinstance(valueOne, float) and isinstance(valueTwo, int):
                return valueOne == valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == 'andalso'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, bool) and isinstance(valueTwo, bool):
                return valueOne and valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif (self.operation == 'orelse'):
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueOne, bool) and isinstance(valueTwo, bool):
                return valueOne or valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif self.operation == 'in':
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if (isinstance(valueTwo, str) and isinstance(valueOne, str)) or isinstance(valueTwo, list):
                return valueOne in valueTwo

            else:
                raise SemanticError('Semantic Error!')

        elif self.operation == '::':
            valueOne = self.left.evaluate()
            valueTwo = self.right.evaluate()

            if isinstance(valueTwo, list):
                return [valueOne] + self.right.evaluate()

            else:
                raise SemanticError('Semantic Error!')

# Node Class for Tuples
class TupleNode(Node):

    def __init__(self, b):
        self.a = b

    def evaluate(self):
        return tuple(self.a.evaluate())

# Class to index tuples properly
class IndexOfTupleNode(Node):

    def __init__(self, t, index):
        self.t = t
        self.index = index

    def evaluate(self):
        if not((isinstance(self.t, TupleNode) or isinstance(self.t, ListIndexNode) or isinstance(self.t, VariableNode)) and isinstance(self.index.evaluate(), int)):
            raise SemanticError('Semantic Error!')

        if isinstance(self.index.evaluate(), int):
            if self.index.evaluate() >= len(self.t.evaluate()):
                raise SemanticError('Semantic Error!')

            return self.t.evaluate()[self.index.evaluate() - 1]

# Node class to print 
class PrintNode(Node):

    def __init__(self, a):
        self.value = a

    def evaluate(self):
        print(self.value.evaluate())

# Node class to evaluate a block of statements
class BlockNode(Node):
    
    def __init__(self, a):
        self.evalList = a

    def evaluate(self):
        if self.evalList is None:
            return

        for statement in self.evalList:
            statement.evaluate()

# Does a simple while block based on a conditional
class WhileNode(Node):

    def __init__(self, continueCondition, whileSection):
        self.continueCondition = continueCondition
        self.whileSection = whileSection

    def evaluate(self):
        while(self.continueCondition.evaluate()):
            self.whileSection.evaluate()

# Does a simple if block based on conditional
class IfNode(Node):

    def __init__(self, continueCondition, ifSection):
        self.continueCondition = continueCondition
        self.ifSection = ifSection

    def evaluate(self):
        if self.continueCondition.evaluate():
            self.ifSection.evaluate()

# Does a simple if-else block based on a conditional
class IfElseNode(Node):

    def __init__(self, continueCondition, ifSection, elseSection):
        self.continueCondition = continueCondition
        self.ifSection = ifSection
        self.elseSection = elseSection

    def evaluate(self):
        if self.continueCondition.evaluate():
            self.ifSection.evaluate()

        else:
            self.elseSection.evaluate()

# Node class for Variables
class VariableNode(Node):

    def __init__(self, variable):
        self.name = variable

    def evaluate(self):
        value = variables.get(self.name)
        if value is None:
            raise SemanticError()

        else:
            return value

    # Need a way to put at the beginning
    def preAppend(self, element):
        if isinstance(self.evaluate(), list):
            variables[self.name] = [element] + variables.get(self.name)

# Properly indexing of variables, needed for AssignNode
class IndexOfVariableNode(Node):

    def __init__(self, variable, index):
        self.variable = variable
        self.index = index

    # Make sure that no semantic errors (not an int, out of bounds, etc) exist
    def evaluate(self):
        if not isinstance(self.index.evaluate(), int):
            raise SemanticError('Semantic Error!')

        if self.index.evaluate() >= len(self.variable.evaluate()):
            raise SemanticError('Semantic Error!')

        if not (isinstance(self.variable, VariableNode) or isinstance(self.variable, IndexOfVariableNode)):
            print(type(self.variable))
            raise SemanticError('Semantic Error!')

        if not (isinstance(self.variable.evaluate(), list) or isinstance(self.variable.evaluate(), str)):
            raise SemanticError('Semantic Error!')

        return self.variable.evaluate()[self.index.evaluate()]

# Assign node for assigning variables
class AssignNode(Node):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    # This looks pretty confusing, but it's just indexing variables based on what it's evaluating
    def evaluate(self):
        if isinstance(self.variable, IndexOfVariableNode):

            if isinstance(self.variable.variable, VariableNode):
                variables[self.variable.variable.name][self.variable.index.evaluate()] = self.value.evaluate()

            elif isinstance(self.variable.variable, IndexOfVariableNode):
                variables[self.variable.variable.variable.name][self.variable.variable.index.evaluate()][self.variable.index.evaluate()] = self.value.evaluate()

            else:
                raise SemanticError('Semantic Error!')

        else:
            variables[self.variable.name] = self.value.evaluate()

# Context Sensitive Node
class CSLNode(Node):

    def __init__(self, a1, a2):
        self.left = a1
        self.right = a2

    # Not entirely sure how to do this, but it's not breaking anything?
    def appendAnElement(self, element):
        self.append(element)

    def evaluate(self):
        if isinstance(self.left, CSLNode):
            return self.left.evaluate() + [self.right.evaluate()]

        else:
            return [self.left.evaluate(), self.right.evaluate()]



class SblParser(Parser):
    
    # Tokens from the lexer
    tokens = SblLexer.tokens

    # Order of operations
    precedence = (
        ('left', 'ORELSE'),
        ('left', 'ANDALSO'),
        ('left', 'NOT'),
        ('left', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ'),
        ('right', 'CONS'),
        ('left', 'IN'),
        ('left', '+', '-'),
        ('left', '*', '/', 'DIV', 'MOD'), 
        ('right', 'EXPONENTIAL'),
        ('right', 'UMINUS'),
    )
  
    # Init with empty dict
    def __init__(self):
        self.envDict = { }

    # PRINT SECTION

    @_('print_statement')
    def statement(self, a):
        return a.print_statement
    
    @_('PRINT "(" expression ")" SEMICOLON')
    def print_statement(self, a):
        return PrintNode(a.expression)
  
    # VARIABLE SECTION

    @_('variable_assign')
    def statement(self, a):
        return a.variable_assign
  
    @_('variable ASSIGN expression SEMICOLON')
    def variable_assign(self, a):
        return AssignNode(a.variable, a.expression)
    
    @_('variable "[" expression "]" ASSIGN expression SEMICOLON')
    def variable_assign(self, a):
        return AssignNode(IndexOfVariableNode(a.variable, a.expression0), a.expression1)

    @_('variable')
    def expression(self, a):
        return a.variable
        
    @_('VARIABLE')
    def variable(self, a):
        return VariableNode(a.VARIABLE)

    # BLOCK SECTION

    @_('block')
    def statement(self, a):
        return a.block

    @_('"{" statement_list "}"')
    def block(self, a):
        return BlockNode(a.statement_list)

    @_('"{" "}"')
    def block(self, a):
        return BlockNode(None)

    # STATEMENTS SECTION

    @_('statement statement_list')
    def statement_list(self, a):
        return [a.statement] + a.statement_list 
    
    @_('statement')
    def statement_list(self, a):
        return [a.statement]

    @_('if_statement')
    def statement(self, a):
        return a.if_statement

    @_('IF "(" expression ")" block')
    def if_statement(self, a):
        return IfNode(a.expression, a.block)

    @_('while_statement')
    def statement(self, a):
        return a.while_statement
    
    @_('WHILE "(" expression ")" block')
    def while_statement(self, a):
        return WhileNode(a.expression, a.block)

    @_('ifelse_statement')
    def statement(self, a):
        return a.ifelse_statement

    @_('IF "(" expression ")" block ELSE block')
    def ifelse_statement(self, a):
        return IfElseNode(a.expression, a.block0, a.block1)

   # ARRAY SECTION

    @_('array')
    def expression(self, a):
        return (a.array)

    @_('"[" "]"')
    def array(self, a):
        return ListNode([])
    
    @_('array "[" expression "]"')
    def array(self, a):
        return ListIndexNode(a.array, a.expression)

    @_('tuple')
    def expression(self, a):
        return a.tuple

    @_('"#" expression tuple')
    def tuple(self, a):
        return IndexOfTupleNode(a.tuple, a.expression)

    @_('"(" csl ")"')
    def tuple(self, a):
        return TupleNode(a.csl)

    @_('expression "," expression ","')
    def csl(self, a):
        return CSLNode(a.expression0, a.expression1)
    
    @_('csl expression ","')
    def csl(self, a):
        return CSLNode(a.csl, a.expression)
    
    # EXPRESSION SECTION

    @_('expression')
    def statement(self, a):
        return (a.expression)

    @_('"[" expression_list "]"')
    def array(self, a):
        return ListNode(a.expression_list)

    @_('expression')
    def expression_list(self, a):
        return [a.expression]

    @_('"(" expression ")"')
    def expression(self, a):
        return a.expression

    @_('expression "," expression_list')
    def expression_list(self, a):
        return [a.expression] + a.expression_list

    @_('expression "[" expression "]"')
    def expression(self, a):
        return IndexOfVariableNode(a.expression0, a.expression1)
    
    @_('NOT expression')
    def expression(self, a):
        return OneOperation(a[0], a.expression)

    @_('"-" expression %prec UMINUS')
    def expression(self, a):
        return OneOperation(a[0], a.expression)

    # Simple operations that need two expressions
    @_( 'expression ANDALSO expression',
        'expression ORELSE expression',
        'expression IN expression',
        'expression CONS expression',
        'expression "+" expression',
        'expression "-" expression',
        'expression "*" expression',
        'expression "/" expression',
        'expression EXPONENTIAL expression',
        'expression "<" expression',
        'expression ">" expression',
        'expression DIV expression',
        'expression MOD expression',
        'expression EQ expression',
        'expression NE expression',
        'expression LT expression',
        'expression LE expression',
        'expression GT expression',
        'expression GE expression')
    def expression(self, a):
        return TwoOperation(a[1], a.expression0, a.expression1)

    # Last bit of methods

    @_('NUMBER')
    def expression(self, a):
        return NumberNode(a.NUMBER)
        
    @_('BOOLEAN')
    def expression(self, a):
        return BooleanNode(a.BOOLEAN)

    @_('string')
    def expression(self, a):
        return a.string

    @_('STRING')
    def string(self, a):
        return StringNode(a.STRING)

    @_('string "[" expression "]"')
    def string(self, a):
        return ListIndexNode(a.string, a.expression)