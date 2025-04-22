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
run:
	python -m server

# Start the server with a static telemetry file
run-test:
	python -m server --test __assets__/telemetry.bin

run-http:
	python -m server_http

run-http-test:
	python -m server_http --test __assets__/telemetry.bin

# Start the server and the envoy proxy
run-web:
	python -m server &
	docker-compose -f compose.yml up -d envoy

run-web-test:
	python -m server --test __assets__/telemetry.bin &
	docker-compose -f compose.yml up -d envoy

# Create a spec for compiling the .exe
spec-grpc:
	pyi-makespec --onefile server/__main__.py --name=telemetry-server-grpc

spec-http:
	pyi-makespec --onefile server_http/__main__.py --name=telemetry-server-http

exe-http:
	pyinstaller telemetry-server-http.spec

exe-grpc:
	pyinstaller telemetry-server-grpc.spec

# Create a spec for compiling the WebSocket‑server .exe
spec-ws:
	pyi-makespec --onefile server_ws/__main__.py --name=telemetry-ws

# ─────────────── Build a Windows executable for the WebSocket server ───────────────
# Requires: telemetry-ws.spec in the project root
#
# Usage:
#   make exe-ws     → dist/telemetry-ws.exe
# ────────────────────────────────────────────────────────────────────────────────────
exe-ws:
	pyinstaller telemetry-ws.spec --noconfirm --clean --distpath dist

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

# ───────────────────────── WebSocket service ─────────────────────────
# Start the JSON‑over‑WebSocket API on port 8000                       #
#                                                                      #
#   make run-ws          – live data from iRacing                      #
#   make run-ws-test     – replay static __assets__/telemetry.bin      #
# ──────────────────────────────────────────────────────────────────────

run-ws:
	python -m server_ws

run-ws-test:
	python -m server_ws --test __assets__/telemetry.bin
