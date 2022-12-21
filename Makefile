############################################ BUILD ############################################

.PHONY: build
build:
	docker-compose up --build
#	docker-compose -f docker-compose.yml build --force-rm --parallel

############################################ CLEAR ############################################

.PHONY: clear
clear:
	docker-compose -f docker-compose.yml down --remove-orphans

.PHONY: clear-networks
clear-networks:
	docker network prune

.PHONY: clear-all
clear-all: clear clear-networks
