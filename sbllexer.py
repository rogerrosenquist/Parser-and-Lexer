from sly import Lexer

class SblLexer(Lexer):
    
    # Ignore these things
    ignore = '\t '
    ignore_comment = r'\#.*'

    # Set of literals 
    literals = { '=', '+', '-', '/', '<', '>', 
                '*', '(', ')', ',', '[', ']', '{', '}', '#'}

    # The tokens the parser will be using
    tokens = {  ANDALSO, PRINT, FUN, ASSIGN, EQ, SEMICOLON,
                VARIABLE, NUMBER, STRING, BOOLEAN,
                EXPONENTIAL, NE, LE, LT, GE, GT,
                IF, ELSE, WHILE,
                MOD, NOT, IN, ORELSE, DIV, CONS}

    # RE logic for the tokens
    EXPONENTIAL = r'\*\*'
    DIV     = r'div'
    MOD     = r'mod'
    EQ      = r'=='
    ASSIGN  = r'='
    NE      = r'<>'
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    ANDALSO = r'andalso'
    NOT     = r'not'
    PRINT   = r'print'
    IF      = r'if'
    ORELSE  = r'orelse'
    ELSE    = r'else'
    WHILE   = r'while'
    IN      = r'in'
    CONS    = r'::'
    SEMICOLON = r';'

    # Slightly more complex RE logic for specific tokens
    VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER  = r'[\d.]+(?:e-?\d+)?'
    STRING = r"['\"](.*?)['\"]"
    BOOLEAN = r'(True|False)'

    # Keeps track of line number
    @_(r'\n+')
    def ignore_newline(self, a):
        self.lineno = a.value.count('\n')