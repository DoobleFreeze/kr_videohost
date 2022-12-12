FROM python:3.8

WORKDIR /opt/app

COPY /requirements.txt .

RUN pip3 install -r /opt/app/requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 app:app
