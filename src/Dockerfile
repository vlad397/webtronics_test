FROM python:3.10.4

WORKDIR /usr/app

RUN pip install --upgrade pip --no-cache-dir
RUN apt-get update && apt-get -y dist-upgrade

COPY ./src/requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

#CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
CMD ["./entrypoint.sh"]