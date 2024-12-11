# -*- coding: utf-8 -*-
file_path = "app/templates/app/index.html"

with open(file_path, 'rb') as file:
    content = file.read()

# Função para localizar o byte problemático
def find_invalid_character(content):
    for i, byte in enumerate(content):
        try:
            # Tente decodificar byte a byte
            byte.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Erro no byte {i}: {byte} (em hexadecimal: {hex(byte)})")
            return i, byte  # Retorna a posição e o byte problemático

    print("Todos os caracteres estão válidos UTF-8.")
    return None

# Verifique o conteúdo do arquivo
problematic_byte = find_invalid_character(content)

# Se encontrado, você pode mostrar onde ocorreu o erro
if problematic_byte:
    print(f"Byte problemático encontrado na posição {problematic_byte[0]} com valor {problematic_byte[1]}")
