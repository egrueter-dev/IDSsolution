FROM python:3.7

ENV PYTHONUNBUFFERED 1
COPY requirements_processing.txt .
COPY processing.py .
RUN pip install -r requirements_processing.txt
EXPOSE 5673

CMD ["python", "processing.py"]
