import pytest
from linter import lint

# Test cases the linter should flag
@pytest.mark.parametrize(
    "source",
    [
        "list = []",
        "str = 'hello'",
        "dict = {}",
        "int = 10",
    ],
)
def test_flags_assignment_to_builtin(source):
    findings = lint(source)

    assert len(findings) == 1
    assert findings[0][1].startswith("GL003")

# Test cases the linter shouldn't flag
@pytest.mark.parametrize(
    "source",
    [
        "my_list = []",
        "items = {}",
        "number = 10",
        "custom_name = 'hello'",
    ],
)
def test_ignores_assignment_to_normal_names(source):
    assert lint(source) == []


def test_flags_annotated_assignment():
    source = "list: list = []"

    assert len(lint(source)) == 1


def test_flags_augmented_assignment():
    source = "list += []"

    assert len(lint(source)) == 1


def test_flags_destructuring_assignment():
    source = "list, number = [], 5"

    findings = lint(source)

    assert len(findings) == 1
    assert findings[0][1].startswith("GL003")


def test_flags_builtin_assignment_inside_function():
    source = """
def f():
    list = []
"""

    assert len(lint(source)) == 1