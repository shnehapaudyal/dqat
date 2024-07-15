# Makefile

all: start

venv: venv/touchfile

venv/touchfile: requirements.txt
	virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/touchfile

npm/install: client/package-lock.json
	cd client; npm start

build: npm/install venv

client:
	cd client; npm start --silent

server:
	. venv/bin/activate; python main.py

start: build server client

.PHONY: all client server start