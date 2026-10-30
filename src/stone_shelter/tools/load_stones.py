"""Send authored stone requests through the running application's HTTP endpoint."""

import argparse
import asyncio
from pathlib import Path
from uuid import UUID

import httpx


async def load_stones(client: httpx.AsyncClient, directory: Path) -> int:
    files = sorted(directory.glob("*.json"))
    if not directory.is_dir() or not files:
        print(f"ERROR: no JSON requests found in {directory}")
        return 1

    succeeded = 0
    for request_file in files:
        try:
            response = await client.post(
                "/api/v1/stones",
                content=request_file.read_bytes(),
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != 201:
                print(f"FAILED {request_file.name}: HTTP {response.status_code} {response.text}")
                continue
            created_id = UUID(response.json()["id"])
        except httpx.RequestError as error:
            print(
                f"FAILED {request_file.name}: {type(error).__name__}; "
                "server outcome may be unknown; not retried."
            )
            continue
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"FAILED {request_file.name}: {type(error).__name__}: {error}")
            continue

        succeeded += 1
        print(f"CREATED {request_file.name}: {created_id}")

    failed = len(files) - succeeded
    print(f"Completed: {succeeded} created, {failed} failed, {len(files)} total.")
    return 1 if failed else 0


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--directory", type=Path, default=Path("fixtures/stones"))
    arguments = parser.parse_args()
    async with httpx.AsyncClient(base_url=arguments.base_url, timeout=30.0) as client:
        return await load_stones(client, arguments.directory)


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
