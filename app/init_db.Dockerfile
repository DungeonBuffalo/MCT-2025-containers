FROM python:3.12

WORKDIR /init
COPY app/init_db.py .
RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "init_db.py"]