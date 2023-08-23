FROM python:3.11.3

ENV PYTHONUNBUFFERD 1
RUN mkdir /CODE
WORKDIR /CODE
COPY . /CODE/
RUN pip install -r requirements.txt
