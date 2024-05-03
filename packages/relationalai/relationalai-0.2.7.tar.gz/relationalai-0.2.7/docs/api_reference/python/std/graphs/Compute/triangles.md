# `relationalai.std.graphs.Compute.triangles()`

```python
relationalai.std.graphs.Compute.triangles(node: Producer | None = None) -> tuple[Expression]
```

Returns a tiple of [Expression](docs/api_reference/python/Expression.md) objects that produce
all nodes that form unique triangles in the graph.
If the optional `node` parameter is provided, the all unique triangles that include the node are produced.

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
| `node` | [`Producer`](docs/api_reference/python/Producer.md) | Optional node for which to compute the unique triangles. If `None`, all unique triangles in the graph are computed. |

## Returns

Returns a tuple of three [Expression](docs/api_reference/python/Expression.md) objects.

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
    diana.set(follows=bob)
    
# Create a directed graph with edges from the Person.follows property
graph = Graph(model)
graph.Edge.extend(Person.follows)

# Compute the unique triangles in the graph.
with model.query() as select:
    person1, person2, person3 = graph.compute.triangles()
    response = select(person1.name, person2.name, person3.name)
    
print(response.results)
# Output:
#       name  name2 name3
# 0  Charlie  Alice   Bob
# 1  Charlie  Diana   Bob

# Compute the unique triangles that include Alice.
with model.query() as select:
    alice = Person(name="Alice")
    person1, person2, person3 = graph.compute.triangles(alice)
    response = select(person1.name, person2.name, person3.name)

print(response.results)
# Output:
#       name  name2 name3
# 0  Charlie  Alice   Bob
```

## See Also

[`is_triangle()`](./is_triangle.md) and [`num_triangles`](./num_triangles.md).
