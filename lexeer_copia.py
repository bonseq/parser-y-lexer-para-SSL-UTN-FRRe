import ply.lex as lex
import re

# Lista de nombres de tokens
tokens = [
    # pal reservadas
    'NOMBRE_EQUIPOS', 'VERSION', 'FIRMA_DIGITAL', 'EQUIPOS', 'IDENTIDAD_EQUIPO', 'DIR', 'LINK',
    'CARRERA', 'ASIGNATURA', 'UNI_REGIONAL', 'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS',
    'NOMBRE', 'EDAD', 'CARGO', 'FOTO', 'EMAIL', 'HABILIDADES', 'SALARIO', 'ACTIVO', 'ESTADO',
    'RESUMEN', 'TAREAS', 'FECHA', 'VIDEO', 'CONCLUSION', 'DIR_DET'
    'CALLE', 'CIUDAD', 'PAIS' 


    'TODO', 'INPROGRESS', 'CANCELED', 'DONE', 'ONHOLD',
    'PRODUCT_ANALYST', 'PROJECT_MANAGER', 'UX_DESIGNER', 'MARKETING', 'DEVELOPER', 'DEVOPS', 'DB_ADMIN',
    # símbolos
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA',
    # tipos  datos
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'URL', 'EMAIL_TYPE', 'DATE'
]

# palabras reservadas y valores literales
reserved = {
    "equipos": "EQUIPOS",
    "version": "VERSION",
    "firma_digital": "FIRMA_DIGITAL",
    "nombre_equipo": "NOMBRE_EQUIPO",
    "identidad_equipo": "IDENTIDAD_EQUIPO",
    "dirección": "DIR_DET",
    "link": "LINK",
    "carrera": "CARRERA",
    "asignatura": "ASIGNATURA",
    "universidad_regional": "UNI_REGIONAL",
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
    "fecha_inicio": "FECHA",
    "fecha_fin": "FECHA",
    "video": "VIDEO",
    "conclusion": "CONCLUSION",
    "calle": "CALLE",
    "ciudad": "CIUDAD",
    "país": "PAIS",
    # valores literales
    "To do": "ESTADO",
    "In progress": "ESTADO",
    "Canceled": "ESTADO",
    "Done": "ESTADO",
    "On hold": "ESTADO",
    "Product Analyst": "CARGO",
    "Project Manager": "CARGO",
    "UX designer": "CARGO",
    "Marketing": "CARGO",
    "Developer": "CARGO",
    "Devops": "CARGO",
    "DB admin": "CARGO"
}

# rules para símbolos
t_DOS_PUNTOS = r':'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','

# ignorar espacios y tabulaciones
t_ignore = ' \t'

# rules para tipos de datos y valores fechas, emails, links
def t_EMAIL(t):
    r'\"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\"'
    t.value = t.value.strip('"') 
    return t

def t_FECHA(t):
    r'\"(19[0-9]{2}|20[0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\"'
    t.value = t.value.strip('"')  
    return t 

def t_LINK(t):
    r'\"(http|https):\/\/[a-zA-Z0-9.-]+(:[0-9]+)?(\/[a-zA-Z0-9._\-\/]*)*\"'
    t.value = t.value.strip('"')  
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

##strings
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t 
#saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#errores
def t_error(t):
    print(f"[Error léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# función reconoce palabras reservadas y valores literales
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_ ]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def menu():
    while True:
        print("\n=== Menú de Análisis de JSON ===")
        print("1. Ingresar un texto para analizar")
        print("2. Analizar un archivo .json")
        print("3. Salir")
        opcion = input("Selecciona una opción (1-3): ")

        if opcion == "1":
            print("\nIngresá el texto a analizar (finalizá con una línea vacía):")
            lineas = []
            while True:
                linea = input()
                if linea == "":
                    break
                lineas.append(linea)
            texto = "\n".join(lineas)
            # Aquí llamás a tu función de análisis con 'texto'
            print("\n[Simulación] Analizando texto ingresado...")
            # analizar_texto(texto)
        elif opcion == "2":
            archivo = input("\nIngresá el nombre del archivo .json: ")
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    texto = f.read()
                print(f"\n[Simulación] Analizando archivo '{archivo}'...")
                # analizar_texto(texto)
            except FileNotFoundError:
                print("Archivo no encontrado. Verificá el nombre y la ruta.")
        elif opcion == "3":
            print("\n¡Gracias por usar el analizador! ¡Hasta luego! 👋")
            break
        else:
            print("Opción inválida. Por favor, elegí 1, 2 o 3.")

if __name__ == "__main__":
    import sys
    menu()
    # si se pasa un archivo como argumento, lo lee; si no, lee desde consola        