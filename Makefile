BOOTSTRAP_VERSION = 5.3.3
BOOTSTRAP_CSS_URL = https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/css/bootstrap.min.css
BOOTSTRAP_JS_URL = https://cdn.jsdelivr.net/npm/bootstrap@$(BOOTSTRAP_VERSION)/dist/js/bootstrap.bundle.min.js
BOOTSTRAP_CSS_DIR = static/vendor/bootstrap/css
BOOTSTRAP_JS_DIR = static/vendor/bootstrap/js

.PHONY: install bootstrap setup migrate makemigrations run test lint format shell superuser clean

install:
	poetry install

bootstrap:
	mkdir -p $(BOOTSTRAP_CSS_DIR) $(BOOTSTRAP_JS_DIR)
	curl -sL $(BOOTSTRAP_CSS_URL) -o $(BOOTSTRAP_CSS_DIR)/bootstrap.min.css
	curl -sL $(BOOTSTRAP_JS_URL) -o $(BOOTSTRAP_JS_DIR)/bootstrap.bundle.min.js
	@echo "Bootstrap $(BOOTSTRAP_VERSION) downloaded to static/vendor/bootstrap/"

setup: install bootstrap migrate
	@echo "Setup complete. Copy .env.example to .env and configure your settings."

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations

run:
	poetry run python manage.py runserver

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

shell:
	poetry run python manage.py shell

superuser:
	poetry run python manage.py createsuperuser

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .ruff_cache

