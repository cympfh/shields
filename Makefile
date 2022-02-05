TAG := shields
PORT := 8080

build:
	docker build -t $(TAG) .

run: build
	docker run -it -p $(PORT):$(PORT) -e PORT=$(PORT) $(TAG)
