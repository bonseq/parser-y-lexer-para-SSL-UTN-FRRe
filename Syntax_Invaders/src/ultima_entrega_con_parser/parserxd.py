import ply.yacc as yacc
from lexer_sininterfaz import tokens

def p_json(p):
    'json : LLAVE_IZQ elementos LLAVE_DER'
    p[0] = ('json', p[2])

def p_elementos(p):
    '''elementos : par
                 | elementos COMA par'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_par(p):
    'par : STRING DOS_PUNTOS valor'
    p[0] = (p[1], p[3])

def p_valor(p):
    '''valor : STRING
             | INTEGER
             | FLOAT
             | BOOL
             | NULL
             | FECHA
             | EMAIL
             | URL
             | objeto
             | lista'''
    p[0] = p[1]

def p_objeto(p):
    'objeto : LLAVE_IZQ elementos LLAVE_DER'
    p[0] = dict(p[2])

def p_lista(p):
    'lista : CORCHETE_IZQ valores CORCHETE_DER'
    p[0] = p[2]

def p_valores(p):
    '''valores : valor
               | valores COMA valor'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    if p:
        raise SyntaxError(f"[ERROR] Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        raise SyntaxError("[ERROR] Error de sintaxis al final del archivo")

parser = yacc.yacc()

def analizar_sintaxis(texto):
    """
    Recibe un string con el JSON y devuelve el árbol sintáctico.
    Lanza SyntaxError si hay error de sintaxis.
    """
    return parser.parse(texto)