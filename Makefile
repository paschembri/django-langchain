.PHONY: setup


venv:
	@python3.9 -m venv venv
	-ln -s venv/bin .


setup: venv
	@venv/bin/pip3 install -U pip
	@venv/bin/pip3 install -r requirements.txt
	@venv/bin/pip3 install -e .

