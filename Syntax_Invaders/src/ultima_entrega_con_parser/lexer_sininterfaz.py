# lexer_sininterfaz.py (modificado con FECHA_INICIO y FECHA_FIN)
import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    'NOMBRE_EQUIPO', 'VERSION', 'FIRMA_DIGITAL', 'LISTA_EQUIPOS', 'IDENTIDAD_EQUIPO', 'LINK',
    'CARRERA', 'ASIGNATURA', 'UNIVERSIDAD_REGIONAL', 'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS',
    'NOMBRE', 'EDAD', 'CARGO', 'FOTO', 'EMAIL', 'HABILIDADES', 'SALARIO', 'ACTIVO', 'ESTADO',
    'RESUMEN', 'TAREAS', 'VIDEO', 'CONCLUSION', 'DIR_DET',
    'CALLE', 'CIUDAD', 'PAIS',
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA',
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'FECHA'
]

reserved = {
    "equipos": "LISTA_EQUIPOS",
    "version": "VERSION",
    "firma_digital": "FIRMA_DIGITAL",
    "nombre_equipo": "NOMBRE_EQUIPO",
    "identidad_equipo": "IDENTIDAD_EQUIPO",
    "dirección": "DIR_DET",
    "link": "LINK",
    "carrera": "CARRERA",
    "asignatura": "ASIGNATURA",
    "universidad_regional": "UNIVERSIDAD_REGIONAL",
    "alianza_equipo": "ALIANZA_EQUIPO",
    "integrantes": "INTEGRANTES",
    "proyectos": "PROYECTOS",
    "nombre": "NOMBRE",
    "edad": "EDAD",
    "cargo": "CARGO",
    "foto": "FOTO",
    "email": "EMAIL",
    "habilidades": "HABILIDADES",
    "salario": "SALARIO",
    "activo": "ACTIVO",
    "estado": "ESTADO",
    "resumen": "RESUMEN",
    "tareas": "TAREAS",
    "video": "VIDEO",
    "conclusion": "CONCLUSION",
    "calle": "CALLE",
    "ciudad": "CIUDAD",
    "país": "PAIS",
    "fecha_inicio": "FECHA",
    "fecha_fin": "FECHA"
}

# Tokens simples
t_DOS_PUNTOS = r':'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_EMAIL(t):
    r'\"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\"'
    t.value = t.value.strip('"')
    return t

def t_LINK(t):
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

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    value = t.value.strip('"')
    if value in reserved:
        t.type = reserved[value]
    else:
        t.type = "STRING"
    t.value = value
    return t

def t_error(t):
    print(f"[Error léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
