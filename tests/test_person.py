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


def test_persons_health_is_reduced_by_damage():
    p = Person(20)
    p.take_damage(10)
    assert p.health == 90

def test_persons_dies_at_health_0():
    p = Person(20)
    p.take_damage(100)
    assert p.alive == False

def test_persons_health_does_not_go_below_0():
    p = Person(20)
    p.take_damage(1000)
    assert p.health == 0

def test_persons_hunger_is_reduced():
    p = Person(20)
    p.increase_hunger()
    assert p.hunger == 20


def test_persons_hunger_does_not_go_over_100():
    p = Person(20)
    for i in range(6):
        p.increase_hunger()
    assert p.hunger == 100