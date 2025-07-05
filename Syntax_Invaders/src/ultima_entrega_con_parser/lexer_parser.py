import ply.lex as lex
import ply.yacc as yacc
import re

# ----------------- LEXER -----------------
reserved = {
    "equipos": "LISTA_EQUIPOS",
    "nombre_equipo": "NOMBRE_EQUIPO",
    "identidad_equipo": "IDENTIDAD_EQUIPO",
    "link": "CLAVE_LINK",
    "asignatura": "ASIGNATURA",
    "carrera": "CARRERA",
    "universidad_regional": "UNIVERSIDAD_REGIONAL",
    "dirección": "DIRECCION",
    "alianza_equipo": "ALIANZA_EQUIPO",
    "integrantes": "INTEGRANTES",
    "proyectos": "PROYECTOS",
    "nombre": "NOMBRE",
    "edad": "EDAD",
    "cargo": "CARGO",
    "foto": "FOTO",
    "email": "CLAVE_EMAIL",
    "habilidades": "HABILIDADES",
    "salario": "SALARIO",
    "activo": "ACTIVO",
    "estado": "ESTADO",
    "resumen": "RESUMEN",
    "tareas": "TAREAS",
    "fecha_inicio": "FECHA_INICIO",
    "fecha_fin": "FECHA_FIN",
    "video": "VIDEO",
    "conclusion": "CONCLUSION",
    "calle": "CALLE",
    "ciudad": "CIUDAD",
    "país": "PAIS",
    "version": "VERSION",
    "firma_digital": "FIRMA_DIGITAL"
}

tokens = [
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'FECHA', 'CLAVE_EMAIL', 'EMAIL', 'URL',
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CLAVE_LINK', 'CORCHETE_DER', 'COMA', 'LISTA_EQUIPOS', 'NOMBRE_EQUIPO', 
    'IDENTIDAD_EQUIPO', 'LINK', 'ASIGNATURA', 'CARRERA', 'UNIVERSIDAD_REGIONAL',
    'DIRECCION', 'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS', 'NOMBRE', 'EDAD', 'CARGO', 'FOTO',
    'HABILIDADES', 'SALARIO', 'ACTIVO', 'ESTADO', 'RESUMEN', 'TAREAS', 'FECHA_INICIO', 'FECHA_FIN', 'VIDEO',
    'CONCLUSION', 'CALLE', 'CIUDAD', 'PAIS', 'VERSION', 'FIRMA_DIGITAL',
]

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_EMAIL(t):
    r'\"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\"'
    t.value = t.value.strip('"')
    return t

def t_FECHA(t):
    r'\"(19[0-9]{2}|20[0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\"'
    t.value = t.value.strip('"')
    return t

def t_URL(t):
    r'\"(http|https):\/\/[a-zA-Z0-9\.\-\/\_\?\=\&\#\:]+\"'
    t.value = t.value.strip('"')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

t_COMA = r','
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_DOS_PUNTOS = r':'

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    valor = t.value.strip('"')
    if valor in reserved:
        t.type = reserved[valor]
        t.value = valor
    else:
        t.type = "STRING"
    t.value = valor
    return t

def t_error(t):
    # No imprimir, solo saltar
    t.lexer.skip(1)

# ----------------- PARSER -----------------
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
    '''par : clave DOS_PUNTOS valor'''
    p[0] = (p[1], p[3])

def p_clave(p):
    '''clave : STRING
             | CLAVE_LINK
             | CLAVE_EMAIL
             | LISTA_EQUIPOS
             | NOMBRE_EQUIPO
             | IDENTIDAD_EQUIPO
             | ASIGNATURA
             | CARRERA
             | UNIVERSIDAD_REGIONAL
             | DIRECCION
             | ALIANZA_EQUIPO
             | INTEGRANTES
             | PROYECTOS
             | NOMBRE
             | EDAD
             | CARGO
             | FOTO
             | HABILIDADES
             | SALARIO
             | ACTIVO
             | ESTADO
             | RESUMEN
             | TAREAS
             | FECHA_INICIO
             | FECHA_FIN
             | VIDEO
             | CONCLUSION
             | CALLE
             | CIUDAD
             | PAIS
             | VERSION
             | FIRMA_DIGITAL
    '''
    p[0] = p[1]

def p_objeto(p):
    'objeto : LLAVE_IZQ elementos LLAVE_DER'
    p[0] = dict(p[2])

def p_lista(p):
    'lista : CORCHETE_IZQ valores CORCHETE_DER'
    p[0] = p[2]

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

lexer = lex.lex()
parser = yacc.yacc()

# ----------------- FUNCIONES PARA LA INTERFAZ -----------------

def imprimir_tokens(texto):
    lexer.input(texto)
    lineas = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        lineas.append(f"Se encontró el token {tok.type} con valor '{tok.value}' en la línea {tok.lineno}")
    return lineas

def analizar_sintaxis(texto):
    return parser.parse(texto)

def pretty_print_tree(tree, indent=0):
    result = ""
    if isinstance(tree, dict):
        for k, v in tree.items():
            result += '  ' * indent + f"{k}:\n"
            result += pretty_print_tree(v, indent + 1)
    elif isinstance(tree, list):
        for i, item in enumerate(tree):
            result += '  ' * indent + f"- [{i}]\n"
            result += pretty_print_tree(item, indent + 1)
    else:
        result += '  ' * indent + str(tree) + "\n"
    return result