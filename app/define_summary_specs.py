
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
