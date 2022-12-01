FROM python:3.8.12-buster

COPY requirements.txt /requirements.txt


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn esports.api.fast_api:app --host 0.0.0.0 --port $PORT
