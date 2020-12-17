FROM python:3.7-slim-stretch

# EXPOSE 8008

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]

CMD ["app.py"]