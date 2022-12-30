import ply.yacc as yacc 
from JSONLexer import tokens
import random as rn
import string
import json
import sys

types = {}
JSON_Name = None
padres = {}
letters = string.ascii_lowercase


def p_start(p):
    'start : TYPE NOMBRE STRUCT LBRACKET atrib types' 
    global JSON_Name 
    JSON_Name = p[2]
    
    
    if p[2] in types:
        print('El tipo "{0}" se intenta definir 2(o mas) veces'.format(p[2]))
        sys.exit(0)
    values_atrib = [x[0] for x in p[5].values() if type(x) == tuple]
    if p[2] in values_atrib:
        print('Se detecto una referencia circular al definir el tipo "{0}" como atributo'.format(p[2]))
        sys.exit(0)
     
    types[p[2]] = p[5]
    
   
def p_types_none(p):
    'types : '


def p_types(p):
    'types : TYPE NOMBRE vartype types'    
    if p[2] in types:
        print('el tipo "{0}" se intenta declarar 2(o mas) veces'.format(p[2]))
        sys.exit(0)

    types[p[2]] = (p[3]['tipo'],p[3]['dim'])


def p_types_struct(p):
    'types : TYPE NOMBRE STRUCT LBRACKET atrib types'    
    if p[2] in types:
        print('el tipo "{0}" se intenta declarar 2(o mas) veces'.format(p[2]))
        sys.exit(0)
    values_atrib = [x[0] for x in p[5].values() if type(x) == tuple]
    if p[2] in values_atrib:
        print('Se detecto una referencia circular al definir el tipo "{0}" como atributo'.format(p[2]))
        sys.exit(0)
    
    types[p[2]] = p[5]
    

def p_atrib(p):
    'atrib : NOMBRE vartype atrib'
    p[0] = {p[1] : (p[2]['tipo'],p[2]['dim'])}
    
    if p[1] in p[3]:
        print('Atributo "{0}" se intenta repetir en un mismo struct'.format(p[1]))
        sys.exit(0)
    
    p[0].update(p[3])
    
def p_atrib_brack(p):
    'atrib : RBRACKET'
    p[0] = {}
    
def p_atrib_struct(p):
    'atrib : NOMBRE STRUCT LBRACKET atrib2 RBRACKET atrib'
    
    values_atrib = [x[0] for x in p[4].values() if type(x) == tuple]
    if p[1] in values_atrib:
        print('Se detecto referencia circular dentro del struct anonimo "{0}"'.format(p[2]))
        sys.exit(0)
        
    #types[p[2]] = p[4]
    p[0] = {p[1]:p[4]}
    p[0].update(p[6])

def p_atrib2(p):
    'atrib2 : NOMBRE vartype atrib2'
    if p[1] in p[3]:
        print('Atributo "{0}" se intenta repetir en un mismo struct anonimo'.format(p[1]))
        sys.exit(0)
    
    p[0] = {p[1] : (p[2]['tipo'],p[2]['dim'])}
    p[0].update(p[3])
 
def p_atrib2_none(p):
    'atrib2 : '
    p[0] = {}

def p_vartype(p):
    'vartype : ARRLOCKS vartype'
    p[0] = {}
    p[0]['tipo'] = p[2]['tipo']
    p[0]['dim'] = 1 + p[2]['dim']

def p_vartype_int(p):
    'vartype : TYPEINT'
    p[0] = {'tipo': p[1], 'dim': 0}

def p_vartype_float(p):
    'vartype : TYPEFLOAT'
    p[0] = {'tipo': p[1], 'dim': 0}

def p_vartype_string(p):
    'vartype : TYPESTRING'
    p[0] = {'tipo': p[1], 'dim': 0}
    
def p_vartype_bool(p):
    'vartype : TYPEBOOL'
    p[0] = {'tipo': p[1], 'dim': 0}

def p_vartype_struct(p):
    'vartype : NOMBRE'
    p[0] = {'tipo': p[1], 'dim': 0}


def p_error(p):
    print("error de sintaxis en la linea: ", p.lineno)
    sys.exit(0)


def rand_value(t):
    if t == JSON_Name:
        print('"{0}" definido recursivamente'.format(t))
        sys.exit(0)
    if t == 'int':
        return rn.randint(0,100)
    elif t == 'string':
        return ''.join(rn.choice(letters) for i in range(10))
    elif t == 'bool':
        b = rn.randint(0, 1)
        if b == 0:
            return False
        else:
            return True
    elif t == 'float64':
        return round(rn.uniform(0,10),3)
    elif t in types and type(types[t]) == tuple:
        return rand_val_or_list(types[t][0], types[t][1])
    elif t in types and type(types[t]) == dict:
        return create_json(types[t])
    else:
        print('No existe el tipo "{0}"'.format(t))
        sys.exit(0)


def rand_val_or_list(t,d):
    if d == 0:
        return rand_value(t)
    r = rn.randint(0, 5)
    return [rand_val_or_list(t, d-1) for i in range(r)]


def create_json(dicc):
    d_json = {}
    for key in dicc:
        if type(dicc[key]) == tuple:
            d_json[key] = rand_val_or_list(dicc[key][0], dicc[key][1])
        else:
            d_json[key] = create_json(dicc[key])
    
    return d_json

def check(atrib,name):
    if type(atrib) == dict:
        for k in atrib:
            if type(atrib[k]) == tuple:
                t = atrib[k][0]
                if t == name or t == JSON_Name:
                    print('Se detectó una referencia circular')
                    sys.exit(0)
                if t in types:
                    check(types[t],name)
            else:
                check(atrib[k], name)
        
var = sys.argv[1]
#file1 = open('ejemplo.txt', 'r')
file1 = open(var, 'r')
text = file1.read()
file1.close()


parser = yacc.yacc()

result = parser.parse(text)

#cheaquemos circularidad recursiva entre los tipos definidos
for k in types:
    if not(k == JSON_Name):
        check(types[k], k)

JSON_out = create_json(types[JSON_Name])
json_string = json.dumps(JSON_out)
print(json_string)

with open('json_salida.txt', 'w') as outfile:
    json.dump(JSON_out, outfile, indent=4)
