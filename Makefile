ROOT=$(CURDIR)
GAME=bindingoffenrir
PYTHON ?= python


play:
	PYTHONPATH=${ROOT} ${PYTHON} ${GAME}/main.py

build:
	pyinstaller ${GAME}.spec

clean:
	rm -rfv ${ROOT}/build/
	rm -rfv ${ROOT}/dist/

execute:
	${ROOT}/dist/${GAME}.exe

resources:
	${ROOT}/dev/cpr.cmd

upload:
	${PYTHON} ${ROOT}/dev/upload.py

dropbox: clean
	@make build FULLSCREEN=true
	@make upload


.PHONY: play build clean execute resources upload dropbox