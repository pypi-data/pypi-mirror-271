import pathlib
from dataclasses import dataclass, field
from typing import Union


@dataclass
class VerificationResult:
    file_path: pathlib.Path
    error: bool = False
    line_errors: list[int] = field(default_factory=list)


def verify_lines(lines: list[str]) -> list[int]:
    errors: list[int] = []
    for line_number, line in enumerate(lines, start=1):
        if line.startswith("#"):
            continue
        if len(line.strip()) == 0:
            continue

        line_parts = line.split(";", maxsplit=3)

        if len(line_parts) not in (3, 4):
            errors.append(line_number)
            continue

        for line_part in line_parts[0:3]:
            try:
                line_part.encode(encoding="utf-8").decode("ascii")
            except UnicodeDecodeError:
                errors.append(line_number)
                break

    return errors


def verify_file(file_path: Union[str, pathlib.Path]) -> VerificationResult:
    file_path = pathlib.Path(file_path)
    result = VerificationResult(file_path=pathlib.Path(file_path))

    try:
        router_db_lines: list[str] = open(file_path, "r", encoding="utf-8").readlines()
    except UnicodeDecodeError:
        result.error = True
        return result

    result.line_errors = verify_lines(router_db_lines)
    if len(result.line_errors) > 0:
        result.error = True

    return result
