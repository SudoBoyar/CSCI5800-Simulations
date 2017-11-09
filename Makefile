build: Dockerfile
	docker build -t simpynb .

run: build
	docker run --name craps --rm -it -d -p 8888:8888 -v `pwd`:/home/jovyan/work simpynb

stop:
	docker stop craps

terminal:
	docker exec -i -t craps /bin/bash
