FROM fnndsc/ubuntu-python3:latest

COPY ./ /srv/app
WORKDIR /srv/app

RUN apt-get update && \
    apt-get -y install curl unzip
RUN curl -OL https://github.com/google/protobuf/releases/download/v3.3.0/protoc-3.3.0-linux-x86_64.zip && \
    unzip protoc-3.3.0-linux-x86_64.zip -d protoc3  && \
    mv protoc3/bin/* /usr/local/bin/ && \
    mv protoc3/include/* /usr/local/include/

RUN protoc --python_out=src protocol/*.proto
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]
