FROM python:3.5

COPY ./api/ /api
WORKDIR /api

RUN pip install -r requirements.txt
EXPOSE 5000

CMD python ./api.py