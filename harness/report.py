import json
from dataclasses import asdict
from pathlib import Path


def print_console_report(summary) -> None:
    print("\nHarness run result")
    print("=" * 18)

    for result in summary.results:
        marker = "PASS" if result.passed else "FAIL"
        print(f"[{marker}] {result.name} ({result.duration_ms:.2f} ms)")
        if result.error:
            print(f"       {result.error}")

    print("-" * 18)
    print(
        f"total={summary.total}, passed={summary.passed}, "
        f"failed={summary.failed}, duration={summary.duration_ms:.2f} ms"
    )


def write_json_report(summary, report_file: Path) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(
        json.dumps(asdict(summary), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
