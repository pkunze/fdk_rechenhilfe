FROM python:3.13-alpine3.23

WORKDIR /app

COPY ./app.py ./app.py

RUN pip install --no-cache-dir streamlit

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
