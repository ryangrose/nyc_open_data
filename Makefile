clean:
	rm nyc_open_data/models.py || true

generate-models: clean
	poetry run python codegen/gen.py
	# poetry run black nyc_open_data/models.py
