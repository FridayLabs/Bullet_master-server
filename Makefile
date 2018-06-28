certificate:
	mkdir -p cert && \
	openssl req -nodes -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -subj "/C=RU/ST=Kaliningrad/L=Kaliningrad/O=KrasnoperovVitaliy/OU=Bullet/CN=*.krasnoperov.tk" -sha256

proto:
	rm -f protocol/*_pb2*
	rm -rf protocol/__pycache__
	find protocol -type f -name "*.proto" -exec protoc --python_out=. {} \;
