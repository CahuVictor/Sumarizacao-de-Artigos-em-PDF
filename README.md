# Sumarização de Artigos em PDF
 Este projeto é um desafio da disciplina Deep Learning do MBA Ciência de Dados e IA da Faculdade Senac.
 Grupo: 
* Cahú Victor
* Álvaro Tavares;
* Ariany Lima;
* Claúsia Gabriella;
* Gabriel Santana;
* Roberto Campelo.


 Este projeto tem como objetivo extrair texto de artigos acadêmicos em PDF e gerar um resumo estruturado, focando em informações como autores, ano, revista/jornal, principais resultados e metodologia aplicada. Ele utiliza bibliotecas Python, como o pdfplumber para extração de texto, e Transformers (Hugging Face) para a sumarização. Também conta com uma interface desenvolvida em Streamlit, o que facilita a interação com diferentes modelos (por exemplo, T5 ou BART) e permite configurar parâmetros como tamanho de chunk ou limites de tokens. Além disso, o projeto pode ser executado localmente ou dentro de um container Docker, garantindo maior portabilidade e facilidade de implantação.

# Como Utilizar
Baixar os arquivos, a hierarquia das pastas e arquivos deve estar da seguinte forma

 projeto/
 │
 ├── app/
 │   ├── app.py                     # Script principal Streamlit
 │   ├── extract_text_plumber.py    # (1) Extrair texto de PDF
 │   ├── choose_model_t5.py         # (2a) Script do modelo T5
 │   ├── choose_model_bart.py       # (2a) Script do modelo BART
 │   ├── define_summary_specs.py    # (3) Define prompt e/ou formatação
 │   ├── summarize_article.py       # (4) Gerar o resumo final usando o modelo
 │   └── __init__.py
 ├── requirements.txt           # Lista de dependências
 ├── Dockerfile                 # Definição do container Docker
 └── README.md

# Instalar Dependências
## No Windows
Instale o Docker Desktop e o Viscual Studio Code (VSCode).
No VSCode instale a extensão Docker for Visual Studio Code Version da Microsoft.

# Construindo o Container
Para construir o Container do projeto, no terminal do VSCode navegue até a pasta onde está o projeto e execute o seguinte comnado na linha de comando.
docker build -t sumario_app .

Este comando irá construir o Container do projeto, este processo pode demorar um pouco, no meu caso demorou quase 30 minutos.

# Inicializando o Container
Com o Container construído, executar o seguinte comando

No windows
docker run -p 8501:8501 \
  -v $(pwd)/app:/app \
  sumario_app

docker run -p 8501:8501 -v ${pwd}/app:/app sumario_app

No Windows, pode ser necessário trocar $(pwd) por ${PWD} ou usar o caminho completo, ex: -v "C:\Users\Fulano\seu_projeto\app:/app".

# PDF Article Summarization
This project is a challenge from the Deep Learning course in the Data Science and AI MBA program at Faculdade Senac.

The goal of this project is to extract text from academic PDF articles and generate a structured summary, focusing on information such as authors, publication year, journal/conference, key results, and applied methodology. It uses Python libraries such as pdfplumber for text extraction and Hugging Face Transformers for summarization. It also features a Streamlit interface, which simplifies interaction with different models (e.g., T5 or BART) and allows configuration of parameters such as chunk size or token limits. Furthermore, the project can be run locally or inside a Docker container, ensuring greater portability and ease of deployment.