# just an example on how to use the Tree class

from collections import defaultdict
from .tree import Tree, Count

class Person(Tree):
    def __init__(self, name:str="nn.", children: defaultdict[str, list[Tree]] | None = None):
        super().__init__(children)
        self.name = name
    
class Family(Person):...
    
class GrandMother(Person):...

class Mother(Person):...
 
class Child(Person):...

class FamilyCount(Count):
    def _do_count_Family(self, tree:Family):
        return 0
    
c1 = Child(name="Alice")
c2 = Child(name="Bob")
c3 = Child(name="Cherryl")
c4 = Child(name="Dick")
c5 = Child(name="Ellen")
c6 = Child(name="Fergal")
c7 = Child(name="Gladys")
c8 = Child(name="Hank")

m1 = Mother(name="Anna", children={"girls":[c1,c3], "boys":[c2,c4]})
m2 = Mother(name="Beatrice", children={"girls":[c5,c7], "boys":[c6,c8]})

g1 = GrandMother(name="Granny", children={"children": [m1, m2]})

f1 = Family(name="The Andersons",children={"matriarch":[g1]})

counter = FamilyCount(f1, strict=False)

print(counter.count())

