import ply.lex as lex
import ply.yacc as yacc
import re

CLAVES_VALIDAS = [
    "nombre_equipo", "identidad_equipo", "dirección", "link", "carrera", "asignatura",
    "universidad_regional", "alianza_equipo", "integrantes", "proyectos",
    "nombre", "edad", "cargo", "foto", "email", "habilidades", "salario", "activo",
    "estado", "resumen", "tareas", "fecha_inicio", "fecha_fin", "video", "conclusion",
    "equipos", "version", "firma_digital", "calle", "ciudad", "país"
]

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
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
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
    errores.append(f"[ERROR LÉXICO] en la línea {t.lineno}: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

# ----------------- PARSER -----------------
CARGOv= [
    "product analyst", "project manager", "ux designer", "marketing",
    "developer", "devops", "db admin"
]
ESTADOSv= [
    "to do", "in progress", "canceled", "done", "on hold"
]
chart_PROHIBIDO="áéíóúÁÉÍÓÚñÑ"

errores=[]

EMAIL_R=r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9._\-]+\.[a-zA-Z]{2,4}$'
URL_R= r'^(http:\/\/|https:\/\/)[a-zA-Z0-9\-\._~:\/\?#\[\]@!$&\'()*+,;=%]+$'
CLAVES_URL = ["link", "identidad_equipo", "video", "foto"]

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
    'par : clave DOS_PUNTOS valor'
    clave_token = p[1]
    clave_valor = clave_token.value
    #clave correcta
    if clave_valor not in CLAVES_VALIDAS:
        errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, clave inválida o mal escrita: '{clave_valor}'")
    
    #valores correctos
    # shequeo de cargo
    if clave_valor == "cargo":
        if str(p[3]).lower() not in CARGOv:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, cargo invalido")
    
    # shequeo de estado (sin distinguir mayúsculas/minúsculas)
    if clave_valor == "estado":
        if str(p[3]).lower() not in ESTADOSv:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, estado invalido")

    #ñam caracteres sin acento o ñÑ
    if isinstance(p[3], str):
        if any(c in p[3] for c in chart_PROHIBIDO):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, palabra acentuada o con Ñ")
    #chequeo edad
    if clave_valor == "edad":
        if not (isinstance(p[3], int) and p[3] > 0):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, edad debe ser mayor a cero")

    #float siosi positivos y max dos decimales
    if isinstance(p[3], float):
        if p[3] < 0:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, numero negativo")
        else:
            # Verificar cantidad de decimales
            decimales = str(p[3]).split(".")[1]
            if len(decimales) > 2:
                errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno} , numero con mas de dos decimales")
    if isinstance(p[3], int):
        if p[3] < 0:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}")
    
    #chequeo fecha semanticamente corrcta
    if isinstance(p[3], str) and re.match(r'^\d{4}-\d{2}-\d{2}$', p[3]):
        anio, mes, dia = map(int, p[3].split('-'))
        if not (1900 <= anio <= 2099):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, anio invalido")
        if not (1 <= mes <= 12):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, mes invalido")
        if not (1 <= dia <= 31):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, dia invalido")
    
    #chequeo de email
    if clave_valor == "email":
        if not re.match(EMAIL_R, str(p[3])):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, email, invalido")
    
    if clave_valor in ["activo"]:  
        if not isinstance(p[3], bool):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, valor booleano inválido")

    # chequeo de URL
    if clave_valor in CLAVES_URL:
        if not re.match(URL_R, str(p[3])):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}")

    p[0] = (clave_valor, p[3])


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
    p[0] = p.slice[1]

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

def imprimir_arbol(arbol, nivel=0):
    resul = ""
    if isinstance(arbol, dict):
        for clave, valor in arbol.items():
            resul += '  ' * nivel + f"{clave}:\n"
            resul += imprimir_arbol(valor, nivel + 1)
    elif isinstance(arbol, list):
        if all(isinstance(elemento, tuple) and len(elemento) == 2 for elemento in arbol):
            for clave, valor in arbol:
                resul += '  ' * nivel + f"{clave}:\n"
                resul += imprimir_arbol(valor, nivel + 1)
        else:
            for indice, elemento in enumerate(arbol):
                resul += '  ' * nivel + f"- [{indice}]\n"
                resul += imprimir_arbol(elemento, nivel + 1)
    else:
        resul+= '  ' * nivel + str(arbol) + "\n"
    return resul