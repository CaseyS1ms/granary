import pytest


from config import REPRODUCTION_COOLDOWN, RNG, TICKS_PER_YEAR, MAX_WORKING_AGE
from sim.person import Person
from sim.settlement import Settlement


@pytest.fixture
def settlement():
    return Settlement(people=[Person(age=MAX_WORKING_AGE + 1, gender=1, tick=0) for i in range(1)], food=10)

@pytest.fixture
def settlement_test_run():
    s = [Settlement(people=[Person(age=RNG.randint(15,65), gender=RNG.randint(1,2), tick=0) for i in range(100)], food=1000) for _ in range(10)]
    return s

def test_settlement_init(settlement):
    assert settlement.population == 1
    assert settlement.food == 10


def test_settlement_counts_living_people():
    people = [Person(age=20, gender=2, tick=0) for i in range(10)]
    s = Settlement(people=people, food=10000)
    assert s.population == 10


def test_eating_reduces_food(settlement):
    settlement.step()
    assert settlement.food == 9


def test_eating_more_food_than_available():
    s = Settlement(people=[Person(age=MAX_WORKING_AGE, gender=1, tick=0) for i in range(100)], food=100)
    s.step()
    assert (s.food == 0)


def test_some_people_go_hungry_when_food_runs_out():
    s = Settlement(people=[Person(age=MAX_WORKING_AGE + 1, gender=1, tick=0) for i in range(10)], food=6)
    s.step()
    hungry = [p for p in s.people if p.hunger > 0]
    assert len(hungry) == 4


def test_starving_person_loses_health():
    s = Settlement(people=[Person(age=MAX_WORKING_AGE, gender=1, tick=0) for i in range(1)], food=0)
    for i in range(5):
        s.step()
    for p in s.people:
        assert p.health == 90


def test_person_dies_when_health_is_0():
    s = Settlement(people=[Person(age=20, gender=1, tick=0) for i in range(1)], food=0)
    for p in s.people:
        p.health = 0
    s.step()
    assert s.people == []


def test_person_is_removed_from_settlement_when_dead():
    s = Settlement(people=[Person(age=20, gender=1, tick=0) for i in range(1)], food=0)
    for p in s.people:
        p.alive = False
    s.step()
    assert not s.people


def test_reproduction_adds_new_people(monkeypatch):
    monkeypatch.setattr("sim.person.BIRTH_CHANCE", 1.0)
    s = Settlement(people=[Person(age=20, gender=2, tick=0) for i in range(10)], food=10000)
    for i in range(91):
        s.step()
    assert len(s.people) > 10


def test_reproduction_only_happens_once(monkeypatch):
    monkeypatch.setattr("sim.person.BIRTH_CHANCE", 1.0)
    s = Settlement(people=[Person(age=20, gender=2, tick=0) for i in range(1)], food=10000)
    for i in range(5):
        s.step()
    assert len(s.people) == 2


def test_reproduction_happens_on_first_tick(monkeypatch):
    monkeypatch.setattr("sim.person.BIRTH_CHANCE", 1.0)
    s = Settlement(people=[Person(age=20, gender=2, tick=0) for i in range(1)], food=10000)
    s.step()
    assert len(s.people) == 2


def test_reproduction_happens_after_cooldown(monkeypatch):
    monkeypatch.setattr("sim.person.BIRTH_CHANCE", 1.0)
    s = Settlement(people=[Person(age=20, gender=2, tick=0) for i in range(1)], food=10000)
    for i in range(REPRODUCTION_COOLDOWN + 1):
        s.step()
    assert len(s.people) > 2


def test_tick_starts_at_0():
    s = Settlement(people=[Person(20, 2) for i in range(1)], food=10000)
    assert s.tick == 0


def test_tick_increases_by_1_per_step():
    s = Settlement(people=[Person(20, 2) for i in range(1)], food=10000)
    for i in range(10):
        s.step()
    assert s.tick == 10


def test_person_ages_correctly():
    s = Settlement(people=[Person(age=20, gender=1, tick=0) for i in range(1)], food=10000)
    for i in range(365):
        s.step()
    assert s.people[0].get_age_in_years(s.tick) > 20


def test_persons_age_is_assigned_correctly():
    s = Settlement(people=[Person(age=20, gender=1, tick=0) for i in range(1)], food=10000)
    for p in s.people:
        age = p.get_age_in_years(s.tick)
        assert age == 20


def test_person_dies_when_too_old():
    s = Settlement(people=[Person(age=20, gender=1, tick=0) for i in range(1)], food=1000000000000)
    for i in range(365 * 100):
        s.step()
    assert s.people == []


def test_settlement_produces_food():
    s = Settlement(people=[Person(age=25, gender=1) for i in range(1)], food=0)
    for i in range(1):
        s.step()
        assert s.food > 0


def test_settlement_doesnt_produce_food_when_hungry():
    s = Settlement(people=[Person(age=20, gender=1) for _ in range(1)], food=0)
    s.people[0].hunger = 100
    for i in range(10):
        s.step()
        assert s.food == 0


def test_person_starts_with_no_job():
    s = Settlement(people=[Person(age=20, gender=1) for _ in range(1)], food=0)
    assert s.people[0].job is None


def test_person_gets_job_when_old_enough():
    s = Settlement(people=[Person(age=18, gender=1) for _ in range(1)], food=0)
    s.step()
    assert s.people[0].job is not None


def test_person_does_not_get_job_when_too_young():
    s = Settlement(people=[Person(age=14, gender=1) for _ in range(1)], food=0)
    s.step()
    assert s.people[0].job is None


def test_person_does_not_get_job_when_too_old():
    s = Settlement(people=[Person(age=MAX_WORKING_AGE + 1, gender=1) for _ in range(1)], food=0)
    s.step()
    assert s.people[0].job is None







