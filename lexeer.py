import ply.lex as lex
import re

# Lista de nombres de tokens
tokens = [
    # Palabras reservadas
    'EQUIPOS', 'VERSION', 'FIRMA_DIGITAL', 'NOMBRE_EQUIPO', 'IDENTIDAD_EQUIPO', 'DIRECCION', 'LINK',
    'CARRERA', 'ASIGNATURA', 'UNIVERSIDAD_REGIONAL', 'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS',
    'NOMBRE', 'EDAD', 'CARGO', 'FOTO', 'EMAIL', 'HABILIDADES', 'SALARIO', 'ACTIVO', 'ESTADO',
    'RESUMEN', 'TAREAS', 'FECHA_INICIO', 'FECHA_FIN', 'VIDEO', 'CONCLUSION',
    # Valores literales
    'TODO', 'INPROGRESS', 'CANCELED', 'DONE', 'ONHOLD',
    'PRODUCT_ANALYST', 'PROJECT_MANAGER', 'UX_DESIGNER', 'MARKETING', 'DEVELOPER', 'DEVOPS', 'DB_ADMIN',
    # Símbolos
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA',
    # Tipos de datos
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'URL', 'EMAIL_TYPE', 'DATE'
]

# Diccionario de palabras reservadas y valores literales
reserved = {
    "equipos": "EQUIPOS",
    "version": "VERSION",
    "firma_digital": "FIRMA_DIGITAL",
    "nombre_equipo": "NOMBRE_EQUIPO",
    "identidad_equipo": "IDENTIDAD_EQUIPO",
    "dirección": "DIRECCION",
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
    "fecha_inicio": "FECHA_INICIO",
    "fecha_fin": "FECHA_FIN",
    "video": "VIDEO",
    "conclusion": "CONCLUSION",
    # Valores literales
    "To do": "TODO",
    "In progress": "INPROGRESS",
    "Canceled": "CANCELED",
    "Done": "DONE",
    "On hold": "ONHOLD",
    "Product Analyst": "PRODUCT_ANALYST",
    "Project Manager": "PROJECT_MANAGER",
    "UX designer": "UX_DESIGNER",
    "Marketing": "MARKETING",
    "Developer": "DEVELOPER",
    "Devops": "DEVOPS",
    "DB admin": "DB_ADMIN"
}

# Reglas para símbolos
t_DOS_PUNTOS = r':'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Reglas para tipos de datos y valores
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # Aquí puedes agregar validaciones para fechas, emails, urls, etc.
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"[Error léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para reconocer palabras reservadas y valores literales
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_ ]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Puedes agregar reglas específicas para EMAIL, URL, DATE si lo deseas
if __name__ == "__main__":
    import sys

    # Si se pasa un archivo como argumento, lo lee; si no, lee desde consola
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        print("Ingrese el texto a analizar:")
        data = ""
        try:
            while True:
                line = input()
                data += line + "\n"
        except EOFError:
            pass

    # Cargar el texto en el lexer
    lexer.input(data)

    # Imprimir los tokens encontrados
    print("\nTokens encontrados:")
    for token in lexer:
        print(f"{token.type}({token.value}) en línea {token.lineno}")
        