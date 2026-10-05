.PHONY: up down clean deploy verify test

up:
	sudo clab deploy -t topology/lab.clab.yml

down:
	sudo clab destroy -t topology/lab.clab.yml --cleanup

clean: down monitoring-down

monitoring-up:
	docker compose -f monitoring/docker-compose.yml up -d

monitoring-down:
	docker compose -f monitoring/docker-compose.yml down

deploy:
	python3 automation/deploy.py

verify:
	python3 automation/verify.py

test:
	python3 -m pytest tests/
