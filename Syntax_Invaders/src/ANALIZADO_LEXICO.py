import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import tkinter.font as tkFont
import ply.lex as lex
import unicodedata


ultima_clave = None
# Lista de nombres de tokens
tokens = [
    'NOMBRE_EQUIPO', 'VERSION', 'FIRMA_DIGITAL', 'LISTA_EQUIPOS', 'IDENTIDAD_EQUIPO', 'LINK',
    'CARRERA', 'ASIGNATURA', 'UNIVERSIDAD_REGIONAL', 'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS',
    'NOMBRE', 'EDAD', 'CARGO', 'FOTO', 'EMAIL', 'HABILIDADES', 'SALARIO', 'ACTIVO', 'ESTADO',
    'RESUMEN', 'TAREAS', 'VIDEO', 'CONCLUSION', 'DIR_DET',
    'CALLE', 'CIUDAD', 'PAIS',
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA',
    'STRING', 'INTEGER', 'FLOAT', 'BOOL', 'NULL', 'URL', 'FECHA'
]

# Palabras reservadas (solo claves, no valores)
reserved = {
    "equipos": "LISTA_EQUIPOS",#S
    "version": "VERSION",#S
    "firma_digital": "FIRMA_DIGITAL",#S
    "nombre_equipo": "NOMBRE_EQUIPO", #S
    "identidad_equipo": "IDENTIDAD_EQUIPO",#URL
    "dirección": "DIR_DET",#S
    "link": "LINK",#UR
    "carrera": "CARRERA",#S
    "asignatura": "ASIGNATURA",#S
    "universidad_regional": "UNIVERSIDAD_REGIONAL",#S
    "alianza_equipo": "ALIANZA_EQUIPO",#S
    "integrantes": "INTEGRANTES",#S
    "proyectos": "PROYECTOS",#S
    "nombre": "NOMBRE",#S
    "edad": "EDAD",#I
    "cargo": "CARGO",#S
    "foto": "FOTO",#U
    "email": "EMAIL",#EMAIL
    "habilidades": "HABILIDADES",#S
    "salario": "SALARIO",#FLOAT
    "activo": "ACTIVO",#BOL
    "estado": "ESTADO",#S
    "resumen": "RESUMEN",#S
    "tareas": "TAREAS",#S
    "fecha_inicio": "FECHA",#FECHA
    "fecha_fin": "FECHA",#FECHGA
    "video": "VIDEO",#URL
    "conclusion": "CONCLUSION",#S
    "calle": "CALLE",#S
    "ciudad": "CIUDAD",#S
    "país": "PAIS"#S
}

# Listas de valores válidos para estado y cargo
valores_estado = ["To do", "In progress", "Canceled", "Done", "On hold"]
valores_cargo = ["Product Analyst", "Project Manager", "UX designer", "Marketing", "Developer", "Devops", "DB admin"]
claves_url = ["VIDEO", "FOTO", "IDENTIDAD_EQUIPO"]

# rules para símbolos
t_DOS_PUNTOS = r':'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','

# ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_EMAIL(t):
    r'\"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\"'
    t.value = t.value.strip('"') 
    return t

def t_FECHA(t):
    r'\"(19[0-9]{2}|20[0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\"'
    t.value = t.value.strip('"')  
    return t 

def t_LINK(t):
    r'\"(http|https):\/\/[a-zA-Z0-9\.\-\/\_\?\=\&\#\:]+\"'
    global ultima_clave
    valor = t.value.strip('"')
    # onda algoritmos, asignar el tipo correcto
    if ultima_clave in claves_url:
        t.type = ultima_clave
    else:
        t.type = "LINK"
    t.value = valor
    ultima_clave = None
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

def t_STRING(t):#manejo de TODOS los string mirar que no haya conflicto
    r'\"([^\\\n]|(\\.))*?\"'
    valor = t.value.strip('"')
    global ultima_clave

    # C1: valor coincide con una clave
    if valor in reserved:
        t.type = reserved[valor]
        if t.type in ["CARGO", "ESTADO", "PAIS", "CALLE", "CIUDAD", "NOMBRE_EQUIPO", "NOMBRE", "FIRMA_DIGITAL", "VERSION", "UNIVERSIDAD_REGIONAL", "HABILIDADES", "CARRERA", "ASIGNATURA", "ALIANZA_EQUIPO", "CONCLUSION", "RESUMEN" ]:
            ultima_clave = t.type
    # C2: valor dinámico y la última clave lo define
    elif ultima_clave in ["CARGO", "ESTADO", "PAIS", "CALLE", "CIUDAD", "NOMBRE_EQUIPO", "NOMBRE", "FIRMA_DIGITAL", "VERSION", "UNIVERSIDAD_REGIONAL", "HABILIDADES", "CARRERA", "ASIGNATURA", "ALIANZA_EQUIPO", "CONCLUSION", "RESUMEN" ]:
        t.type = ultima_clave
        ultima_clave = None
    # C3: listas literales(????)
    elif valor in valores_estado:
        t.type = "ESTADO"
    elif valor in valores_cargo:
        t.type = "CARGO"
    else:
        t.type = "STRING"
        ultima_clave = None

    t.value = valor
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
        # guardar contexto si es clave con valor libre
        if t.type in ["PAIS", "CALLE", "CIUDAD"]:
            global ultima_clave
            ultima_clave = t.type
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Error léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def analizar_entrada():
    texto = entrada.get("1.0", tk.END)
    lexer.input(texto)
    salida.delete("1.0", tk.END)
    def tildes(texto):
        return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii').lower()#versi ta bien o no
    while True:
        tok = lexer.token()
        if not tok:
            break

        if not (tok.type in reserved.values() and tildes(tok.value) == tok.type.lower()):#con esto muestra solo token de verdad en vez de repetirse ejemplo ya no hay CARGO: cargo sino que muestra CARGO:marketing
            salida.insert(tk.END, f"[Linea{tok.lineno}] {tok.type}: {tok.value}\n")

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        entrada.delete("1.0", tk.END)
        entrada.insert(tk.END, contenido)

def construir_ui():
    global entrada, salida
    root = tk.Tk()
    root.title("Lexer JSON - Análisis Léxico")

    try:
        font_path = "Minecraftia-Regular.ttf"
        custom_font = tkFont.Font(file=font_path, size=10)
    except Exception:
        custom_font = tkFont.Font(family="Courier", size=10)

    tk.Label(root, text="entrada JSON", font=custom_font, bg="#000", fg="#33ff33").pack()
    entrada = scrolledtext.ScrolledText(root, width=80, height=15,
        font=custom_font, relief="solid", bd=3, bg="#111", fg="#00ffff", insertbackground="#00ffff")
    entrada.pack(padx=10, pady=5)

    tk.Button(root, text="Analizar", font=custom_font, bg="#222", fg="#00ffff",
        command=analizar_entrada).pack(pady=2)
    tk.Button(root, text="Cargar archivo JSON", font=custom_font, bg="#222", fg="#00ffff",
        command=cargar_archivo).pack(pady=2)

    tk.Label(root, text="Tokens:", font=custom_font, bg="#000", fg="#33ff33").pack()
    salida = scrolledtext.ScrolledText(root, width=80, height=15,
        bg="#111", fg="#00ffff", insertbackground="#00ffff",
        font=custom_font, relief="solid", bd=3)
    salida.pack(padx=10, pady=5)

    root.configure(bg="#000")
    root.mainloop()

if __name__ == "__main__":
    construir_ui()
