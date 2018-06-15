certificate-dev:
	mkdir cert && \
	openssl req -nodes -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -subj "/C=RU/ST=Kaliningrad/L=Kaliningrad/O=KrasnoperovVitaliy/OU=Bullet/CN=0.0.0.0" -sha256

certificate-prod:
	mkdir cert && \
	openssl req -nodes -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -subj "/C=RU/ST=Kaliningrad/L=Kaliningrad/O=KrasnoperovVitaliy/OU=Bullet/CN=ip.krasnoperov.tk" -sha256

proto:
	protoc --python_out=. protocol/*.proto

up-prod:
	git submodule update --init && docker-compose -f docker-compose.prod.yml up
