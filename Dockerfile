FROM python:3.13-alpine3.23

WORKDIR /app

RUN apk --no-cache add curl

COPY ./app.py ./app.py

RUN pip install --no-cache-dir streamlit
RUN pip install --no-cache-dir --upgrade setuptools

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
