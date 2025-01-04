import pytest

def test_fail():
    assert 1 == 2

@pytest.fixture
def fix():
    raise Exception('oops')

def test_error(fix):
    assert fix == 2

def test_success():
    assert True
    

@pytest.mark.skip(reason="Skipping this FUNCTION level test - Simple Interest")
def test_simple_interest_calculator_function() -> None:
    value = simple_interest(8, 6, 8)
    assert value == 3.84

@pytest.mark.skip(reason="Skipping this CLASS level test")
class TestInterestCalculator:
    def test_simple_interest_calculator_class(self) -> None:
        value = simple_interest(8, 6, 8)
        assert value == 3.84

    def test_compound_interest_calculator_class(self) -> None:
        value = compound_interest(10000, 2, 5)
        assert value == 110250000.0

@pytest.mark.xfail(reason="Missing Arguments")  
def test_simple_interest_calculator_xfail_missing_arg() -> None:  
    value = simple_interest(8)  # Missing Argument - FAIL  
    assert value == 3.84  
