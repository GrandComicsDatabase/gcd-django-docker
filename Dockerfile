# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set work directory
RUN mkdir /code
WORKDIR /code
# install external packages
RUN apt-get update && apt-get install -y netcat && apt-get install -y vim
# install GCD code and python packages
ADD https://api.github.com/repos/GrandComicsDatabase/gcd-django/git/refs/heads/master version.json
RUN git clone https://github.com/GrandComicsDatabase/gcd-django.git
RUN cp /code/gcd-django/requirements.txt /code
RUN pip install -r requirements.txt
COPY ./settings_local.py /code/gcd-django/
COPY . /code/
