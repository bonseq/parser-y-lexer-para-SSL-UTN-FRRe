import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer_parser import analizar_sintaxis, imprimir_tokens, imprimir_arbol, errores, lexer
 
 
def json_a_html(arbol):
  
    html = "<html><head><meta charset='utf-8'><title>Equipos</title></head><body>"
    html += "<h1>Equipos</h1>"

    # Si el árbol es ('json', [...])
    if isinstance(arbol, tuple) and arbol[0] == 'json':
        arbol = arbol[1]

    datos = dict(arbol)
    equipos = datos.get("equipos", [])
    version = datos.get("version", "")
    firma = datos.get("firma_digital", "")

    if equipos:
        for equipo in equipos:
            html += "<div style='border: 1px solid gray; padding: 20px; margin-bottom: 20px;'>" #Agregado que equipos sea metido dentro de un div
            html += f"<h2>{equipo.get('nombre_equipo', '')}</h2>"                               #con borde y margen
            html += f"<p><b>Identidad:</b> <img src='{equipo.get('identidad_equipo', '')}' width='100'></p>"
            html += f"<p><b>Link:</b> <a href='{equipo.get('link', '')}'>{equipo.get('link', '')}</a></p>"
            html += f"<p><b>Asignatura:</b> {equipo.get('asignatura', '')}</p>"
            html += f"<p><b>Carrera:</b> {equipo.get('carrera', '')}</p>"
            html += f"<p><b>Universidad:</b> {equipo.get('universidad_regional', '')}</p>"
            direccion = equipo.get('dirección', {})
            html += f"<p><b>Dirección:</b> {direccion.get('calle', '')}, {direccion.get('ciudad', '')}, {direccion.get('país', '')}</p>"
            html += f"<p><b>Alianza equipo:</b> {equipo.get('alianza_equipo', '')}</p>"

            # Integrantes
            html += "<h2>Integrantes</h2><ul>" # Consigna del tpi pide nombre de int. en h2, asi que lo cambié
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
                html += f"<b>{proyecto.get('nombre', '')}</b><br>" #Acá había un problema que Estado aparecía pegado al Nombre
                html += f"Estado: {proyecto.get('estado', '')}<br>" #Solicionado con solo agregar un <br> en proyecto
                html += f"Resumen: {proyecto.get('resumen', '')}<br>"
                html += f"Fecha inicio: {proyecto.get('fecha_inicio', '')} - Fecha fin: {proyecto.get('fecha_fin', '')}<br>"
                html += f"Video: <a href='{proyecto.get('video', '')}'>{proyecto.get('video', '')}</a><br>"
                html += f"Conclusión: {proyecto.get('conclusion', '')}<br>"
            
             # Tareas
               # Tareas como tabla ((las medidas son arbitrarias nuestras)?)
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

    html += f"<hr><b>Versión:</b> {version if version else ''}<br>"
    html += f"<b>Firma digital:</b> {firma if firma else ''}<br>"
    html += "</body></html>"
    return html

               
 
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
    lineas_texto = TextLineNumbers(frame)
    lineas_texto.pack(side="left", fill="y")

    # Entrada JSON manual
    text_input = ScrolledText(frame, height=15)
    text_input.pack(side="left", fill="both", expand=True)

    # Función para actualizar los números de línea
    def actualizar_lineas(event=None):
        lineas_texto.update_line_numbers(text_input)

    text_input.bind("<KeyRelease>", actualizar_lineas)
    text_input.bind("<MouseWheel>", actualizar_lineas)
    text_input.bind("<ButtonRelease-1>", actualizar_lineas)

    # Botones
    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=5)

    # Salida
    etiqueta_salida = tk.Label(root, text="Resultado del Análisis:")
    etiqueta_salida.pack(anchor="w", padx=10)
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
                    actualizar_lineas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")

    def analizar():
        texto = text_input.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Vacío", "Por favor, ingresa o carga un JSON primero.")
            return
        try:
            errores.clear()
            lexer.lineno = 1

            tokens_encontrados = imprimir_tokens(texto)
            lexer.lineno = 1
            resultado = analizar_sintaxis(texto)
            text_output.delete("1.0", tk.END)
            if errores:
                text_output.insert(tk.END, "[ERRORES ENCONTRADOS]\n")
                for err in errores:
                    text_output.insert(tk.END, err + "\n")
            if resultado:
                text_output.insert(tk.END, "Análisis sintáctico exitoso.\n\n")
                text_output.insert(tk.END, "-TOKENS ENCONTRADOS-\n")
                for linea in tokens_encontrados:
                    text_output.insert(tk.END, linea + "\n")
                text_output.insert(tk.END, "\nÁRBOL SINTÁCTICO\n")
                if isinstance(resultado, tuple) and resultado[0] == 'json':
                    bonito = imprimir_arbol(resultado[1])
                else:
                    bonito = imprimir_arbol(resultado)
                text_output.insert(tk.END, bonito)
            else:
                text_output.insert(tk.END, "[ERROR] El análisis sintáctico falló.")

        except Exception as e:
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, f"[ERROR] Excepción al analizar:\n{str(e)}")

    def exportar_html():
        texto = text_input.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Vacío", "Por favor, ingresa o carga un JSON primero.")
            return
        try:
            errores.clear()
            lexer.lineno = 1
            resultado = analizar_sintaxis(texto)
            if not resultado or errores:
                messagebox.showerror("Error", "Corrige los errores antes de exportar a HTML.")
                return
            html = json_a_html(resultado)
            ruta = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Archivos HTML", "*.html")])
            if ruta:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(html)
                messagebox.showinfo("Éxito", f"Archivo HTML exportado en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el HTML:\n{str(e)}")

    btn_cargar = tk.Button(frame_botones, text="Cargar Archivo", command=cargar_archivo)
    btn_cargar.pack(side="left", padx=10)

    btn_analizar = tk.Button(frame_botones, text="Analizar", command=analizar)
    btn_analizar.pack(side="left", padx=10)

    btn_exportar = tk.Button(frame_botones, text="Exportar a HTML", command=exportar_html)
    btn_exportar.pack(side="left", padx=10)

    root.mainloop()
if __name__ == "__main__":
    main()
