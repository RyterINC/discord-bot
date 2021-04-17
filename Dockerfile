FROM python:3.9.4-alpine

COPY . /app
WORKDIR /app
RUN apk add build-base && \
    pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]
