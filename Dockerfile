FROM python:3.6

RUN apt-get update && apt-get upgrade -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]