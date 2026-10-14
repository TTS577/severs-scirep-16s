.PHONY: figures clean

FIGURE_SCRIPTS := $(wildcard figures/scripts/*.py)

figures:
	@mkdir -p figures/output
	@for script in $(FIGURE_SCRIPTS); do \
		echo "Running $$script"; \
		python $$script; \
	done

clean:
	rm -rf figures/output/* data/interim/* data/processed/*
