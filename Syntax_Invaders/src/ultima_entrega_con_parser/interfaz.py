import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import sys

# Asegura que el directorio actual contenga el lexer_parser.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer_parser import analizar_sintaxis, imprimir_tokens, pretty_print_tree

class TextLineNumbers(tk.Text):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(width=4, padx=4, takefocus=0, border=0, background="#f0f0f0", state="disabled", wrap="none")

    def update_line_numbers(self, text_widget):
        self.config(state="normal")
        self.delete("1.0", tk.END)
        line_count = int(text_widget.index('end-1c').split('.')[0])
        line_numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self.insert("1.0", line_numbers)
        self.config(state="disabled")

def main():
    root = tk.Tk()
    root.title("Analizador Sintáctico JSON (Lexer/Parser)")
    root.geometry("1000x600")

    # Frame para numerador y texto
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    # Numerador de líneas
    line_numbers = TextLineNumbers(frame)
    line_numbers.pack(side="left", fill="y")

    # Entrada JSON manual
    text_input = ScrolledText(frame, height=15)
    text_input.pack(side="left", fill="both", expand=True)

    # Función para actualizar los números de línea
    def update_lines(event=None):
        line_numbers.update_line_numbers(text_input)

    # Bindings para actualizar el numerador
    text_input.bind("<KeyRelease>", update_lines)
    text_input.bind("<MouseWheel>", update_lines)
    text_input.bind("<ButtonRelease-1>", update_lines)

    # Botones
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=5)

    # Salida
    label_output = tk.Label(root, text="Resultado del Análisis:")
    label_output.pack(anchor="w", padx=10)
    text_output = ScrolledText(root, height=15, bg="#f0f0f0")
    text_output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def cargar_archivo():
        ruta = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")])
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    text_input.delete("1.0", tk.END)
                    text_input.insert(tk.END, contenido)
                    update_lines()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")

    def analizar():
        texto = text_input.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Vacío", "Por favor, ingresa o carga un JSON primero.")
            return
        try:
            tokens_encontrados = imprimir_tokens(texto)
            resultado = analizar_sintaxis(texto)
            text_output.delete("1.0", tk.END)
            if resultado:
                text_output.insert(tk.END, "[OK] Análisis sintáctico exitoso.\n\n")
                text_output.insert(tk.END, "--- TOKENS ENCONTRADOS ---\n")
                for linea in tokens_encontrados:
                    text_output.insert(tk.END, linea + "\n")
                text_output.insert(tk.END, "\n--- ÁRBOL SINTÁCTICO (BONITO) ---\n")
                if isinstance(resultado, tuple) and resultado[0] == 'json':
                    bonito = pretty_print_tree(resultado[1])
                else:
                    bonito = pretty_print_tree(resultado)
                text_output.insert(tk.END, bonito)
            else:
                text_output.insert(tk.END, "[ERROR] El análisis sintáctico falló.")
        except Exception as e:
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, f"[ERROR] Excepción al analizar:\n{str(e)}")

    btn_cargar = tk.Button(frame_buttons, text="Cargar Archivo", command=cargar_archivo)
    btn_cargar.pack(side="left", padx=10)

    btn_analizar = tk.Button(frame_buttons, text="Analizar", command=analizar)
    btn_analizar.pack(side="left", padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()