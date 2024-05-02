import argparse
import pathlib
import sys

from rancid_verifier.verification import VerificationResult, verify_file


def print_results(results: list[VerificationResult]) -> None:
    for result in results:
        if not result.error:
            status: str = "OK"
        else:
            status: str = "Error"
        print(f"{str(result.file_path)} {status}")


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument("path", help="Path to router.db")
    parser.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help=(
            "Dont print anything, "
            "exit with non-zero exit code if file contains errors."
        ),
    )

    return parser.parse_args()


def cli() -> None:
    args: argparse.Namespace = parse_args()

    results: list[VerificationResult] = []

    router_db_path = pathlib.Path(args.path)
    if not router_db_path.exists():
        if not args.quite:
            print(f"File {router_db_path} doesn't exist.")
        sys.exit(2)

    exit_code: int = 0

    result: VerificationResult = verify_file(router_db_path)
    if result.error:
        exit_code = 1
    results.append(result)

    if args.quite:
        sys.exit(exit_code)

    print_results(results)

    sys.exit(exit_code)
