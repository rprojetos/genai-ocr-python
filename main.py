from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
import sys # Usado para acessar argumentos da linha de comando

# --- CONFIGURAÇÃO ---
# Define o caminho do PDF. Idealmente, passe como um argumento ao executar o script.
# Exemplo de como rodar: python seu_script.py caminho/para/o/arquivo.pdf
try:
    caminho_pdf_str = sys.argv[1]
except IndexError:
    print("ERRO: Você precisa fornecer o caminho para o arquivo PDF.")
    print("Uso: python seu_script.py <caminho_do_pdf>")
    sys.exit(1) # Encerra o script se nenhum arquivo for fornecido

pdf_path = Path(caminho_pdf_str)
caminho_saida_txt = pdf_path.with_suffix('.txt') # Cria um nome de arquivo de saída, ex: "relatorio.txt"

# Verifica se o arquivo PDF realmente existe antes de continuar
if not pdf_path.is_file():
    print(f"ERRO: O arquivo '{pdf_path}' não foi encontrado.")
    sys.exit(1)

# Parâmetros do OCR
lang = "por"
dpi = 300

# --- PROCESSAMENTO ---
all_text = ""

try:
    print(f"Processando o arquivo: {pdf_path.name}")
    print("Convertendo PDF para imagens... (isso pode demorar)")
    
    # Converte o PDF em uma lista de imagens (uma por página)
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    
    print("Extraindo texto com OCR...")
    
    # Itera sobre cada página para extrair o texto
    for i, page in enumerate(pages, start=1):
        print(f" - Lendo página {i}/{len(pages)}")
        text = pytesseract.image_to_string(page, lang=lang)
        all_text += f"\n\n==== Página {i} ====\n\n{text.strip()}"

    # --- SAÍDA ---
    print(f"\nExtração concluída! Salvando texto em: {caminho_saida_txt.name}")
    
    # Salva todo o texto extraído em um arquivo .txt
    with open(caminho_saida_txt, 'w', encoding='utf-8') as f:
        f.write(all_text)

    print("Operação finalizada com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")