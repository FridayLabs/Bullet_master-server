run:
	docker-compose up

build:
	git submodule update && docker-compose build
