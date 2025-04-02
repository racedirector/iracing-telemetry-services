install:
	pip install -r requirements.txt

protoc:
	python -m grpc_tools.protoc -I./proto \
		--python_out=./proto \
		--pyi_out=./proto \
		--grpc_python_out=./proto \
		proto/broadcast.proto proto/telemetry.proto

run:
	python server.py