BOARD_PORT ?= /dev/ttyUSB0
MICROPYTHON_FIRMWARE_PATH ?= ./misc/firmware/firmware.bin

development-dependencies:
	@pipenv sync --dev

lint: development-dependencies
	@pipenv run flake8 --ignore=E402

fix-lint: development-dependencies
	@pipenv run black .

unit-test: development-dependencies
	@pipenv run python3 -m unittest

test: lint unit-test

deploy: development-dependencies
	@pipenv run ampy --port $(BOARD_PORT) reset
	@pipenv run rshell -p $(BOARD_PORT) rsync -m ./source /pyboard

run: development-dependencies
	@pipenv run mpremote connect $(BOARD_PORT) mount ./source exec "import main"

install-firmware: development-dependencies
	@echo "GET BOARD INTO BOOT MODE OR THIS WILL FAIL!"
	@pipenv run esptool.py --chip esp32 --port $(BOARD_PORT) erase_flash
	@pipenv run esptool.py --chip esp32 --port $(BOARD_PORT) write_flash -z 0x1000 $(MICROPYTHON_FIRMWARE_PATH)

websocket-server: development-dependencies
	@pipenv run python3 ./misc/websocket-server/websocket_server.py
