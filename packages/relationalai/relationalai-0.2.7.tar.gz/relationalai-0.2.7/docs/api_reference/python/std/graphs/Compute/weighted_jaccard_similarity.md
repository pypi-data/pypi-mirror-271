# `relationalai.std.graphs.Compute.weighted_jaccard_similarity()`

```python
relationalai.std.graphs.Compute.weighted_jaccard_similarity(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that produces the
[weighted Jaccard similarity](https://en.wikipedia.org/wiki/Jaccard_index) of `node1` and `node2`.
Values range from 0.0 to 1.0, inclusive.
The difference betwen [`jaccard_similarity`](./jaccard_similarity.md) and `weighted_jaccard_similarity`
is that the latter takes into account the weights of the edges between the nodes.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes |   |
| Unweighted | Yes | All edge weights are set to `1.0`.  |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |
| `node2` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |

## Returns

An [`Expression`](../../../Expression.md) object that produces `float` values in the range 0.0 to 1.0, inclusive.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "transactions" with Person and Transaction types.
model = rai.Model("socialNetwork2")
Person = model.Type("Person")
Transaction = model.Type("Transaction")

# Add some people and transactions to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    Transaction.add(sender=alice, receiver=carol, amount=25.0)
    Transaction.add(sender=alice, receiver=bob, amount=50.0)
    Transaction.add(sender=bob, receiver=carol, amount=100.0)

# Create a directed graph and populate edges from Transaction objects.
graph = Graph(model, weighted=True)
with model.rule():
    transaction = Transaction()
    graph.Edge.add(transaction.sender, transaction.receiver, weight=transaction.amount)

# Compute the weighted Jaccard similarity between each pair of distinct people.
with model.query() as select:
    person1, person2 = Person(), Person()
    person1 < person2
    similarity = graph.compute.weighted_jaccard_similarity(person1, person2)
    response = select(person1.name, person2.name, alias(similarity, "similarity"))

print(response.results)
# Output:
#     name  name2  similarity
# 0  Alice    Bob    0.166667
# 1  Carol  Alice    0.000000
# 2  Carol    Bob    0.000000
```

## See Also

[`jaccard_similarity()`](./jaccard_similarity.md)
