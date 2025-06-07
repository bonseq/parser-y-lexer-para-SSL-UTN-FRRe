import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import tkinter.font as tkFont
import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    'NOMBRE_EQUIPOS', 'VERSION', 'FIRMA_DIGITAL', 'EQUIPOS', 'IDENTIDAD_EQUIPO', 'DIR', 'LINK',
    'CARRERA', 'ASIGNATURA', 'UNI_REGIONAL', 'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS',
    'NOMBRE', 'EDAD', 'CARGO', 'FOTO', 'EMAIL', 'HABILIDADES', 'SALARIO', 'ACTIVO', 'ESTADO',
    'RESUMEN', 'TAREAS', 'FECHA', 'VIDEO', 'CONCLUSION', 'DIR_DET',
    'CALLE', 'CIUDAD', 'PAIS',
    'TODO', 'INPROGRESS', 'CANCELED', 'DONE', 'ONHOLD',
    'PRODUCT_ANALYST', 'PROJECT_MANAGER', 'UX_DESIGNER', 'MARKETING', 'DEVELOPER', 'DEVOPS', 'DB_ADMIN',
    'DOS_PUNTOS', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'COMA',
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

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Error léxico] Línea {t.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_ ]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def analizar_entrada():
    texto = entrada.get("1.0", tk.END)
    lexer.input(texto)
    salida.delete("1.0", tk.END)
    while True:
        tok = lexer.token()
        if not tok:
            break
        salida.insert(tk.END, f"{tok.type}: {tok.value}\n")

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

    # Intenta cargar la fuente retro, si no existe usa la default
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