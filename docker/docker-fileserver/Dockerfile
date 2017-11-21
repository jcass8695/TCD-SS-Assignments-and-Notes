FROM python:3.5-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV http_proxy http://www-proxy.scss.tcd.ie:8080
ENV https_proxy http://www-proxy.scss.tcd.ie:8080

CMD ["python3", "node.py"]
