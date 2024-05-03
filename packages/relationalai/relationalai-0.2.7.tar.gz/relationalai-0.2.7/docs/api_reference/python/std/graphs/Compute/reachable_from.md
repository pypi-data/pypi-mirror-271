# `relationalai.std.graphs.Compute.reachable_from()`

```python
relationalai.std.graphs.Compute.reachable_from(node: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that produces object IDs of all nodes reachable from `node` in the transitive closure of the graph.
Self-loops are only included in the transitive closure if they exist in the graph.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :---------- |
| node | [`Producer`](../../Producer.md) | The node from which to compute the transitive closure. |

## Returns

An [`Expression`](../../../Expression.md) object that produces object IDs of all nodes reachable from `node`.

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

# Who is "reachable" from Alice, following a chain of `follows` edges?
with model.query() as select:
    alice = Person(name="Alice")
    reachable_from_alice = graph.compute.reachable_from(node=alice)
    response = select(reachable_from_alice.name)

print(response.results)
# Output:
#     name
# 0    Bob
# 1  Carol
```

Alice is not reported as reachable from herself because there is no edge from Alice to herself in the graph.
