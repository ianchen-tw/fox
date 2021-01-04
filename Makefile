PRETTIER_CMDS:= better format lint
.PHONY: $(PRETTIER_CMDS) test

ALL: test

test:
	pytest

# lint and format code
define PRETTIER
	poetry run python3 scripts/prettier.py
endef
better:
	$(PRETTIER) all

format:
	$(PRETTIER) format

lint:
	$(PRETTIER) lint