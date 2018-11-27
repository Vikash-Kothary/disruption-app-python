FROM python:3.4

EXPOSE 5000

COPY ./jobie_api /jobie-api
WORKDIR /jobie-api

RUN apt-get install python libxml2 zlib1g
RUN pip install -r requirements.txt

CMD ["python", "main.py"] 
