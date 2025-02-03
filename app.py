
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

# app.py
import streamlit as st
import tempfile
import os

from summarize_article import summarize_article

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
    help="Ex: 'unicamp-dl/ptt5-base-portuguese-vocab' ou 'Jonatas/bart-large-portuguese-sum'"
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
                final_summary = summarize_article(
                    pdf_path=tmp_path,
                    model_name=model_name_input,
                    model_type=model_type,
                    chunk_size=chunk_size,
                    max_length=max_length,
                    min_length=min_length
                )

            st.success("Resumo gerado!")
            st.write("### Resumo Final:")
            st.write(final_summary)
        else:
            st.info("Clique em 'Gerar Resumo' para iniciar.")
    else:
        st.warning("Por favor, carregue um arquivo PDF na barra lateral.")
