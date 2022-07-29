createsuperuser:
	docker compose -f docker-compose.yml exec notification-service-admin python manage.py createsuperuser

makemigrations:
	docker compose -f docker-compose.yml exec notification-service-admin python manage.py makemigrations

migrate:
	docker compose -f docker-compose.yml exec notification-service-admin python manage.py migrate

up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down --volumes

deploy:
	make up && make makemigrations && make migrate && make createsuperuser