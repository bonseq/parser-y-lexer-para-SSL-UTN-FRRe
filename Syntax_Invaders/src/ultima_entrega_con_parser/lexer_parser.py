import ply.lex as lex
import ply.yacc as yacc
import re

CLAVES_VALIDAS = [
    "nombre_equipo", "identidad_equipo", "direccion", "link", "carrera", "asignatura",
    "universidad_regional", "alianza_equipo", "integrantes", "proyectos",
    "nombre", "edad", "cargo", "foto", "email", "habilidades", "salario", "activo",
    "estado", "resumen", "tareas", "fecha_inicio", "fecha_fin", "video", "conclusion",
    "equipos", "version", "firma_digital", "calle", "ciudad", "pais"
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
    "direccion": "DIRECCION",
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
    "pais": "PAIS",
    "version": "VERSION",
    "firma_digital": "FIRMA_DIGITAL"
}

tokens = [
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'FECHA', 'CLAVE_EMAIL', 'EMAIL', 'URL',
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CLAVE_LINK', 'CORCHETE_DER', 'COMA', 'LISTA_EQUIPOS', 'NOMBRE_EQUIPO', 
    'IDENTIDAD_EQUIPO', 'ASIGNATURA', 'CARRERA', 'UNIVERSIDAD_REGIONAL',
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

ultimo_error_lexico_linea = [None]

def t_error(t):
    if ultimo_error_lexico_linea[0] != t.lineno:
        errores.append(f"[ERROR LÉXICO] en la línea {t.lineno}: carácter inesperado '{t.value[0]}'")
        ultimo_error_lexico_linea[0] = t.lineno
    t.lexer.skip(1)

# ----------------- PARSER -----------------
errores = []

CARGOv = [
    "product analyst", "project manager", "ux designer", "marketing",
    "developer", "devops", "db admin"
]
ESTADOSv = [
    "to do", "in progress", "canceled", "done", "on hold"
]
chart_PROHIBIDO = "áéíóúÁÉÍÓÚñÑ"

EMAIL_R = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9._\-]+\.[a-zA-Z]{2,4}$'
URL_R = r'^(http:\/\/|https:\/\/)[a-zA-Z0-9\-\._~:\/\?#\[\]@!$&\'()*+,;=%]+$'
CLAVES_URL = ["link", "identidad_equipo", "video", "foto"]

def p_json(p):
    'json : LLAVE_IZQ elementos LLAVE_DER'
    arbol, html = p[2]
    p[0] = ('json', arbol)
    # el html se genera en la interfaz usando json_a_html, así que solo imprimo el árbol

def p_elementos(p):
    '''elementos : par
                 | elementos COMA par'''
    if len(p) == 2:
        arbol, html = p[1]
        p[0] = ([arbol], html)
    else:
        arboles, html1 = p[1]
        arbol, html2 = p[3]
        p[0] = (arboles + [arbol], html1 + html2)

def p_par(p):
    'par : clave DOS_PUNTOS valor'
    clave_token = p[1]
    clave_valor = clave_token.value
    arbol, html = p[3]

    # chequeos semánticos (igual que antes)
    if clave_valor not in CLAVES_VALIDAS:
        errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, clave inválida o mal escrita: '{clave_valor}'")
    if clave_valor == "cargo":
        if str(arbol).lower() not in CARGOv:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, cargo invalido")
    if clave_valor == "estado":
        if str(arbol).lower() not in ESTADOSv:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, estado invalido")
    #if isinstance(arbol, str): creo q sto no es necesario
     #   if any(c in arbol for c in chart_PROHIBIDO):
     #      errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, palabra acentuada o con Ñ")
    if clave_valor == "edad":
        if not (isinstance(arbol, int) and arbol > 0):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, edad debe ser mayor a cero y entero")
    if isinstance(arbol, float):
        if arbol < 0:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, numero negativo")
        else:
            decimales = str(arbol).split(".")[1]
            if len(decimales) > 2:
                errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno} , numero con mas de dos decimales")
    if isinstance(arbol, int):
        if arbol < 0:
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}")
    if isinstance(arbol, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', arbol):
        anio, mes, dia = map(int, arbol.split('-'))
        if not (1900 <= anio <= 2099):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, anio invalido")
        if not (1 <= mes <= 12):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, mes invalido")
        if not (1 <= dia <= 31):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, dia invalido")
    if clave_valor == "email":
        if not re.match(EMAIL_R, str(arbol)):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, email, invalido")
    if clave_valor in ["activo"]:
        if not isinstance(arbol, bool):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}, valor booleano inválido")
    if clave_valor in CLAVES_URL:
        if not re.match(URL_R, str(arbol)):
            errores.append(f"[ERROR SEMÁNTICO] en la línea {clave_token.lineno}")

    # HTML: para acumulamor el HTML de los valores que sean equipos (para mostrar en la interfaz)
    if clave_valor == "equipos":
        html_out = html
    else:
        html_out = ""  # El HTML de los otros campos lo arma la interfaz

    p[0] = (clave_valor, arbol), html_out

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
    arboles, html = p[2]
    arbol = dict(arboles)
    # si es un equipo, generá HTML especial para ese equipo
    if "nombre_equipo" in arbol:
        html = html_equipo(arbol)
    elif "nombre" in arbol and "cargo" in arbol and "edad" in arbol:
        html = html_integrante(arbol)
    elif "nombre" in arbol and "estado" in arbol and "resumen" in arbol:
        html = html_proyecto(arbol)
    elif "nombre" in arbol and "estado" in arbol and "fecha_inicio" in arbol:
        html = html_tarea(arbol)
    else:
        html = ""
    p[0] = (arbol, html)

def p_lista(p):
    'lista : CORCHETE_IZQ valores CORCHETE_DER'
    arboles, html = p[2]
    p[0] = (arboles, html)

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
    if isinstance(p[1], tuple) and len(p[1]) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], str(p[1]))

def p_valores(p):
    '''valores : valor
               | valores COMA valor'''
    if len(p) == 2:
        arbol, html = p[1]
        p[0] = ([arbol], html)
    else:
        arboles, html1 = p[1]
        arbol, html2 = p[3]
        p[0] = (arboles + [arbol], html1 + html2)

def p_error(p):
    if p:
        errores.append(f"[ERROR SINTÁCTICO] en la línea {p.lineno}: token inesperado '{p.value}'")
        while True:
            tok = parser.token()
            if not tok or tok.type in ('LLAVE_DER', 'COMA', 'CORCHETE_DER'):
                break
    else:
        errores.append("[ERROR SINTÁCTICO] al final del archivo")

# ----------------- FUNCIONES DE HTML PARA CADA OBJETO -----------------

def html_equipo(equipo):
    # Devuelve solo el HTML del equipo (sin <html> ni <body>)
    html = "<div style='border: 1px solid gray; padding: 20px; margin-bottom: 20px;'>"
    html += f"<h2>{equipo.get('nombre_equipo', '')}</h2>"
    html += f"<p><b>Identidad:</b> <img src='{equipo.get('identidad_equipo', '')}' width='100'></p>"
    html += f"<p><b>Link:</b> <a href='{equipo.get('link', '')}'>{equipo.get('link', '')}</a></p>"
    html += f"<p><b>Asignatura:</b> {equipo.get('asignatura', '')}</p>"
    html += f"<p><b>Carrera:</b> {equipo.get('carrera', '')}</p>"
    html += f"<p><b>Universidad:</b> {equipo.get('universidad_regional', '')}</p>"
    direccion = equipo.get('dirección', {})
    html += f"<p><b>Dirección:</b> {direccion.get('calle', '')}, {direccion.get('ciudad', '')}, {direccion.get('país', '')}</p>"
    html += f"<p><b>Alianza equipo:</b> {equipo.get('alianza_equipo', '')}</p>"

    # Integrantes
    html += "<h2>Integrantes</h2><ul>"
    for integrante in equipo.get('integrantes', []):
        html += "<li>"
        html += f"<b>{integrante.get('nombre', '')}</b> ({integrante.get('cargo', '')})<br>"
        html += f"Edad: {integrante.get('edad', '')}<br>"
        html += f"Email: {integrante.get('email', '')}<br>"
        html += f"Habilidades: {integrante.get('habilidades', '')}<br>"
        html += f"Salario: {integrante.get('salario', '')}<br>"
        html += f"Activo: {'Sí' if integrante.get('activo', False) else 'No'}<br>"
        html += f"<img src='{integrante.get('foto', '')}' width='60'><br>"
        html += "</li>"
    html += "</ul>"

    # Proyectos
    html += "<h3>Proyectos</h3><ul>"
    for proyecto in equipo.get('proyectos', []):
        html += "<li>"
        html += f"<b>{proyecto.get('nombre', '')}</b><br>"
        html += f"Estado: {proyecto.get('estado', '')}<br>"
        html += f"Resumen: {proyecto.get('resumen', '')}<br>"
        html += f"Fecha inicio: {proyecto.get('fecha_inicio', '')} - Fecha fin: {proyecto.get('fecha_fin', '')}<br>"
        html += f"Video: <a href='{proyecto.get('video', '')}'>{proyecto.get('video', '')}</a><br>"
        html += f"Conclusión: {proyecto.get('conclusion', '')}<br>"
        # Tareas
        html += f"Tareas:"
        html += "<table border='1' cellpadding='5' cellspacing='0' style='margin-left:20px;'>"
        html += "<tr>"
        html += "<th>Nombre</th><th>Estado</th><th>Resumen</th><th>Fecha inicio</th><th>Fecha fin</th>"
        html += "</tr>"
        for tarea in proyecto.get('tareas', []):
            html += "<tr>"
            html += f"<td>{tarea.get('nombre', '')}</td>"
            html += f"<td>{tarea.get('estado', '')}</td>"
            html += f"<td>{tarea.get('resumen', '')}</td>"
            html += f"<td>{tarea.get('fecha_inicio', '')}</td>"
            html += f"<td>{tarea.get('fecha_fin', '')}</td>"
            html += "</tr>"
        html += "</table>"
        html += "</li>"
    html += "</ul>"
    html += "</div>"
    return html

def html_integrante(integrante):
    html = "<li>"
    html += f"<b>{integrante.get('nombre', '')}</b> ({integrante.get('cargo', '')})<br>"
    html += f"Edad: {integrante.get('edad', '')}<br>"
    html += f"Email: {integrante.get('email', '')}<br>"
    html += f"Habilidades: {integrante.get('habilidades', '')}<br>"
    html += f"Salario: {integrante.get('salario', '')}<br>"
    html += f"Activo: {'Sí' if integrante.get('activo', False) else 'No'}<br>"
    html += f"<img src='{integrante.get('foto', '')}' width='60'><br>"
    html += "</li>"
    return html

def html_proyecto(proyecto):
    html = "<li>"
    html += f"<b>{proyecto.get('nombre', '')}</b><br>"
    html += f"Estado: {proyecto.get('estado', '')}<br>"
    html += f"Resumen: {proyecto.get('resumen', '')}<br>"
    html += f"Fecha inicio: {proyecto.get('fecha_inicio', '')} - Fecha fin: {proyecto.get('fecha_fin', '')}<br>"
    html += f"Video: <a href='{proyecto.get('video', '')}'>{proyecto.get('video', '')}</a><br>"
    html += f"Conclusión: {proyecto.get('conclusion', '')}<br>"
    # Tareas
    html += "Tareas:"
    html += "<table border='1' cellpadding='5' cellspacing='0' style='margin-left:20px;'>"
    html += "<tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Fecha inicio</th><th>Fecha fin</th></tr>"
    for tarea in proyecto.get('tareas', []):
        html += html_tarea(tarea)
    html += "</table>"
    html += "</li>"
    return html

def html_tarea(tarea):
    html = "<tr>"
    html += f"<td>{tarea.get('nombre', '')}</td>"
    html += f"<td>{tarea.get('estado', '')}</td>"
    html += f"<td>{tarea.get('resumen', '')}</td>"
    html += f"<td>{tarea.get('fecha_inicio', '')}</td>"
    html += f"<td>{tarea.get('fecha_fin', '')}</td>"
    html += "</tr>"
    return html

lexer = lex.lex()
parser = yacc.yacc()

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
    resultado = parser.parse(texto)
    if resultado is None:
        # Si el parser no pudo armar nada, devolvé un árbol vacío para que igual se genere HTML
        return ('json', [])
    return resultado

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
