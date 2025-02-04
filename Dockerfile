# Dockerfile
FROM python:3.9
#FROM python:3.9-slim
#FROM pytorch/libtorch-cxx11-builder

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiamos APENAS o requirements.txt primeiro, para evitar reinstalar tudo
# sempre que alteramos qualquer script Python
COPY requirements.txt /app/
# Copiar os arquivos do projeto
# (Se você tiver muitas pastas, ajuste conforme necessário)
# COPY . /app

# Instalar dependências
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -v -r requirements.txt
# RUN pip install --no-cache-dir --progress-bar=on -r requirements.txt

# Ajusta para que o Python enxergue /app como PYTHONPATH 
# (assim "app/" vira um pacote de nível superior)
ENV PYTHONPATH=/app

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# docker build -t sumario_app .
# docker run -p 8501:8501 sumario_app

# docker run -p 8501:8501 \
#   -v $(pwd)/app:/app \
#   sumario_app