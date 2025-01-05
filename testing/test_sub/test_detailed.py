import pytest

def test_fail42():
    assert 1 == 2

class TestClass:
    def test_success(self) -> None:
        assert True

    def test_fail(self) -> None:
        assert False
