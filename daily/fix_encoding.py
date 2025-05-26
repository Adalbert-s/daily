# -*- coding: utf-8 -*-
file_path = "app/templates/app/index.html"

with open(file_path, 'rb') as file:
    content = file.read()

# Fun��o para localizar o byte problem�tico
def find_invalid_character(content):
    for i, byte in enumerate(content):
        try:
            # Tente decodificar byte a byte
            byte.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Erro no byte {i}: {byte} (em hexadecimal: {hex(byte)})")
            return i, byte  # Retorna a posi��o e o byte problem�tico

    print("Todos os caracteres est�o v�lidos UTF-8.")
    return None

# Verifique o conte�do do arquivo
problematic_byte = find_invalid_character(content)

# Se encontrado, voc� pode mostrar onde ocorreu o erro
if problematic_byte:
    print(f"Byte problem�tico encontrado na posi��o {problematic_byte[0]} com valor {problematic_byte[1]}")
