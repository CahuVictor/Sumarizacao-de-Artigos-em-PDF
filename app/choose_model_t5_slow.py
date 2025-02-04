
from transformers import T5Tokenizer, AutoModelForSeq2SeqLM, pipeline

def get_summarizer_t5(model_name="unicamp-dl/ptt5-base-portuguese-vocab"):
    """
    Retorna um pipeline de 'text2text-generation' para summarization, baseado em T5.
    Você pode trocar o model_name para outro que suporte sumarização em PT-BR.
    Ex: "Jonatas/bart-large-portuguese-sum" (pipeline("summarization")),
        "csevero/t5-base-ptbr-summ", etc.
    """
    tokenizer = T5Tokenizer.from_pretrained(model_name)  # T5Tokenizer => sempre "slow"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
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

    summarizer = get_summarizer_t5(model_name)
    texto_teste = "Este é um texto de exemplo para testar a sumarização em português."
    resultado = summarizer(texto_teste, max_length=50, min_length=10, do_sample=False)
    print("Resumo de teste:", resultado[0]["generated_text"])

# No terminal
#   python choose_model.py "unicamp-dl/ptt5-base-portuguese-vocab"
#   python choose_model.py