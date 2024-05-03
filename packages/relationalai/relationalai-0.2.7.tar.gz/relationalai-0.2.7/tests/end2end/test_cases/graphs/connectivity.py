import relationalai as rai
from relationalai import std


model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    Relationship.add(from_=obj1, to=obj2)

disconnected_graph = std.graphs.Graph(model)
disconnected_graph.Node.extend(Object)

connected_graph = std.graphs.Graph(model)
with model.rule():
    r = Relationship()
    connected_graph.Edge.add(r.from_, r.to)

# Check that is_connected works
with model.query() as select:
    select(
        connected_graph.compute.is_connected(),
        disconnected_graph.compute.is_connected()
    )

# Check that reachable_from works
with model.query() as select:
    n = Object()
    reachable_from_n = connected_graph.compute.reachable_from(n)
    select(n, reachable_from_n)

# Check that is_reachable works
with model.query() as select:
    n1 = Object(id=1)
    n2 = Object(id=2)
    is_reachable1 = connected_graph.compute.is_reachable(n1, n2)
    is_reachable2 = connected_graph.compute.is_reachable(n2, n1)
    select(is_reachable1, is_reachable2)
