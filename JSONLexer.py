import ply.lex as lex
 
 # List of token names.   This is always required
tokens = (
        'TYPE',
        'STRUCT',
        'NOMBRE',
        'TYPESTRING',
        'TYPEINT',
        'TYPEFLOAT',
        'TYPEBOOL',
        'LBRACKET',
        'RBRACKET',
        'ARRLOCKS'
     )
 
# Regular expression rules for simple tokens
 #   t_STRUCT  = 'struct'
t_LBRACKET  = r'\{'
t_RBRACKET  = r'\}'
t_ARRLOCKS = r'\[]'
     
     
 
     # A regular expression rule with some action code
     # Note addition of self parameter since we're in a class
     
def t_TYPE(t):
    r'type'
    return t
     
def t_TYPESTRING(t):
    r'string'
    return t
      
def t_TYPEINT(t):
    r'int'
    return t
     
def t_TYPEFLOAT(t):
    r'float64'
    return t
     
def t_TYPEBOOL(t):
    r'bool'
    return t
        
def t_STRUCT(t): 
    r'struct'
    return t
         
def t_NOMBRE(t): 
    r'[a-zA-Z0-9\.\,\-\_\~\+\´]+'
    return t
    
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
     # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
     # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return 'ERROR'
 
     # Build the lexer
   #  def build(self,**kwargs):
    #     self.lexer = lex.lex(module=self, **kwargs)
     
     # Test it output
def test(data):
    while True:
        tok = lexer.token()
        if not tok: 
            break
        print(tok)



#file1 = open('ejemplo_3.txt', 'r')
#text = file1.read()
#file1.close()
    

lexer = lex.lex()
#lexer.input(text)
#test(text)