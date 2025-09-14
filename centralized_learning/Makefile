.PHONY: up upb stop down down-v local-up local-upb local-stop local-down local-down-v

up:
	docker compose -f ./docker-compose.yaml up -d

upb:
	docker compose -f ./docker-compose.yaml up -d --build

stop:
	docker compose -f ./docker-compose.yaml stop

down:
	docker compose -f ./docker-compose.yaml down

down-v:
	docker compose -f ./docker-compose.yaml down -v

local-up:
	docker compose -f ./docker-compose.local.yaml up -d

local-upb:
	docker compose -f ./docker-compose.local.yaml up -d --build

local-stop:
	docker compose -f ./docker-compose.local.yaml stop

local-down:
	docker compose -f ./docker-compose.local.yaml down

local-down-v:
	docker compose -f ./docker-compose.local.yaml down -v