# `relationalai.std.graphs.Compute.is_reachable()`

```python
relationalai.std.graphs.Compute.is_reachable(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that produces `True` if `node2` is reachable from `node1` in graph, and `False` otherwise.
A node is reachable from itself only if there is a self-loop in the graph.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :---------- |
| node1 | [`Producer`](../../Producer.md) | The node from which to check if `node2` is reachable. |
| node2 | [`Producer`](../../Producer.md) | The node to check if it is reachable from `node1`. | 

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
    bob.set(follows=carol)

# Create a graph and add nodes and edges from the `follows` property.
graph = Graph(model)
graph.Edge.extend(Person.follows)

# Is Alice reachable from Carol?
with model.query() as select:
    is_reachable = graph.compute.is_reachable(Person(name="Carol"), Person(name="Alice"))
    response = select(is_reachable)

print(response.results)
# Output:
#        v
# 0  False
```

Alice is not reported as reachable from herself because there is no edge from Alice to herself in the graph.
