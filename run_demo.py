from pathlib import Path

from harness.runner import HarnessRunner


def main() -> int:
    root = Path(__file__).parent
    runner = HarnessRunner(
        case_file=root / "cases" / "price_cases.json",
        report_file=root / "reports" / "result.json",
    )
    summary = runner.run()
    return 0 if summary.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
