
test:
	go test -coverprofile coverage.out ./...
	go tool cover -func=coverage.out


build:
	GODEBUG=cgocheck=0 go build -o dist/tilty

run:
	sudo ./dist/tilty -c test.ini

build-docker:
	docker-compose build

run-docker: build-docker
	docker-compose run tilty
