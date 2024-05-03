# `relationalai.std.graphs.Compute.num_triangles()`

```python
relationalai.std.graphs.Compute.num_triangles(node: Producer | None = None) -> Expression
```

Returns an [Expression](docs/api_reference/python/Expression.md) object that produces the number of unique triangles in the graph.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node` | [`Producer`](docs/api_reference/python/Producer.md) | Optional node for which to compute the number of unique triangles. If `None`, the number of unique triangles in the whole graph is computed. |

## Returns

Returns an [Expression](docs/api_reference/python/Expression.md) object that producers `int` values.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to and 
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    charlie = Person.add(name="Charlie")
    diana = Person.add(name="Diana")
    alice.set(follows=bob)
    bob.set(follows=charlie)
    charlie.set(follows=alice).set(follows=diana)
    
# Create a directed graph with edges from the Person.follows property
graph = Graph(model)
graph.Edge.extend(Person.follows)

# Compute the number of unique triangles in the graph.
with model.query() as select:
    num_triangles = graph.compute.num_triangles()
    response = select(alias(num_triangles, "num_triangles"))
    
print(response.results)
# Output:
#    num_triangles
# 0              1

# Compute the number of unique triangles that each node is part of.
with model.query() as select:
    person = Person()
    num_triangles = graph.compute.num_triangles(person)
    response = select(person.name, alias(num_triangles, "num_triangles"))

print(response.results)
# Output:
#       name  num_triangles
# 0    Alice              1
# 1      Bob              1
# 2  Charlie              1
# 3    Diana              0
```

## See Also

[`is_triangle()`](./is_triangle.md) and [`triangles`](./triangles.md).