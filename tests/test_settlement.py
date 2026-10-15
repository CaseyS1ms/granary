import pytest

from sim.settlement import Settlement

@pytest.fixture
def settlement():
    return Settlement(population = 100, food = 10000)


def test_settlement_init(settlement):
    assert settlement.population == 100
    assert settlement.food == 10000

def test_eating_reduces_food(settlement):
    settlement.tick()
    assert settlement.food == 9900

def test_eating_more_food_than_available(settlement):
    s = Settlement(population = 100, food = 100)
    s.eat(10000)
    assert (s.food == 0)