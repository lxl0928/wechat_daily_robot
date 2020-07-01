FROM python:3.7.4

RUN mkdir -p /app

WORKDIR /app

RUN apt-get update && apt-get install -y vim

COPY requirements.txt /app/

RUN pip --no-cache-dir install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN pip --no-cache-dir install timi-robot==1.0.1 -i https://pypi.org/simple

COPY . /app

CMD ["python3", "/app/run.py"]
