FROM python:3.6.11

RUN mkdir -p /app

WORKDIR /app

RUN apt-get update && apt-get install -y vim

COPY requirements.txt /app/

RUN pip --no-cache-dir install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /app

CMD ["python3", "/app/run.py"]
