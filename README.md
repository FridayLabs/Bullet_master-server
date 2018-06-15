## Run prod:
1. Generate cert
```
mkdir cert && \
openssl req -nodes -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -subj "/C=RU/ST=Kaliningrad/L=Kaliningrad/O=KrasnoperovVitaliy/OU=Bullet/CN=ip.krasnoperov.tk" -sha256
```
1. Create .env file like .env.example
1. Run container
```
docker run neronmoon/bullet-master-server:latest \
--name bullet-master-server \
-v ./cert:/srv/app/cert \
--restart always \
--env-file .env \
--network="host"
```
