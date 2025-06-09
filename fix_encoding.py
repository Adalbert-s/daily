# -*- coding: utf-8 -*-
file_path = "app/templates/app/index.html"

with open(file_path, 'rb') as file:
    content = file.read()

# FunÃ§Ã£o para localizar o byte problemÃ¡tico
def find_invalid_character(content):
    for i, byte in enumerate(content):
        try:
            # Tente decodificar byte a byte
            byte.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Erro no byte {i}: {byte} (em hexadecimal: {hex(byte)})")
            return i, byte  # Retorna a posiÃ§Ã£o e o byte problemÃ¡tico

    print("Todos os caracteres estÃ£o vÃ¡lidos UTF-8.")
    return None

# Verifique o conteÃºdo do arquivo
problematic_byte = find_invalid_character(content)

# Se encontrado, vocÃª pode mostrar onde ocorreu o erro
if problematic_byte:
    print(f"Byte problemÃ¡tico encontrado na posiÃ§Ã£o {problematic_byte[0]} com valor {problematic_byte[1]}")
