from lexer_sininterfaz import lexer

# Cambiá el nombre del archivo si tu JSON se llama distinto
with open("ejemplo.json", "r", encoding="utf-8") as f:
    data = f.read()

lexer.input(data)

print("TOKENS GENERADOS POR EL LEXER:\n")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type:20} {tok.value!r} (linea {tok.lineno})")