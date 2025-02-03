
# projeto/
# │
# ├── extract_text.py            # (1) Extrair texto de PDF
# ├── choose_model.py            # (2) Selecionar modelo de sumarização
# ├── define_summary_specs.py    # (3) Especificar conteúdo do resumo
# ├── summarize_article.py       # (4) Gerar o resumo final usando o modelo
# └── requirements.txt           # (opcional) Dependências do projeto

# extract_text.py
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extrai o texto de todas as páginas de um PDF e retorna como string única.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

if __name__ == "__main__":
    """
    Se você rodar este script diretamente:
        python extract_text.py caminho_do_pdf
    ele imprime o texto extraído no terminal.
    """
    import sys
    if len(sys.argv) < 2:
        print("Uso: python extract_text.py <caminho_do_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    print(text)

# No terminal
#   python extract_text.py "/caminho/para/artigo.pdf"