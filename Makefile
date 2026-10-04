.PHONY: up down clean deploy verify test

up:
	sudo clab deploy -t topology/lab.clab.yml

down:
	sudo clab destroy -t topology/lab.clab.yml --cleanup

clean: down

deploy:
	python3 automation/deploy.py

verify:
	python3 automation/verify.py

test:
	python3 -m pytest tests/
