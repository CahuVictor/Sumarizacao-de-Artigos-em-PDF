
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

# choose_model.py
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline
)

def get_summarizer(model_name="unicamp-dl/ptt5-base-portuguese-vocab"):
    """
    Retorna um pipeline de 'text2text-generation' para summarization, baseado em T5.
    Você pode trocar o model_name para outro que suporte sumarização em PT-BR.
    Ex: "Jonatas/bart-large-portuguese-sum" (pipeline("summarization")),
        "csevero/t5-base-ptbr-summ", etc.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    # Nesse caso, usamos "text2text-generation" pois T5 é "text2text".
    summarizer = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
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

    summarizer = get_summarizer(model_name)
    texto_teste = "Este é um texto de exemplo para testar a sumarização em português."
    resultado = summarizer(texto_teste, max_length=50, min_length=10, do_sample=False)
    print("Resumo de teste:", resultado[0]["generated_text"])

# No terminal
#   python choose_model.py "unicamp-dl/ptt5-base-portuguese-vocab"
#   python choose_model.py