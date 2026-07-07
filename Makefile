include .env
export

export PROJECT_ROOT=$(shell pwd)

env-up:
	@docker compose up -d

env-down:
	@docker compose down
