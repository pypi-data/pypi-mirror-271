# `relationalai.std.graphs.Compute.is_triangle()`

```python
relationalai.std.graphs.Compute.is_triangle(node1: Producer, node2: Producer, node3: Producer) -> Expression
```

Returns an [Expression](docs/api_reference/python/Expression.md) object that produces `bool` values indicating whether `node1`, `node2`, and `node3` form a triangle in the graph.

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
| `node1` | [`Producer`](docs/api_reference/python/Producer.md) | The first node in the triangle. |
| `node2` | [`Producer`](docs/api_reference/python/Producer.md) | The second node in the triangle. |
| `node3` | [`Producer`](docs/api_reference/python/Producer.md) | The third node in the triangle. |

## Returns

Returns an [Expression](docs/api_reference/python/Expression.md) object that produces `bool` values.

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

# Do Alice, Bob, and Charlie form a triangle?
with model.query() as select:
    is_triangle = graph.compute.is_triangle(
        Person(name="Alice"), Person(name="Bob"), Person(name="Charlie")
    )
    response = select(is_triangle)
    
print(response.results)
# Output:
#       v
# 0  True

# Do Alice, Bob, and Diana form a triangle?
with model.query() as select:
    is_triangle = graph.compute.is_triangle(
        Person(name="Alice"), Person(name="Bob"), Person(name="Diana")
    )
    response = select(is_triangle)

print(response.results)
# Output:
#        v
# 0  False
```

## See Also

[`num_triangles()`](./num_triangles.md) and [`triangles`](./triangles.md).
