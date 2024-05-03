# `relationalai.std.graphs.Compute.diameter_range()`

```python
relationalai.std.graphs.Compute.diameter_range() -> tuple[Expression]
```

Returns a tuple of two [`Expression`](../../../Expression.md) objects that estimates the diameter of the graph by producing a minimum bound and a maximum bound.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Weights are ignored.   |

## Parameters

No parameters are needed.

## Returns

Returns an tuple of two [Expression](docs/api_reference/python/Expression.md) objects that produce `int` values.

## Example
```python
import relationalai as rai
from relationalai.std.graphs import Graph
from relationalai.std import alias

# Create a model named "techProfessionalsNetwork" with a Person type.
model = rai.Model("techProfessionalsNetwork")
Person = model.Type("Person")

# Add tech professionals to the model and connect them based on professional relationships.
with model.rule():
    # Adding tech professionals
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    dave = Person.add(name="Dave")
    eve = Person.add(name="Eve")
    frank = Person.add(name="Frank")

    # Creating professional relationships
    alice.set(relationship=bob)
    bob.set(relationship=carol).set(relationship=dave)
    carol.set(relationship=dave).set(relationship=alice)
    dave.set(relationship=eve).set(relationship=frank)
    eve.set(relationship=frank)

# Create a graph and add all `Person` objects to the set of nodes
# and the `Person.relationship` property to the set of edges.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.relationship)

# Compute the range of possible diameters in the tech professionals network graph.
with model.query() as select:
    diam_min, diam_max = graph.compute.diameter_range()
    response = select(alias(diam_min, "min"), alias(diam_max, "max"))

print(response.results)
# Output: 
#    min  max
# 0    3    4
```
