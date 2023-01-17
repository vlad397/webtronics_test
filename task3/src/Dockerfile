FROM python:3.10.4

WORKDIR /usr/app

RUN pip install --upgrade pip --no-cache-dir
RUN apt-get update && apt-get -y dist-upgrade

COPY ./src/requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["./entrypoint.sh"]