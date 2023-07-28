# syntax=docker/dockerfile:1.4
FROM python:3.9-alpine

EXPOSE 5000

RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev && apk add libffi-dev
WORKDIR /code
COPY requirements.txt /code/requirement.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirement.txt
COPY aliddns.py /code

CMD ["python", "./aliddns.py", ""]
