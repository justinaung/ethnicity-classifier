FROM python:3.7.3-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --virtual .build-deps gcc libc-dev linux-headers make musl-dev pcre-dev netcat-openbsd
RUN pip install pipenv 

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . /usr/src/app

EXPOSE 8008

CMD ["python", "eth_gen.py", "serve"]
