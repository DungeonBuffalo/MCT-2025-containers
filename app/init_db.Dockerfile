FROM python:3.12.9

WORKDIR /init
COPY app/init_db.py .

RUN pip install psycopg2-binary

CMD ["python", "init_db.py"]