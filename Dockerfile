FROM python:3.8

WORKDIR /app

COPY server.py .
COPY requirements.txt .
RUN pip install -r requirements.txt \
 && pip freeze

EXPOSE 8080

CMD ["python", "server.py"]
