FROM python:3.7.5-slim

ADD requirements.txt /

RUN pip3 install -r requirements.txt

ADD . /

CMD ["python", "main.py"]
