.PHONY: help build up down restart logs shell clean test

help: ## Hiển thị trợ giúp
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image
	docker-compose build

up: ## Khởi động containers
	docker-compose up -d

down: ## Dừng và xóa containers
	docker-compose down

restart: ## Khởi động lại containers
	docker-compose restart

logs: ## Xem logs (Ctrl+C để thoát)
	docker-compose logs -f

logs-tail: ## Xem 100 dòng logs cuối
	docker-compose logs --tail=100 -f

shell: ## Vào shell của container
	docker-compose exec mcp-servers bash

ps: ## Xem trạng thái containers
	docker-compose ps

clean: ## Dọn dẹp containers và images
	docker-compose down -v
	docker system prune -f

rebuild: ## Rebuild từ đầu
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

dev: ## Chạy ở chế độ development
	docker-compose up

prod: ## Chạy ở chế độ production
	docker-compose up -d

stop: ## Dừng containers (không xóa)
	docker-compose stop

start: ## Khởi động containers đã dừng
	docker-compose start

stats: ## Xem resource usage
	docker stats mcp-xiaozhi-vietnam

inspect: ## Inspect container
	docker inspect mcp-xiaozhi-vietnam

test: ## Chạy tests (nếu có)
	docker-compose run --rm mcp-servers python -m pytest

check-token: ## Kiểm tra biến MCP_ENDPOINT
	@if [ -z "$$MCP_ENDPOINT" ]; then \
		echo "⚠️  MCP_ENDPOINT chưa được set!"; \
		echo "Vui lòng:"; \
		echo "1. Set biến môi trường: export MCP_ENDPOINT='wss://...'"; \
		echo "2. Hoặc chỉnh sửa trực tiếp trong docker-compose.yml"; \
	else \
		echo "✓ MCP_ENDPOINT đã được set"; \
	fi
