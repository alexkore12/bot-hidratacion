# Makefile for bot-hidratacion
# Common development tasks

.PHONY: help install run test docker-build docker-run clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the bot"
	@echo "  make test         - Run tests"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make clean        - Clean temporary files"

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest -v

docker-build:
	docker build -t alexkore12/bot-hidratacion:latest .

docker-run:
	docker run -d --name bot-hidratacion \
		-e TELEGRAM_BOT_TOKEN=$$TELEGRAM_BOT_TOKEN \
		alexkore12/bot-hidratacion:latest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
