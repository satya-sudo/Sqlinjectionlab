FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3-pip && apt-get install -y python3-venv

# RUN python3

COPY ./ /SqlInjections/

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /SqlInjections/requirements.txt

WORKDIR /SqlInjections

EXPOSE 8000

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD ["python3","manage.py","runserver", "0.0.0.0:8000"]