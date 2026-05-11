from decimal import Decimal


class AssertionFailure(Exception):
    pass


def assert_mapping_matches(actual: dict, expected: dict) -> None:
    for key, expected_value in expected.items():
        if key not in actual:
            raise AssertionFailure(f"missing key: {key}")

        actual_value = actual[key]
        normalized_expected = _normalize(expected_value)
        normalized_actual = _normalize(actual_value)

        if normalized_actual != normalized_expected:
            raise AssertionFailure(
                f"{key}: expected {normalized_expected!r}, got {normalized_actual!r}"
            )


def _normalize(value):
    if isinstance(value, Decimal):
        return str(value)
    return value
