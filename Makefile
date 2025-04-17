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

load-test-subscription:
	ghz --insecure --proto ./proto/telemetry.proto \
		--call iracing.telemetry.Telemetry/SubscribeTelemetryStream \
		-D ./load-test/subscription.json \
		-t 0 \
		-z 30s \
		-c 100 \
		0.0.0.0:50051

load-test-schema-struct:
	ghz --insecure --proto ./proto/telemetry.proto --call iracing.telemetry.Telemetry/GetTelemetryJSONSchema -t 0 -z 30s 0.0.0.0:50051

load-test-schema-string:
	ghz --insecure --proto ./proto/telemetry.proto --call iracing.telemetry.Telemetry/GetTelemetryJSONSchemaString -t 0 -z 30s 0.0.0.0:50051

load-test-telemetry:
	ghz --insecure --proto ./proto/telemetry.proto \
		--call iracing.telemetry.Telemetry/GetTelemetry \
		-D ./load-test/get-telemetry.json \
		-t 0 \
		-z 30s \
		-c 100 \
		-n 10000 \
		0.0.0.0:50051
