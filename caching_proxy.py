import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Caching Proxy Server")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--origin", type=str, help="Upstream base URL")
    parser.add_argument("--ttl", type=int, help="Cache TTL in seconds")

    args = parser.parse_args()

    if args.origin:
        os.environ["UPSTREAM_BASE_URL"] = args.origin

    if args.ttl:
        os.environ["CACHE_TTL"] = str(args.ttl)

    command = [
        "uvicorn",
        "app.main:app",
        "--reload",
        "--port",
        str(args.port),
    ]

    subprocess.run(command)

if __name__ == "__main__":
    main()