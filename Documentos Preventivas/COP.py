import shutil
from pathlib import Path

def consolidar_planilhas(caminho_raiz):
    raiz = Path(caminho_raiz)
    
    if not raiz.exists():
        print(f"Erro: O caminho '{caminho_raiz}' não foi encontrado.")
        return

    # Extensões de planilhas suportadas
    extensoes = ['*.xlsx', '*.xls', '*.csv', '*.ods']
    
    print(f"Lendo pasta: {raiz.absolute()}")
    print("-" * 30)

    for extensao in extensoes:
        for arquivo in raiz.rglob(extensao):
            
            # Pula arquivos que já estão na pasta raiz
            if arquivo.parent == raiz:
                continue
                
            destino = raiz / arquivo.name
            
            # Se já existir um arquivo com o mesmo nome na raiz, renomeia a cópia
            contador = 1
            while destino.exists():
                nome_novo = f"{arquivo.stem}_copia{contador}{arquivo.suffix}"
                destino = raiz / nome_novo
                contador += 1
            
            try:
                shutil.copy2(arquivo, destino)
                print(f"Sucesso: {arquivo.name} -> Copiado para a raiz")
            except Exception as e:
                print(f"Falha ao copiar {arquivo.name}: {e}")

    print("-" * 30)
    print("Processo finalizado!")

# --- CAMINHO CONFIGURADO ---
caminho_usuario = r"C:\Users\thiag\Desktop\000 - Minha Demanda\1 - Preventivas 2026\03 - Documentos Preventivas"

consolidar_planilhas(caminho_usuario)