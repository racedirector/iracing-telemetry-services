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

spec:
	pyi-makespec --onefile server/__main__.py --name=telemetry-server

load-test:
	ghz --insecure \
		--proto ./proto/telemetry.proto \
		--call iracing.telemetry.Telemetry \
		-t 0 \
		-z 20m \
		-d '{ "keys": ["LapDistPct", "CarIdxLapDistPct", "CarIdxSessionFlags", "CpuUsageFG", "CpuUsageBG"], "fps": 20 }' \
		0.0.0.0:50051
