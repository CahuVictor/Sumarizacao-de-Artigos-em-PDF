
# app.py
import streamlit as st
import tempfile
import os

#from app.summarize_article import summarize_article
# Dentro de app.py, que está em /app/app.py
#from summarize_article import summarize_article
from extract_text import extract_text_from_pdf
from summarize_article import chunk_text, summarize_chunk_t5, summarize_chunk_bart
# Você pode importar ou repetir algumas funções de "summarize_article"
# caso queira mais controle. Aqui uso chunk_text e as funções de chunk summarization.


def main():
    st.set_page_config(page_title="Sumarizador de Artigos", layout="wide")
    
    st.title("Sumarizador de Artigos em PDF")
    
    # Layout de colunas: col1 (sidebar "direita simulada"), col2 (conteúdo principal).
    col1, col2 = st.columns([1, 3])

    # --- SIDEBAR à esquerda: ---
    st.sidebar.header("Selecione as opções")

    model_type = st.sidebar.radio(
        "Tipo de modelo:",
        ("T5", "BART"),
        index=0
    )

    default_model_name = (
        "unicamp-dl/ptt5-base-portuguese-vocab"
        if model_type == "T5"
        else "Jonatas/bart-large-portuguese-sum"
    )

    model_name_input = st.sidebar.text_input(
        "Hugging Face Model Name:",
        value=default_model_name,
        #help="Ex: 'unicamp-dl/ptt5-base-portuguese-vocab' ou 'Jonatas/bart-large-portuguese-sum'"
    )

    chunk_size = st.sidebar.number_input("Tamanho do chunk (caracteres)", value=2000, min_value=500, max_value=10000, step=500)
    max_length = st.sidebar.number_input("Max Length (tokens)", value=512, min_value=50, max_value=2048, step=10)
    min_length = st.sidebar.number_input("Min Length (tokens)", value=50, min_value=10, max_value=512, step=5)

    uploaded_pdf = st.sidebar.file_uploader("Carregue um PDF", type=["pdf"])

    # --- Exemplo de barra lateral extra (ou se preferir, use col1) ---
    # Se quiser mesmo "duas" barras laterais, podemos usar col1 como uma "barra da direita":
    with col1:
        st.markdown("### Parâmetros Adicionais")
        st.write("Se necessário, adicione parâmetros extras aqui (fictícios ou futuros).")


    # --- Conteúdo principal (col2) ---
    with col2:
        st.subheader("Texto Extraído e Resumo")

        if uploaded_pdf is not None:
            # Precisamos salvar temporariamente o PDF para repassar ao summarize_article
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name

            if st.button("Gerar Resumo"):
                with st.spinner("Processando..."):
                    # Aqui chamamos nossa função principal
                    # final_summary = summarize_article(
                    #     pdf_path=tmp_path,
                    #     model_name=model_name_input,
                    #     model_type=model_type,
                    #     chunk_size=chunk_size,
                    #     max_length=max_length,
                    #     min_length=min_length
                    # )
                    # 1) Extrair texto
                    pdf_text = extract_text_from_pdf(tmp_path)
                    
                    # 2) Carregar o pipeline do modelo
                    if model_type == "T5":
                        from choose_model_t5_slow import get_summarizer_t5
                        summarizer = get_summarizer_t5(model_name_input)
                        summarize_func = summarize_chunk_t5
                    else:
                        from choose_model_bart import get_summarizer_bart
                        summarizer = get_summarizer_bart(model_name_input)
                        summarize_func = summarize_chunk_bart

                    # 3) Dividir texto em chunks
                    chunks = chunk_text(pdf_text, chunk_size=chunk_size)
                    st.write(f"Texto dividido em {len(chunks)} bloco(s).")

                    partial_summaries = []
                    # Criar uma barra de progresso
                    progress_bar = st.progress(0)

                    for i, chunk in enumerate(chunks, start=1):
                        st.write(f"**Processando chunk {i}/{len(chunks)}** (tamanho: {len(chunk)} caracteres)")

                        # Resumo parcial
                        partial_summary = summarize_func(
                            summarizer,
                            chunk,
                            max_length=max_length,
                            min_length=min_length
                        )
                        partial_summaries.append(partial_summary)

                        # Mostrar resumo parcial
                        st.write(f"**Resumo parcial {i} / {len(partial_summary)}:**")
                        st.write(partial_summary)

                        # Atualizar a barra de progresso
                        progress_bar.progress(i/len(chunks))
                    
                    if len(partial_summaries) > 1:
                        st.write(f"**Combinacao dos resusmos parciais ( {len(combined_text)} )...**")
                        combined_text = "\n".join(partial_summaries)
                        st.write(combined_text)
                    
                    partial_summaries_2 = []
                    group_size = 4
                    for i in range(0, len(partial_summaries), group_size):
                        group_text = "\n".join(partial_summaries[i:i+group_size])
                        sub_summary = summarize_func(summarizer, group_text, max_length, min_length)
                        partial_summaries_2.append(sub_summary)

                        # Mostrar resumo parcial
                        st.write(f"**Resumo parcial {i} / {len(sub_summary)}:**")
                        st.write(sub_summary)
                    
                    if len(partial_summaries_2) > 1:
                        st.write("**Combinacao dos novos resusmos parciais...**")
                        combined_text = "\n".join(partial_summaries_2)
                        st.write(combined_text)
                    
                    # Agora resumimos esses "sub-resumos" novamente
                    #final_text = "\n".join(partial_summaries_2)

                    try:
                        final_summary = summarize_func(
                            summarizer,
                            combined_text,
                            max_length=max_length,
                            min_length=min_length
                        )
                        return final_summary

                    except (ValueError, RuntimeError) as e:
                        # Aqui capturamos os erros mais prováveis
                        # (caso esteja tudo dentro de um ambiente Streamlit, podemos exibir com st.error)
                        print("ERRO ao gerar o resumo final:", str(e))
                        # Podemos retornar algo básico ou None
                        return "Ocorreu um erro ao gerar o resumo final: " + str(e)
                # else:
                #     # Caso tenha só 1 chunk
                #     return partial_summaries[0]

                    # Se houver mais de 1 chunk, gerar resumo final
                    # final_summary = partial_summaries[0]
                    # if len(partial_summaries) > 1:
                    #     st.write("**Gerando resumo final a partir dos resumos parciais...**")
                    #     combined_text = "\n".join(partial_summaries)
                    #     final_summary = summarize_func(
                    #         summarizer,
                    #         combined_text,
                    #         max_length=max_length,
                    #         min_length=min_length
                    #     )

                st.success("Resumo gerado!")
                st.write("### Resumo Final:")
                st.write(final_summary)
            else:
                st.info("Clique em 'Gerar Resumo' para iniciar.")
        else:
            st.warning("Por favor, carregue um arquivo PDF na barra lateral.")

if __name__ == "__main__":
    main()