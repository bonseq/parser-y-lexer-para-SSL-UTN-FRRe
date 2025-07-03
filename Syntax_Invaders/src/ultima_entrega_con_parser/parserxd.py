import ply.yacc as yacc
from lexer_sininterfaz import tokens, lexer

# ----
# REGLA PRINCIPAL (JSON RAÍZ)
# ----
def p_json(p):
    'json : LLAVE_IZQ campos_json LLAVE_DER'
    p[0] = p[2]

# ----
# CAMPOS DEL JSON RAÍZ
# ----
def p_campos_json(p):
    '''campos_json : campo_json
                   | campo_json COMA campos_json'''
    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        else:
            p[0] = dict([p[1]])
    else:
        if isinstance(p[1], dict):
            d = p[1]
        else:
            d = dict([p[1]])
        d.update(p[3])
        p[0] = d

def p_campo_json(p):
    '''campo_json : LISTA_EQUIPOS DOS_PUNTOS CORCHETE_IZQ lista_equipos CORCHETE_DER
                  | VERSION DOS_PUNTOS STRING
                  | FIRMA_DIGITAL DOS_PUNTOS STRING'''
    if p[1] == 'LISTA_EQUIPOS':
        p[0] = ("equipos", p[4])
    elif p[1] == 'VERSION':
        p[0] = ("version", p[3])
    elif p[1] == 'FIRMA_DIGITAL':
        p[0] = ("firma_digital", p[3])

# ----
# LISTA DE EQUIPOS
# ----
def p_lista_equipos(p):
    '''lista_equipos : equipo
                     | equipo COMA lista_equipos'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_equipo(p):
    'equipo : LLAVE_IZQ campos_equipo LLAVE_DER'
    p[0] = p[2]

def p_campos_equipo(p):
    '''campos_equipo : campo_equipo
                     | campo_equipo COMA campos_equipo'''
    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        else:
            p[0] = dict([p[1]])
    else:
        if isinstance(p[1], dict):
            d = p[1]
        else:
            d = dict([p[1]])
        d.update(p[3])
        p[0] = d

def p_campo_equipo(p):
    '''campo_equipo : NOMBRE_EQUIPO DOS_PUNTOS STRING
                    | IDENTIDAD_EQUIPO DOS_PUNTOS IDENTIDAD_EQUIPO
                    | IDENTIDAD_EQUIPO DOS_PUNTOS LINK
                    | LINK DOS_PUNTOS LINK
                    | ASIGNATURA DOS_PUNTOS STRING
                    | CARRERA DOS_PUNTOS STRING
                    | UNIVERSIDAD_REGIONAL DOS_PUNTOS STRING
                    | DIR_DET DOS_PUNTOS LLAVE_IZQ campos_direccion LLAVE_DER
                    | ALIANZA_EQUIPO DOS_PUNTOS STRING
                    | INTEGRANTES DOS_PUNTOS CORCHETE_IZQ lista_integrantes CORCHETE_DER
                    | PROYECTOS DOS_PUNTOS CORCHETE_IZQ lista_proyectos CORCHETE_DER'''
    if p[1] == 'NOMBRE_EQUIPO':
        p[0] = ("nombre_equipo", p[3])
    elif p[1] == 'IDENTIDAD_EQUIPO':
        p[0] = ("identidad_equipo", p[3])
    elif p[1] == 'LINK':
        p[0] = ("link", p[3])
    elif p[1] == 'ASIGNATURA':
        p[0] = ("asignatura", p[3])
    elif p[1] == 'CARRERA':
        p[0] = ("carrera", p[3])
    elif p[1] == 'UNIVERSIDAD_REGIONAL':
        p[0] = ("universidad_regional", p[3])
    elif p[1] == 'DIR_DET':
        p[0] = ("dirección", p[5])
    elif p[1] == 'ALIANZA_EQUIPO':
        p[0] = ("alianza_equipo", p[3])
    elif p[1] == 'INTEGRANTES':
        p[0] = ("integrantes", p[4])
    elif p[1] == 'PROYECTOS':
        p[0] = ("proyectos", p[4])

# ----
# DIRECCIÓN
# ----
def p_campos_direccion(p):
    '''campos_direccion : campo_direccion
                        | campo_direccion COMA campos_direccion'''
    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        else:
            p[0] = dict([p[1]])
    else:
        if isinstance(p[1], dict):
            d = p[1]
        else:
            d = dict([p[1]])
        d.update(p[3])
        p[0] = d

def p_campo_direccion(p):
    '''campo_direccion : CALLE DOS_PUNTOS STRING
                       | CIUDAD DOS_PUNTOS STRING
                       | PAIS DOS_PUNTOS STRING'''
    p[0] = (p[1].lower(), p[3])

# ----
# INTEGRANTES
# ----
def p_lista_integrantes(p):
    '''lista_integrantes : integrante
                         | integrante COMA lista_integrantes'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_integrante(p):
    'integrante : LLAVE_IZQ campos_integrante LLAVE_DER'
    p[0] = p[2]

def p_campos_integrante(p):
    '''campos_integrante : campo_integrante
                         | campo_integrante COMA campos_integrante'''
    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        else:
            p[0] = dict([p[1]])
    else:
        if isinstance(p[1], dict):
            d = p[1]
        else:
            d = dict([p[1]])
        d.update(p[3])
        p[0] = d

def p_campo_integrante(p):
    '''campo_integrante : NOMBRE DOS_PUNTOS STRING
                        | EDAD DOS_PUNTOS INTEGER
                        | CARGO DOS_PUNTOS STRING
                        | FOTO DOS_PUNTOS FOTO
                        | EMAIL DOS_PUNTOS EMAIL
                        | HABILIDADES DOS_PUNTOS STRING
                        | SALARIO DOS_PUNTOS FLOAT
                        | ACTIVO DOS_PUNTOS BOOL'''
    p[0] = (p[1].lower(), p[3])

# ----
# PROYECTOS
# ----
def p_lista_proyectos(p):
    '''lista_proyectos : proyecto
                       | proyecto COMA lista_proyectos'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_proyecto(p):
    'proyecto : LLAVE_IZQ campos_proyecto LLAVE_DER'
    p[0] = p[2]

def p_campos_proyecto(p):
    '''campos_proyecto : campo_proyecto
                       | campo_proyecto COMA campos_proyecto'''
    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        else:
            p[0] = dict([p[1]])
    else:
        if isinstance(p[1], dict):
            d = p[1]
        else:
            d = dict([p[1]])
        d.update(p[3])
        p[0] = d

def p_campo_proyecto(p):
    '''campo_proyecto : NOMBRE DOS_PUNTOS STRING
                      | ESTADO DOS_PUNTOS STRING
                      | RESUMEN DOS_PUNTOS STRING
                      | TAREAS DOS_PUNTOS CORCHETE_IZQ lista_tareas CORCHETE_DER
                      | FECHA DOS_PUNTOS FECHA
                      | VIDEO DOS_PUNTOS VIDEO
                      | CONCLUSION DOS_PUNTOS STRING'''
    if p[1] == 'NOMBRE':
        p[0] = ("nombre", p[3])
    elif p[1] == 'ESTADO':
        p[0] = ("estado", p[3])
    elif p[1] == 'RESUMEN':
        p[0] = ("resumen", p[3])
    elif p[1] == 'TAREAS':
        p[0] = ("tareas", p[4])
    elif p[1] == 'FECHA':
        # p.slice[1].value contiene el nombre de la clave: "fecha_inicio" o "fecha_fin"
        p[0] = (p.slice[1].value, p[3])
    elif p[1] == 'VIDEO':
        p[0] = ("video", p[3])
    elif p[1] == 'CONCLUSION':
        p[0] = ("conclusion", p[3])

# ----
# TAREAS
# ----
def p_lista_tareas(p):
    '''lista_tareas : tarea
                   | tarea COMA lista_tareas'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_tarea(p):
    'tarea : LLAVE_IZQ campos_tarea LLAVE_DER'
    p[0] = p[2]

def p_campos_tarea(p):
    '''campos_tarea : campo_tarea
                    | campo_tarea COMA campos_tarea'''
    if len(p) == 2:
        if isinstance(p[1], dict):
            p[0] = p[1]
        else:
            p[0] = dict([p[1]])
    else:
        if isinstance(p[1], dict):
            d = p[1]
        else:
            d = dict([p[1]])
        d.update(p[3])
        p[0] = d

def p_campo_tarea(p):
    '''campo_tarea : NOMBRE DOS_PUNTOS STRING
                   | ESTADO DOS_PUNTOS STRING
                   | RESUMEN DOS_PUNTOS STRING
                   | FECHA DOS_PUNTOS FECHA'''
    if p[1] == 'NOMBRE':
        p[0] = ("nombre", p[3])
    elif p[1] == 'ESTADO':
        p[0] = ("estado", p[3])
    elif p[1] == 'RESUMEN':
        p[0] = ("resumen", p[3])
    elif p[1] == 'FECHA':
        p[0] = (p.slice[1].value, p[3])

# ----
# MANEJO DE ERRORES
# ----
def p_error(p):
    if p:
        print(f"[ERROR] Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("[ERROR] Error de sintaxis al final del archivo")

parser = yacc.yacc()

# ----
# FUNCIÓN DE ANÁLISIS
# ----
def analizar_sintaxis(texto):
    resultado = parser.parse(texto, lexer=lexer)
    if resultado:
        print("[OK] Análisis sintáctico exitoso.\n")
        print("Árbol sintáctico/resultante:")
        print(resultado)
        return resultado
    else:
        print("[ERROR] El análisis sintáctico falló.")
        return None

# ----
# MENÚ PRINCIPAL
# ----
if __name__ == "__main__":
    print("Parser JSON - Análisis Sintáctico (CMD)")
    print("1. Analizar archivo JSON")
    print("2. Pegar texto manualmente")
    opcion = input("Elige una opción (1/2): ").strip()
    if opcion == "1":
        ruta = input("Ruta del archivo JSON: ").strip()
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            analizar_sintaxis(contenido)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    elif opcion == "2":
        print("Pega el texto JSON (finaliza con una línea vacía):")
        lineas = []
        while True:
            linea = input()
            if linea == "":
                break
            lineas.append(linea)
        texto = "\n".join(lineas)
        analizar_sintaxis(texto)
    else:
        print("Opción no válida.")
        input("\nPresiona Enter para salir...")