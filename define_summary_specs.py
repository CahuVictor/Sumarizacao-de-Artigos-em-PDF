
# projeto/
# │
# ├── app.py                     # Script principal Streamlit
# ├── extract_text_plumber.py    # (1) Extrair texto de PDF
# ├── choose_model_t5.py         # (2a) Script do modelo T5
# ├── choose_model_bart.py       # (2a) Script do modelo BART
# ├── define_summary_specs.py    # (3) Define prompt e/ou formatação
# ├── summarize_article.py       # (4) Gerar o resumo final usando o modelo
# ├── requirements.txt           # Lista de dependências
# └── Dockerfile                 # Definição do container Docker

# define_summary_specs.py

def build_summary_prompt(text):
    """
    Cria um 'prompt' (instrução) que será passado ao modelo T5
    para que retorne um resumo com informações específicas.
    """
    # Ajuste o prompt ao seu gosto:
    instructions = (
        "Faça um resumo do texto a seguir, incluindo as informações: "
        "Autores, Ano, Revista/Jornal, Resumo Geral, Principais Resultados, "
        "e Metodologia Aplicada.\n\n"
        f"Texto: {text}"
    )
    return instructions

if __name__ == "__main__":
    """
    Se você executar este script, apenas mostra o prompt gerado
    para fins de teste.
    """
    exemplo_texto = "Este é um texto de exemplo que deveria conter autores, ano, etc."
    prompt = build_summary_prompt(exemplo_texto)
    print("Prompt gerado:\n")
    print(prompt)
