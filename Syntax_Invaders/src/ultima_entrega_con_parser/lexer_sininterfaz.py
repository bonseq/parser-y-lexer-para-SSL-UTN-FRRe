import ply.lex as lex
import re

tokens = [
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'FECHA', 'EMAIL', 'URL',
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA'
]

# Tipos especiales para validación posterior
valores_estado = ["To do", "In progress", "Canceled", "Done", "On hold"]
valores_cargo = ["Product Analyst", "Project Manager", "UX designer", "Marketing", "Developer", "Devops", "DB admin"]

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
    r'\d+\.\d{2}'
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
    t.value = t.value.strip('"')
    return t

def t_error(t):
    print(f"[Error léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()