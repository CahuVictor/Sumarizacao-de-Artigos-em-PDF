
from transformers import pipeline

# Modelo pré-treinado para inglês
# model_name = "facebook/bart-large-cnn"

# max_length=130
# min_length=30
# do_sample=False

# Função para resumir texto
# summarizer = pipeline("summarization", model=model_name)

# def summarize_text(text, max_length=130, min_length=30):
#     #summarizer = pipeline("summarization", model=model_name)
#     return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)

# def summarize_text_pt(text, max_length=200, min_length=50):
#     return summarizer(
#         text,
#         max_length=max_length,
#         min_length=min_length,
#         do_sample=False
#     )[0]["summary_text"]

def get_summarizer_bart(model_name="Jonatas/bart-large-portuguese-sum"):
    """
    Retorna um pipeline de 'summarization' para o modelo BART em PT-BR.
    """
    summarizer = pipeline("summarization", model=model_name)
    return summarizer

if __name__ == "__main__":
    """
    Se você rodar este script diretamente, fará um teste rápido no modelo
    com um texto curto.
    """
    import sys

    # Se um nome de modelo for passado como argumento, use-o, senão use o default:
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    else:
        model_name = "unicamp-dl/ptt5-base-portuguese-vocab"

    summarizer = get_summarizer_bart(model_name)
    texto_teste = "Este é um texto de exemplo para testar a sumarização em português."
    resultado = summarizer(texto_teste, max_length=50, min_length=10, do_sample=False)
    print("Resumo de teste:", resultado[0]["generated_text"])

# No terminal
#   python choose_model.py "unicamp-dl/ptt5-base-portuguese-vocab"
#   python choose_model.py