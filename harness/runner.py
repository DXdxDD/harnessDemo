import json
import time
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from harness.assertions import AssertionFailure, assert_mapping_matches
from harness.report import print_console_report, write_json_report
from src.price_engine import OrderItem, calculate_order_total, money


@dataclass(frozen=True)
class CaseResult:
    name: str
    passed: bool
    duration_ms: float
    actual: dict[str, Any] | None
    error: str | None


@dataclass(frozen=True)
class RunSummary:
    total: int
    passed: int
    failed: int
    duration_ms: float
    results: list[CaseResult]


class HarnessRunner:
    def __init__(self, case_file: Path, report_file: Path) -> None:
        self.case_file = case_file
        self.report_file = report_file

    def run(self) -> RunSummary:
        start = time.perf_counter()
        cases = self._load_cases()
        results = [self._run_case(case) for case in cases]
        duration_ms = (time.perf_counter() - start) * 1000

        passed = sum(1 for result in results if result.passed)
        summary = RunSummary(
            total=len(results),
            passed=passed,
            failed=len(results) - passed,
            duration_ms=duration_ms,
            results=results,
        )

        print_console_report(summary)
        write_json_report(summary, self.report_file)
        return summary

    def _load_cases(self) -> list[dict[str, Any]]:
        raw = self.case_file.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("case file must contain a JSON list")
        return data

    def _run_case(self, case: dict[str, Any]) -> CaseResult:
        start = time.perf_counter()
        name = case.get("name", "<unnamed>")

        try:
            actual = self._execute(case)
            assert_mapping_matches(actual, case["expected"])
            return CaseResult(
                name=name,
                passed=True,
                duration_ms=self._elapsed_ms(start),
                actual=actual,
                error=None,
            )
        except (AssertionFailure, Exception) as exc:
            return CaseResult(
                name=name,
                passed=False,
                duration_ms=self._elapsed_ms(start),
                actual=None,
                error=f"{type(exc).__name__}: {exc}",
            )

    def _execute(self, case: dict[str, Any]) -> dict[str, str]:
        input_data = case["input"]
        items = [
            OrderItem(
                sku=item["sku"],
                quantity=int(item["quantity"]),
                unit_price=money(item["unit_price"]),
            )
            for item in input_data["items"]
        ]

        result = calculate_order_total(
            items=items,
            coupon=input_data.get("coupon"),
            tax_rate=Decimal(str(input_data.get("tax_rate", "0.08"))),
        )

        return {
            "subtotal": str(result.subtotal),
            "discount": str(result.discount),
            "tax": str(result.tax),
            "total": str(result.total),
        }

    @staticmethod
    def _elapsed_ms(start: float) -> float:
        return (time.perf_counter() - start) * 1000
