FROM python:3.4-alpine

EXPOSE 5000

COPY ./disruption_app /jobie-api
WORKDIR /jobie-api

RUN pip install -r requirements.txt

CMD ["python", "main.py"] 
