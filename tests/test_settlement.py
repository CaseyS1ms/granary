import pytest

from sim.person import Person
from sim.settlement import Settlement

@pytest.fixture
def settlement():
    return Settlement(people = [Person(20) for i in range(10)], food = 10000)


def test_settlement_init(settlement):
    assert settlement.population == 10
    assert settlement.food == 10000

def test_settlement_counts_living_people(settlement):
    people = [Person(20) for i in range(10)]
    s = Settlement(people = people, food = 10000)
    assert s.population == 10

def test_eating_reduces_food(settlement):
    settlement.tick()
    assert settlement.food == 9990

def test_eating_more_food_than_available(settlement):
    s = Settlement(people = [Person(20) for i in range(100)], food = 100)
    s.eat(10000)
    assert (s.food == 0)

def test_some_people_go_hungry_when_food_runs_out(settlement):
    s = Settlement(people = [Person(20) for i in range(10)], food = 6)
    s.tick()
    hungry = [p for p in s.people if p.hunger > 0]
    assert len(hungry) == 4

def test_starving_person_loses_health(settlement):
    s = Settlement(people = [Person(20) for i in range(1)], food = 0)
    for i in range(6):
        s.tick()
    for p in s.people:
        assert p.health == 90

def test_person_dies_when_health_is_0(settlement):
    s = Settlement(people = [Person(20) for i in range(1)], food = 0)
    for i in range(100):
        s.tick()
    assert s.people[0].alive == False
