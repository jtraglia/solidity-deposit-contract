SOURCE = deposit_contract.sol
OUTPUT = deposit_contract.json

.PHONY: all compile_deposit_contract test clean

all: compile_deposit_contract test

compile_deposit_contract:
	@solc --metadata-literal --optimize --optimize-runs 5000000 --bin --abi \
		--combined-json=abi,bin,bin-runtime,srcmap,srcmap-runtime,ast,metadata,storage-layout \
		--overwrite -o build $(SOURCE)
	@/bin/echo -n '{"abi": ' > $(OUTPUT)
	@cat build/DepositContract.abi >> $(OUTPUT)
	@/bin/echo -n ', "bytecode": "0x' >> $(OUTPUT)
	@cat build/DepositContract.bin >> $(OUTPUT)
	@/bin/echo -n '"}' >> $(OUTPUT)

test:
	@uv sync
	@uv run pytest -v

clean:
	@rm -rf build .pytest_cache
