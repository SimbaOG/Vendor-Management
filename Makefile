.PHONY: install
install:
	poetry install

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit install

.PHONY: uninstall-pre-commit
uninstall-pre-commit:
	poetry run pre-commit uninstall

.PHONY: linter
linter:
	poetry run pre-commit run --all-files

.PHONY: run-server
run-server:
	poetry run python -m core.manage runserver

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: update
update:	install migrate uninstall-pre-commit install-pre-commit;

