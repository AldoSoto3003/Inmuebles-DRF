FROM python

ENV PYTHONBUFFERED 1

RUN mkdir /drf_app

WORKDIR /drf_app

ADD . /drf_app/

RUN pip install -r requirements.txt
