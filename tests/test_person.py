import pytest

from config import REPRODUCTION_COOLDOWN
from sim.person import Person



def test_person_init():
    p = Person(20, 2)
    assert p.alive == True
    assert p.age == 20

def test_person_starts_full():
    p = Person(20, 2)
    assert p.hunger == 0

def test_person_starts_full_health():
    p = Person(20, 2)
    assert p.health == 100


def test_persons_health_is_reduced_by_damage():
    p = Person(20, 2)
    p.take_damage(10)
    assert p.health == 90

def test_persons_dies_at_health_0():
    p = Person(20,2)
    p.take_damage(100)
    assert p.alive == False

def test_persons_health_does_not_go_below_0():
    p = Person(20, 2)
    p.take_damage(1000)
    assert p.health == 0

def test_persons_hunger_is_reduced():
    p = Person(20, 2)
    p.increase_hunger()
    assert p.hunger == 20


def test_persons_hunger_does_not_go_over_100():
    p = Person(20, 2)
    for i in range(6):
        p.increase_hunger()
    assert p.hunger == 100


def test_persons_hunger_is_reset_when_fed():
    p = Person(20, 2)
    p.increase_hunger()
    p.eat()
    assert p.hunger == 0


def test_person_can_reproduce_from_start():
    p = Person(age = 20, gender = 2)
    assert p.can_reproduce(tick = 0) == True


def test_reproduction_is_correctly_triggered():
    p = Person(age = 20, gender =  2)
    assert p.can_reproduce(tick = 90) == True

def test_reproduction_is_incorrectly_triggered_gender_mismatch():
    p = Person(age = 20, gender = 1)
    assert p.can_reproduce(tick = 90) == False

def test_reproduction_is_incorrectly_triggered_age_mismatch():
    p = Person(age = 17, gender = 2)
    assert p.can_reproduce(tick = 90) == False

def test_reproduction_cant_be_triggered_twice():
    p = Person(age = 20, gender = 2)
    p.can_reproduce(tick = 0)
    assert p.can_reproduce(tick = REPRODUCTION_COOLDOWN - 1) == False

def test_reproduction_is_correctly_triggered_after_cooldown():
    p = Person(age = 20, gender = 2)
    p.can_reproduce(tick = 0)
    assert p.can_reproduce(tick = REPRODUCTION_COOLDOWN + 1) == True


