## Run prod:
- Generate cert
```
mkdir cert && \
openssl req -nodes -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -subj "/C=RU/ST=Kaliningrad/L=Kaliningrad/O=KrasnoperovVitaliy/OU=Bullet/CN=ip.krasnoperov.tk" -sha256
```
- Create .env file like .env.example
- Run container
```
docker run -it --rm --mount type=bind,source="$(pwd)"/cert,target=/srv/app/cert --env-file .env -p 9999:9999 neronmoon/bullet-master-server:master-25
```

## Kill:
```
docker kill bullet-master-server && docker rm bullet-master-server
```

## Tests:
```
docker run -it --mount type=bind,source="$(pwd)"/,target=/srv/app/ neronmoon/bullet-master-server:master-27 python -m pytest -v --cov-report term-missing --cov --cov-fail-under 80 --pdb
```
