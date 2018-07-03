certificate:
	mkdir -p cert && \
	openssl req -nodes -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -subj "/C=RU/ST=Kaliningrad/L=Kaliningrad/O=KrasnoperovVitaliy/OU=Bullet/CN=*.krasnoperov.tk" -sha256

tdd:
	./runtests.sh

proto:
	rm -f protocol/*_pb2*
	rm -rf protocol/__pycache__
	find protocol -type f -name "*.proto" -exec protoc --python_out=. {} \;

clean:
	rm -rf .pytest_cache
	find protocol -type f -name "*_pb2*" -exec rm -f {} \;
	find . -type d -name "__pycache__" -exec rm -rf {} \;
