# Start Web Scraping

FROM quay.io/bitnami/python:3.6.13-prod-debian-10-r87

WORKDIR /code

ENV LANG C.UTF-8

COPY requirements.txt .
COPY config.ini .

RUN pip install --no-cache-dir -r requirements.txt
RUN echo Asia/Shanghai >> /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR /code/data_collection

COPY data_collection/ .

CMD ["python", "main.py"]
