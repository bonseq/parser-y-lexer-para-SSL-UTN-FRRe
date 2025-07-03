import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import sys

# Asegura que el directorio actual contenga el lexer_sininterfaz.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parserxd import analizar_sintaxis

def cargar_archivo(text_input):
    ruta = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")])
    if ruta:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")

def analizar(text_input, text_output):
    texto = text_input.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Vacío", "Por favor, ingresa o carga un JSON primero.")
        return
    try:
        resultado = analizar_sintaxis(texto)
        text_output.delete("1.0", tk.END)
        if resultado:
            text_output.insert(tk.END, "[OK] Análisis sintáctico exitoso.\n\n")
            text_output.insert(tk.END, str(resultado))
        else:
            text_output.insert(tk.END, "[ERROR] El análisis sintáctico falló.")
    except Exception as e:
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, f"[ERROR] Excepción al analizar:\n{str(e)}")

def main():
    root = tk.Tk()
    root.title("Analizador Sintáctico JSON (Lexer/Parser)")
    root.geometry("1000x600")

    # Entrada JSON manual
    label_input = tk.Label(root, text="JSON de entrada:")
    label_input.pack(anchor="w", padx=10, pady=(10, 0))
    text_input = ScrolledText(root, height=15)
    text_input.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Botones
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=5)

    btn_cargar = tk.Button(frame_buttons, text="Cargar Archivo", command=lambda: cargar_archivo(text_input))
    btn_cargar.pack(side="left", padx=10)

    btn_analizar = tk.Button(frame_buttons, text="Analizar", command=lambda: analizar(text_input, text_output))
    btn_analizar.pack(side="left", padx=10)

    # Salida
    label_output = tk.Label(root, text="Resultado del Análisis:")
    label_output.pack(anchor="w", padx=10)
    text_output = ScrolledText(root, height=15, bg="#f0f0f0")
    text_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    root.mainloop()

if __name__ == "__main__":
    main()
