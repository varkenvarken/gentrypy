# just an example on how to use the Tree class

from collections import defaultdict
from gentry.tree import Tree, Count
from gentry.html import HTMLLayout


class Family(Tree, HTMLLayout): ...


class Person(Tree, HTMLLayout):
    _groups = {"children"}


class GrandMother(Person): ...

class Mother(Person):
    _groups = {"girls", "boys"}


class Child(Person):
    _include_properties = True


# define a few children
c1 = Child("Alice")
c2 = Child("Bob")
c3 = Child("Cherryl", properties={"chess master": "ELO 2235"})
c4 = Child("Dick")
c5 = Child("Ellen")
c6 = Child("Fergal")
c7 = Child("Gladys", properties={"drivers license": 2023, "nose piercing": 2024})
c8 = Child("Hank")
c9 = Child("Iris")
c10 = Child("Janice")

# Mothers have girls and boys attributes defined, so those can be assigned directly
m1 = Mother("Anna")
m1.girls = [c1, c3]
m1.boys = [c2, c4]

m2 = Mother("Beatrice")
m2.girls.append(
    c5
)  # under the hood they are all items in a defaultdict(list) so we can append directly
m2.girls.append(c7)
m2.boys = [c6, c8]

m3 = Mother("Carla")
m3.girls += [c9, c10]

# Grandmothers do not make the distinction
g1 = GrandMother("Granny")
g1.children = [m1, m2, m3]

# Family does not have any direct access attributes defined, but anything
# that is passed as the children argument (and can be converted to a defaultdict(list))
# will be added to the _children attribute, so will still be automatically discovered
# by Visitor derived classes.
f1 = Family("The Andersons", children={"matriarch": [g1]})


print(f1)
