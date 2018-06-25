FROM python:3.6.5-jessie

COPY ./ /srv/app
WORKDIR /srv/app

RUN apt-get update && apt-get -y install curl unzip
RUN curl -OL https://github.com/google/protobuf/releases/download/v3.3.0/protoc-3.3.0-linux-x86_64.zip && \
    unzip protoc-3.3.0-linux-x86_64.zip -d protoc3  && \
    mv protoc3/bin/* /usr/local/bin/ && \
    mv protoc3/include/* /usr/local/include/

RUN make proto
RUN pip --no-cache-dir  install -r requirements.txt

CMD [ "python", "./main.py" ]
