import pytest
from linter import lint


@pytest.mark.parametrize(
    "source",
    [
        "def f(items=[]): pass",
        "def f(items={}): pass",
        "def f(items=()): pass",
        "def f(items={1, 2}): pass",
        "def f(items=[1, 3]): pass",
    ]
)
def test_flags_mutable_default_args(source):
    findings = lint(source)

    assert len(findings) == 1
    assert findings[0][1].startswith("GL001")


@pytest.mark.parametrize(
    "source",
    [
        "def f(value=10): pass",
        "def f(value='hello'): pass",
        "def f(value=None): pass",
        "def f(value=True): pass",
    ]
)
def test_ignores_immutable_defaults(source):
    assert lint(source) == []


def test_flags_keyword_only_mutable_defaults():
    source = "def f(*, items=[]): pass"

    assert len(lint(source)) == 1


def test_flags_async_function_mutable_default():
    source = "async def f(items=[]): pass"

    assert len(lint(source)) == 1


def test_does_not_flag_mutable_object_indside_func_body():
    source = """
def f():
    items = []
"""

    assert lint(source) == []