install:
	git submodule update --init --recursive
	pip install -r requirements.txt

protoc:
	python -m grpc_tools.protoc -Iserver/proto=./proto \
		--python_out=. \
		--pyi_out=. \
		--grpc_python_out=. \
		proto/*.proto

run:
	python -m server
