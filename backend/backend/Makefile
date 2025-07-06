export PYTHONPATH := $(PWD)

.PHONY: test test-cov

test: # Este é o alvo 'test'
	pytest -v 

test-cov: # Este é o alvo 'test-cov'
	pytest --cov=petfit --cov-report=term-missing -v 