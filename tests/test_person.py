import pytest

from sim.person import Person



def test_person_init():
    p = Person(20)
    assert p.alive == True
    assert p.age == 20

def test_person_starts_full():
    p = Person(20)
    assert p.hunger == 0

def test_person_starts_full_health():
    p = Person(20)
    assert p.health == 100