# syntax=docker/dockerfile:1.4
FROM python:3.10

EXPOSE 5000

WORKDIR /code
COPY requirements.txt /code/requirement.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirement.txt
COPY aliddns.py /code

ENV NAME_IPV4=www
ENV NAME_IPV6=www

CMD ["python", "./aliddns.py", ""]
