

# extract_text.py
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extrai o texto de todas as páginas de um PDF e retorna como string única.
    """
    try:
      text = ""
      with pdfplumber.open(pdf_path) as pdf:
          for page in pdf.pages:
              page_text = page.extract_text()
              if page_text:
                  text += page_text + "\n"
      return text
    except Exception as e:
        return f"Erro ao processar o PDF: {e}"

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