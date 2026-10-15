import pytest

from config import REPRODUCTION_COOLDOWN
from sim.person import Person
from sim.settlement import Settlement

@pytest.fixture
def settlement():
    return Settlement(people = [Person(age = 66, gender =  2, tick = 0) for i in range(10)], food = 10000)


def test_settlement_init(settlement):
    assert settlement.population == 10
    assert settlement.food == 10000

def test_settlement_counts_living_people():
    people = [Person(age = 20, gender = 2, tick = 0) for i in range(10)]
    s = Settlement(people = people, food = 10000)
    assert s.population == 10

def test_eating_reduces_food(settlement):
    settlement.step()
    assert settlement.food == 9990

def test_eating_more_food_than_available():
    s = Settlement(people = [Person(age = 66,gender =  2, tick = 0) for i in range(100)], food = 100)
    s.step()
    assert (s.food == 0)

def test_some_people_go_hungry_when_food_runs_out():
    s = Settlement(people = [Person(age = 66, gender = 2, tick = 0) for i in range(10)], food = 6)
    s.step()
    hungry = [p for p in s.people if p.hunger > 0]
    assert len(hungry) == 4

def test_starving_person_loses_health():
    s = Settlement(people = [Person(age = 66, gender = 1, tick = 0) for i in range(1)], food = 0)
    for i in range(6):
        s.step()
    for p in s.people:
        assert p.health == 90


def test_person_dies_when_health_is_0():
    s = Settlement(people = [Person(age = 20, gender = 2, tick = 0) for i in range(1)], food = 0)
    for i in range(100):
        s.step()
    assert s.people == []

def test_person_is_removed_from_settlement_when_dead():
    s = Settlement(people = [Person(age =20, gender = 2, tick = 0) for i in range(1)], food = 0)
    for i in range(100):
        s.step()
    assert not s.people


def test_reproduction_adds_new_people():
    s = Settlement(people = [Person(age = 20,gender = 2, tick = 0) for i in range(10)], food = 10000)
    for i in range(91):
        s.step()
    assert len(s.people) > 10

def test_reproduction_only_happens_once():
    s = Settlement(people = [Person(age = 20, gender = 2, tick = 0) for i in range(1)], food = 10000)
    for i in range(5):
        s.step()
    assert len(s.people) == 2

def test_reproduction_happens_on_first_tick():
    s = Settlement(people = [Person(age = 20, gender = 2, tick = 0) for i in range(1)], food = 10000)
    s.step()
    assert len(s.people) == 2

def test_reproduction_happens_after_cooldown():
    s = Settlement(people = [Person(age = 20, gender = 2, tick = 0) for i in range(1)], food = 10000)
    for i in range(REPRODUCTION_COOLDOWN + 1):
        s.step()
    assert len(s.people) > 2



def test_tick_starts_at_0():
    s = Settlement(people = [Person(20, 2) for i in range(1)], food = 10000)
    assert s.tick == 0

def test_tick_increases_by_1_per_step():
    s = Settlement(people = [Person(20, 2) for i in range(1)], food = 10000)
    for i in range(10):
        s.step()
    assert s.tick == 10

def test_person_ages_correctly():
    s = Settlement(people = [Person(age = 20, gender = 1, tick = 0) for i in range(1)], food = 10000)
    for i in range(365):
        s.step()
    assert s.people[0].get_age_in_years(s.tick) > 20


def test_settlement_produces_food():
    s = Settlement(people = [Person(age = 20, gender = 1) for i in range(1)], food = 0)
    for i in range(1):
        s.step()
        assert s.food > 0

def test_settlement_produces_food_when_hungry():
    s = Settlement(people = [Person(age = 20, gender = 1) for _ in range(1)], food = 0)
    s.people[0].hunger = 100
    for i in range(10):
        s.step()
        assert s.food == 0


def test_person_starts_with_no_job():
    s = Settlement(people = [Person(age = 20, gender = 1) for _ in range(1)], food = 0)
    assert s.people[0].job is None

def test_person_gets_job_when_old_enough():
    s = Settlement(people = [Person(age = 18, gender = 1) for _ in range(1)], food = 0)
    s.step()
    assert s.people[0].job is not None

def test_person_does_not_get_job_when_too_young():
    s = Settlement(people = [Person(age = 14, gender = 1) for _ in range(1)], food = 0)
    s.step()
    assert s.people[0].job is None

def test_person_does_not_get_job_when_too_old():
    s = Settlement(people = [Person(age = 66, gender = 1) for _ in range(1)], food = 0)
    s.step()
    assert s.people[0].job is None


