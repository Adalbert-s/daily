import os

def convert_to_utf8(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):  # Pode mudar para .html, .txt, etc.
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r', encoding='latin1') as f:  # Se der erro, tente 'cp1252'
                        content = f.read()
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"[OK] {file_path}")
                except Exception as e:
                    print(f"[ERRO] {file_path} - {e}")

# Altere '.' para outro caminho se quiser
convert_to_utf8('.')
