# `relationalai.std.graphs.Compute.weighted_cosine_similarity()`

```python
relationalai.std.graphs.Compute.weighted_cosine_similarity(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that produces the
[weighted cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) of `node1` and `node2`.
Values range from -1.0 to 1.0, inclusive.
The difference betwen [`cosine_similarity`](./cosine_similarity.md) and `weighted_cosine_similarity`
is that the latter takes into account the weights of the edges between the nodes.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | No |   |
| Undirected | Yes |   |
| Weighted | Yes |   |
| Unweighted | Yes | All edge weights are set to `1.0`.  |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |
| `node2` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |

## Returns

An [`Expression`](../../../Expression.md) object that produces `float` values in the range -1.0 to 1.0, inclusive.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with Person and Friendship types.
model = rai.Model("socialNetwork2")
Person = model.Type("Person")
Friendship = model.Type("Friendship")

# Add some people to the model and connect them with a `friend` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    Friendship.add(person1=alice, person2=bob, weight=1.0)
    Friendship.add(person1=bob, person2=carol, weight=1.0)


# Create a graph and populate edges from Friendship objects.
graph = Graph(model, undirected=True)
with model.rule():
    friendship = Friendship()
    graph.Edge.add(friendship.person1, friendship.person2, weight=friendship.weight)

# Compute the cosine similarity between each pair of distinct people.
with model.query() as select:
    person1, person2 = Person(), Person()
    person1 < person2
    similarity = graph.compute.weighted_cosine_similarity(person1, person2)
    response = select(person1.name, person2.name, alias(similarity, "similarity"))

print(response.results)
# Output:
#     name  name2  similarity
# 0  Carol  Alice         1.0
```

> [!NOTE]
> Pairs of nodes for which the weighted cosine similarity is `0.0` are excluded from results.

## See Also

[`cosine_similarity`](./cosine_similarity.md)
