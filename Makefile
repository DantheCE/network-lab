.PHONY: up down clean

up:
	sudo clab deploy -t topology/lab.clab.yml

down:
	sudo clab destroy -t topology/lab.clab.yml --cleanup

clean: down
