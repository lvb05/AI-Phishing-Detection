FROM python:3.10-slim
WORKDIR /app
COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ../src ./src
COPY ../dashboard ./dashboard
COPY ../data ./data
COPY ../models ./models
EXPOSE 8501

ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
