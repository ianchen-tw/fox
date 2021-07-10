PRETTIER_CMDS:= better format lint
.PHONY: $(PRETTIER_CMDS) test

ALL: test

test:
	pytest tests

testcov:
	pytest --cov-report term-missing --cov=fox .

ready:
	poetry shell
	poetry install

stubgen :
	rm -rf stubs
	stubgen fox -o stubs
	make better

# lint and format code
define PRETTIER
	poetry run python scripts/prettier.py
endef
better:
	$(PRETTIER) all

format:
	$(PRETTIER) format

lint:
	$(PRETTIER) lint