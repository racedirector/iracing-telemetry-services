"""CLI entry‑point:  python -m server_ws  (same as `make run-ws`)."""
import argparse, uvicorn
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--reload", action="store_true")
    ap.add_argument("--test", type=Path,
                    help="Pass a .bin telemetry file for offline testing")
    ns = ap.parse_args()

    if ns.test:
        import os
        os.environ["PYIRSDK_TEST_FILE"] = str(ns.test)

    uvicorn.run(
        "server_ws.app:app",
        host=ns.host,
        port=ns.port,
        reload=ns.reload,
    )

if __name__ == "__main__":  # pragma: no cover
    main()
