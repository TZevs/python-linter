from linter import lint


def test_flags_mutable_default():
    assert lint("def f(x, items=[]):\n    pass\n") == [(1, "GL001 mutable default argument")]


def test_ignores_none_default():
    assert lint("def f(x, items=None):\n    pass\n") == []


def test_flags_is_with_number():
    assert lint("x = 1\nif x is 5:\n    pass\n") == [(2, "GL002 'is' used with a literal")]


def test_ignores_is_none():
    assert lint("x = 1\ny = x is None\n") == []


def test_flags_builtin_name():
    assert lint("list = [1, 2]\n") == [(1, "GL003 built-in name 'list' overwritten")]


def test_ignores_normal_name():
    assert lint("my_list = []\n") == []


def test_attribute_assignment_does_not_crash():
    assert lint("class A:\n    def __init__(self):\n        self.x = 1\n") == []
