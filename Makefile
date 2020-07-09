.PHONY: coverage-server

coverage-server:
	@cd htmlcov && python -m http.server 5000
