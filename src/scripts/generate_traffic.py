#!/usr/bin/env python3
"""Traffic generator for testing orders-app observability in Prometheus and Grafana."""

import argparse
from collections import Counter
import random
import sys
import time
import urllib.error
import urllib.request

VALID_REQUESTS = [
    ("GET", "/"),
    ("GET", "/get-orders"),
    ("GET", "/get-customers"),
    ("GET", "/get-customers/CUST-5001"),
    ("GET", "/get-customers/CUST-5002"),
    ("GET", "/get-customers/CUST-5003"),
    ("POST", "/add-id/300"),
]

ERROR_REQUEST = ("GET", "/get-customers/CUST-9999")
LATENCY_REQUEST = ("GET", "/get-orders")

MODE_FIXED_REQUEST = {
    "errors": ERROR_REQUEST,
    "latency": LATENCY_REQUEST,
}


def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate controlled HTTP traffic against orders-app to verify "
            "Prometheus scraping, Grafana dashboards, and Alertmanager rules."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 src/scripts/generate_traffic.py --url http://127.0.0.1:54321\n"
            "  python3 src/scripts/generate_traffic.py --url http://127.0.0.1:54321 --mode mixed --duration 60\n"
            "  python3 src/scripts/generate_traffic.py --url http://127.0.0.1:54321 --mode errors --duration 75\n"
            "  python3 src/scripts/generate_traffic.py --url http://127.0.0.1:54321 --mode latency --duration 120\n"
        ),
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Base URL of orders-app (for example, output of 'minikube service orders-app-service --url').",
    )
    parser.add_argument(
        "--mode",
        choices=("normal", "mixed", "errors", "latency"),
        default="mixed",
        help=(
            "Traffic profile: 'normal' sends 200 OK requests only; "
            "'mixed' sends ~80%% 200 OK and ~20%% 404 errors (default); "
            "'errors' sends 404 requests only; "
            "'latency' targets /get-orders (0-4s simulated delay) to test p95 latency alerts."
        ),
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Total duration to send requests in seconds (default: 60).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.3,
        help="Delay in seconds between consecutive requests (default: 0.3).",
    )
    args = parser.parse_args()

    if args.duration <= 0:
        parser.error("--duration must be a positive integer.")
    if args.interval < 0:
        parser.error("--interval cannot be negative.")

    args.url = args.url.rstrip("/")
    return args


def send_request(base_url: str, method: str, path: str, timeout: float = 10.0) -> str:
    """Send a single HTTP request and return its status code category or error label."""
    req = urllib.request.Request(url=f"{base_url}{path}", method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return str(response.status)
    except urllib.error.HTTPError as exc:
        # HTTP 4xx/5xx responses raise HTTPError in urllib; record the exact status code
        return str(exc.code)
    except urllib.error.URLError as exc:
        print(f"Connection error calling {method} {path}: {exc.reason}", file=sys.stderr)
        return "connection_error"


def verify_target(base_url: str) -> bool:
    """Confirm orders-app is reachable via /metrics before starting the traffic loop."""
    status = send_request(base_url, "GET", "/metrics")
    if status != "200":
        print(
            f"Target check failed: GET {base_url}/metrics returned {status}. "
            "Check that orders-app is running and the URL is reachable.",
            file=sys.stderr,
        )
        return False
    return True


def choose_request(mode: str) -> tuple[str, str]:
    """Select the next (method, path) pair according to the requested traffic mode."""
    if mode in MODE_FIXED_REQUEST:
        return MODE_FIXED_REQUEST[mode]
    if mode == "mixed" and random.random() < 0.2:
        return ERROR_REQUEST
    return random.choice(VALID_REQUESTS)


def run_traffic(base_url: str, mode: str, duration: int, interval: float) -> Counter:
    """Run the timed traffic generation loop and return a Counter of response codes."""
    counts: Counter[str] = Counter()
    deadline = time.monotonic() + duration
    total_sent = 0
    progress_step = 10 if mode == "latency" else 20

    print(f"Sending '{mode}' traffic to {base_url} for {duration}s (interval={interval}s)...")
    try:
        while time.monotonic() < deadline:
            method, path = choose_request(mode)
            status = send_request(base_url, method, path)
            counts[status] += 1
            total_sent += 1

            # Print periodic progress so output stays responsive without flooding stdout
            if total_sent % progress_step == 0:
                print(f"  Sent {total_sent} requests so far (latest: {method} {path} -> {status})")

            if interval > 0:
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped early by user (Ctrl+C).")

    return counts


def print_summary(counts: Counter, elapsed: float) -> None:
    """Print an aggregate summary of sent requests and status code counts."""
    total = sum(counts.values())
    print("\n--- Traffic Generation Summary ---")
    print(f"Total requests: {total} in {elapsed:.1f}s")
    for status, count in sorted(counts.items()):
        print(f"  HTTP {status}: {count}")


def main() -> int:
    """Entry point for the orders-app traffic generator."""
    args = parse_args()
    if not verify_target(args.url):
        return 1

    start = time.monotonic()
    counts = run_traffic(args.url, args.mode, args.duration, args.interval)
    print_summary(counts, time.monotonic() - start)
    return 0


if __name__ == "__main__":
    sys.exit(main())
