VERSION=0.0.1

build:
	docker build -t stock_price_retrieval:$(VERSION) stock_price_retrieval

run:
	docker-compose -f docker-compose.yml up -d
