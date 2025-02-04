

import sys
from textwrap import wrap

# (1) Função para extrair texto
from extract_text import extract_text_from_pdf

# (2) Função que constrói o "prompt" (caso use T5)
from define_summary_specs import build_summary_prompt

def chunk_text(text, chunk_size=2000):
    """
    Divide uma string grande em blocos (chunks) de tamanho máximo 'chunk_size' caracteres.
    Retorna uma lista de strings.
    """
    # Uma forma simples é usar wrap ou slicing. Ex:
    #   wrap(text, width=chunk_size) divide em linhas,
    #   mas iremos usar slicing manual para mantermos blocos "integrais".
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        # Pega o trecho de 'start' até 'end'
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks

def summarize_chunk(summarizer, chunk, max_length=512, min_length=50):
    """
    Gera o resumo de um único chunk usando o pipeline 'summarizer' (T5).
    """
    prompt = build_summary_prompt(chunk)
    summary = summarizer(
        prompt,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]["generated_text"]

def summarize_chunk_t5(summarizer, text_chunk, max_length=512, min_length=50):
    """
    Resumo de um chunk usando T5 (precisa de prompt).
    """
    prompt = build_summary_prompt(text_chunk)
    summary = summarizer(
        prompt,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]["generated_text"]

def summarize_chunk_bart(summarizer, text_chunk, max_length=512, min_length=50):
    """
    Resumo de um chunk usando BART (basta passar o texto).
    """
    summary = summarizer(
        text_chunk,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]["summary_text"]

def summarize_article(
    pdf_path,
    model_name,
    model_type="T5",
    chunk_size=2000,
    max_length=512,
    min_length=50,
):
    """
    1) Extrai texto do PDF.
    2) Divide em chunks para não estourar limite.
    3) Gera resumo parcial de cada chunk.
    4) (Opcional) Gera um resumo final dos resumos parciais (hierarchical summarization).
    """
    # Passo 1: Extrair texto
    article_text = extract_text_from_pdf(pdf_path)

    # Passo 2: Dividir em chunks
    chunks = chunk_text(article_text, chunk_size=chunk_size)
    print(f"Texto dividido em {len(chunks)} bloco(s).")
    
    # Passo 3:  Carregar o modelo de acordo com model_type
    #    (evitando import circular, fazemos import aqui)
    if model_type == "T5":
        from choose_model_t5_slow import get_summarizer_t5
        summarizer = get_summarizer_t5(model_name)
        summarize_func = summarize_chunk_t5
    else:
        from choose_model_bart import get_summarizer_bart
        summarizer = get_summarizer_bart(model_name)
        summarize_func = summarize_chunk_bart

    # Passo 4: Resumir cada chunk
    partial_summaries = []
    #for chunk in chunks:
    for i, chunk in enumerate(chunks, start=1):
        print(f"\n[Resumo parcial {i}/{len(chunks)}] Tamanho do chunk: {len(chunk)} caracteres")
        partial_summary = summarize_func(
            summarizer,
            chunk,
            max_length=max_length,
            min_length=min_length
        )
        
        #partial_summaries.append(summarize_func(summarizer, chunk, max_length, min_length))
        partial_summaries.append(partial_summary)
        print(f"Resumo do chunk {i} de tamanho {len(partial_summary)}:\n{partial_summary}")

    # Se houver mais de um chunk, unifica para gerar um "resumo do resumo"
    if len(partial_summaries) > 1:
        # Unir todos os resumos parciais
        combined_text = "\n".join(partial_summaries)
        print("\nGerando resumo final a partir dos resumos parciais...\n")
        # Resumir novamente
        final_summary = summarize_func(summarizer, combined_text, max_length, min_length)
        return final_summary
    else:
        # Apenas 1 chunk => o resumo parcial é o final
        return partial_summaries[0]

if __name__ == "__main__":
    """
    Exemplo de uso no terminal:

        python summarize_article.py /caminho/artigo.pdf "unicamp-dl/ptt5-base-portuguese-vocab"
    
    Ou se não passar o nome do modelo, usa o default "unicamp-dl/ptt5-base-portuguese-vocab".
    """
    if len(sys.argv) < 2:
        print("Uso: python summarize_article.py <caminho_pdf> [<modelo>]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    if len(sys.argv) > 2:
        model_name = sys.argv[2]
    else:
        model_name = "unicamp-dl/ptt5-base-portuguese-vocab"

    # Ajuste aqui se quiser outra granularidade de chunk, ex: 1500 ou 1024
    chunk_size = 2000

    # Gera o resumo
    # if (chunk_size <= 0):
    #     resumo_final = summarize_article(
    #         pdf_path, 
    #         model_name=model_name
    #     )
    # else:
    #     resumo_final = summarize_article(
    #         pdf_path,
    #         model_name=model_name,
    #         chunk_size=chunk_size,
    #         max_length=512,
    #         min_length=50
    #     )
    resumo_final = summarize_article(
        pdf_path,
        model_name=model_name,
        model_type="T5",
        chunk_size=chunk_size,
        max_length=512,
        min_length=50
    )

    print("\n--- RESUMO FINAL ---\n")
    print(resumo_final)