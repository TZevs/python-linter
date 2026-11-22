import pytest
from linter import lint

# Tests cases the linter should flag
@pytest.mark.parametrize(
    "source",
    [
        "if x is 5: pass",
        "if x is not 5: pass",
        "if x is 'hello': pass",
        "if x is not 'hello': pass",
        "if x is 5.5: pass",
    ],
)
def test_flags_identity_comparison_with_literal(source):
    findings = lint(source)

    assert len(findings) == 1
    assert findings[0][1].startswith("GL002")

# Test cases the linter shouldn't flag
@pytest.mark.parametrize(
    "source",
    [
        "if x == 5: pass",
        "if x != 5: pass",
        "if x is None: pass",
        "if x is not None: pass",
        "if x is y: pass",
    ],
)
def test_ignores_valid_identity_comparisons(source):
    assert lint(source) == []


def test_chained_comparison_does_not_flag_wrong_comparator():
    source = "if x is y < 5: pass"

    assert lint(source) == []


def test_chained_comparison_flags_literal():
    source = "if x is 5 < y: pass"

    findings = lint(source)

    assert len(findings) == 1
    assert findings[0][1].startswith("GL002")


def test_multiple_is_comparisons():
    source = "if x is 5 is 6: pass"

    findings = lint(source)

    assert len(findings) == 2