import math
import random

from . import family

from .word.name.female import female_names
from .word.name.male import male_names
from .word.adjective.whimsical import whimsical_adjectives
from .word.adjective.standard import adjectives
from .word.animal import animals
from .word.family import male_family, female_family
from .word.cognomen import cognomens
from .word.race import races
from .word.title import titles as titles_library

MAX_AGE = 99
MALE = "male"
FEMALE = "female"

ADULT_AGE = 20


class Person():
    def __init__(
        self,
        race=None,
        leader=False,
        max_age=MAX_AGE,
    ):

        if random.random() > 0.5:
            self.sex = MALE
        else:
            self.sex = FEMALE

        self.leader = leader
        self.character = random.choice(adjectives)
        self.past = random.choice(adjectives)
        self.leader_relation = None
        self.position = None
        self.events = []
        (
            self.pre_nickname,
            self.firstname,
            self.post_nickname,
        ) = self._generate_name()

        if race is None:
            self.race = random.choice(races)
        else:
            self.race = race

        if self.leader is True:
            self.age = ADULT_AGE + math.floor(
                random.random() * (max_age - ADULT_AGE)
            )
        else:
            self.age = math.floor(random.random() * max_age)

    def get_first_name(self):
        name = self.firstname
        if self.pre_nickname is not None:
            name = "\"" + self.pre_nickname + "\" " + name
        if self.post_nickname is not None:
            name = name + " \"" + self.post_nickname + "\""
        return name

    def get_full_name(self):
        name = self.firstname
        if self.pre_nickname is not None:
            name = "\"" + self.pre_nickname + "\" " + name
        if self.post_nickname is not None:
            name = name + " \"" + self.post_nickname + "\""
        return name

    def _generate_name(self):
        if self.sex == MALE:
            firstname = random.choice(male_names)
        else:
            firstname = random.choice(female_names)

        post_nickname = None
        pre_nickname = None

        r = random.random() * 30

        if r < 15 and self.leader is True:
            post_nickname = "{}".format(random.choice(cognomens))
        elif r < 1:
            post_nickname = "the {}".format(
                random.choice(adjectives).capitalize()
            )
        elif r < 2:
            pre_nickname = random.choice(adjectives).capitalize()
        elif r < 3:
            post_nickname = "the {}".format(
                random.choice(whimsical_adjectives).capitalize()
            )
        elif r < 4:
            pre_nickname = random.choice(animals).capitalize()
        elif r < 5:
            post_nickname = "the {}".format(
                random.choice(animals)
            )

        return pre_nickname, firstname, post_nickname


class Noble(Person):
    def __init__(
        self,
        family_name,
        rank,
        race=None,
        leader=False,
        max_age=MAX_AGE,
        titles=None
    ):
        super().__init__(race=race, leader=leader, max_age=max_age)

        self.rank = rank
        self.family_name = family_name

        if leader is False:
            self.leader_relation = self._generate_relation()
        else:
            self.leader_relation = None

        if titles is None:
            titles = titles_library[0]
        self.title = self._get_title(titles)

    def get_full_name(self):
        name = self.firstname
        if self.pre_nickname is not None:
            name = "\"" + self.pre_nickname + "\" " + name
        if self.post_nickname is not None:
            name = name + " \"" + self.post_nickname + "\""
        name = name + " " + self.family_name
        return name

    def set_spouse(self, leader, titles):
        if random.random() * 100 > 10:
            if leader.sex == MALE:
                self.leader_relation = "wife"
                self.sex = FEMALE
                self.firstname = random.choice(female_names)
            else:
                self.leader_relation = "husband"
                self.sex = MALE
                self.firstname = random.choice(male_names)
        else:
            if leader.sex == MALE:
                self.leader_relation = "husband"
                self.sex = MALE
                self.firstname = random.choice(male_names)
            else:
                self.leader_relation = "wife"
                self.sex = FEMALE
                self.firstname = random.choice(female_names)

        if self.age < ADULT_AGE:
            self.age = ADULT_AGE

        self.title = self._get_title(titles)

    def get_full_title(self):
        return self.title + " " + self.get_first_name()

    def get_full_title_link(self):
        s = self.get_first_name()

        if self.title is not None:
            s = "{} {}".format(self.title, s)

        if self.affiliation is not None:
            s = "{} of the {}".format(s, self.affiliation.get_full_name_link())

        return s

    def _generate_relation(self):
        if self.sex == MALE:
            leader_relation = random.choice(male_family)
        else:
            leader_relation = random.choice(female_family)

        return leader_relation

    def _get_title(self, titles):
        if self.rank == family.ROYAL_FAMILY:
            if self.sex == MALE:
                if self.leader is True:
                    title = titles["monarch"]
                else:
                    title = titles["heir"]
            else:
                if self.leader is True:
                    title = titles["monarchess"]
                else:
                    title = titles["heiress"]
        elif (self.rank == family.GREAT_FAMILY or
                self.rank == family.MINOR_FAMILY):
            if self.sex == MALE:
                title = titles["lord"]
            else:
                title = titles["lordess"]
        elif self.rank == family.PETTY_FAMILY:
            if self.sex == MALE:
                title = titles["knight"]
            else:
                title = titles["knightess"]

        return title
