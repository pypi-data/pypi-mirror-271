# `relationalai.std.graphs.Compute.is_connected()`

```python
relationalai.std.graphs.Compute.is_connected() -> Expression
```

Returns an [`Expression`](../../../Expression.md) that produces `True` if the graph is connected
and `False` otherwise.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes |   |

## Parameters

None.

## Returns

An [`Expression`](../../../Expression.md) object that produces `bool` values.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    alice.set(follows=bob)

# Create a graph and add nodes and edges from the `follows` property.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Is the graph conected? No, because Edgar is not connected to anyone else.
with model.query() as select:
    connected = graph.compute.is_connected()
    response = select(alias(connected, "connected"))

print(response.results)
# Output:
#    connected
# 0      False
```
