# Install dependencies and submodules
install:
	git submodule update --init --recursive
	pip install -r requirements.txt

# Generate the gRPC code from the proto files
protoc:
	python -m grpc_tools.protoc -Iserver/proto=./proto \
		--python_out=. \
		--pyi_out=. \
		--grpc_python_out=. \
		proto/*.proto

# Start the server
run-grpc:
	python -m server

# Start the server with a static telemetry file
run-grpc-test:
	python -m server --test __assets__/telemetry.bin

run-http:
	python -m server_http

run-http-test:
	python -m server_http --test __assets__/telemetry.bin

# Start the server and the envoy proxy
run-grpc-web:
	python -m server &
	docker-compose -f compose.yml up -d envoy

run-grpc-web-test:
	python -m server --test __assets__/telemetry.bin &
	docker-compose -f compose.yml up -d envoy

# Create a spec for compiling the .exe
spec-grpc:
	pyi-makespec --onefile server/__main__.py --name=telemetry-server-grpc

spec-http:
	echo "Removed"

exe-http:
	pyinstaller --clean --name telemetry-server-http --add-data="server_http\static;static" --additional-hooks-dir extra-hooks server_http/app.py -F

exe-grpc:
	pyinstaller telemetry-server-grpc.spec --clean --noconfirm --distpath dist

# Load test subscription streams
load-test-subscription:
	ghz --insecure --proto ./proto/telemetry.proto \
		--call iracing.telemetry.Telemetry/SubscribeTelemetryStream \
		-D ./load-test/subscription.json \
		-t 0 \
		-z 30s \
		-c 100 \
		0.0.0.0:50051

# Load test GetTelemetryJSONSchema
load-test-schema-struct:
	ghz --insecure --proto ./proto/schema.proto --call iracing.telemetry.Schema/GetTelemetryJSONSchema -t 0 -z 30s 0.0.0.0:50051

# Load test GetTelemetryJSONSchemaString
load-test-schema-string:
	ghz --insecure --proto ./proto/schema.proto --call iracing.telemetry.Schema/GetTelemetryJSONSchemaString -t 0 -z 30s 0.0.0.0:50051

# Load test GetTelemetry requests
load-test-telemetry:
	ghz --insecure --proto ./proto/telemetry.proto \
		--call iracing.telemetry.Telemetry/GetTelemetry \
		-D ./load-test/get-telemetry.json \
		-t 0 \
		-z 30s \
		-c 100 \
		-n 10000 \
		0.0.0.0:50051
