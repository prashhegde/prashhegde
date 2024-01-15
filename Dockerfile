FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY server/ .

ENV PORT 8080

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
