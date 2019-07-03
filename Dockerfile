FROM python:3.7-slim-stretch
ENV PYTHONUNBUFFERED 1

# RUN apk update && apk add --virtual .build-deps gcc libc-dev linux-headers make musl-dev pcre-dev netcat-openbsd
RUN apt update
RUN apt install -y python3-dev gcc

WORKDIR /usr/src/app

RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip install fastai

# Install starlette and uvicorn
RUN pip install starlette uvicorn python-multipart aiohttp

COPY eth_gen.py eth_gen.py
COPY export.pkl export.pkl

EXPOSE 8008

CMD ["python", "eth_gen.py", "serve"]
