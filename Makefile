############################################ BUILD ############################################

.PHONY: build
build:
	python3 generate_ts.py
	docker-compose build
	docker-compose up

############################################ CLEAR ############################################

.PHONY: clear
clear:
	docker-compose -f docker-compose.yml down --remove-orphans

.PHONY: clear-networks
clear-networks:
	docker network prune

.PHONY: clear-all
clear-all: clear clear-networks
