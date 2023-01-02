BOARD_PORT ?= /dev/ttyUSB0
START_SCRIPT ?= main.py

development-dependencies:
	@pipenv sync --dev

lint: development-dependencies
	@pipenv run flake8

fix-lint: development-dependencies
	@pipenv run black .

unit-test: development-dependencies
	@pipenv run python3 -m unittest

silent-unit-test: development-dependencies
	@pipenv run python3 -m unittest

test: lint unit-test

websocket-server: development-dependencies
	@pipenv run python3 ./misc/websocket-server/websocket_server.py

deploy: development-dependencies
	@pipenv run ampy --port $(BOARD_PORT) reset
	@pipenv run rshell -p $(BOARD_PORT) rsync -m ./source /pyboard

run: development-dependencies
	@pipenv run ampy --port $(BOARD_PORT) run ./source/main.py

deploy-run: deploy run

install-firmware: development-dependencies
	@echo "GET BOARD INTO BOOT MODE OR THIS WILL FAIL!"
	@pipenv run esptool.py --chip esp32 --port $(BOARD_PORT) erase_flash
	@pipenv run esptool.py --chip esp32 --port $(BOARD_PORT) write_flash -z 0x1000 ./misc/firmware/firmware.bin

