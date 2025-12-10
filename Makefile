clean-venv:
	@echo "Cleaning up"
	rm -rf .venv

venv:
	@echo "Creating env"
	uv sync

run:
	uv run main.py