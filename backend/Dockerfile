FROM python:3.11

WORKDIR /app

COPY ./requirements.txt .

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip3 install -r requirements.txt

COPY *.py .
COPY classifier/ ./classifier/
COPY data/ ./data/
COPY embedding/ ./embedding/
COPY *.rb .

EXPOSE 5000

CMD ["python", "server.py"]
