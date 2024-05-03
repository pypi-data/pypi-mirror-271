# `relationalai.std.graphs.Compute.weighted_distance()`

```python
relationalai.std.graphs.Compute.weighted_distance(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that computes the weighted distance between `node1` and `node2`.
`weighted_distance` is the counterpart of [`distance`](./distance.md) that uses edge weights for computing the shortest path length between nodes.
All edge weights must be non-negative, otherwise no results are returned.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes | Edge weights default to `1.0` |
| Directed | Yes | Edge weights default to `1.0` |
| Weighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |
| `node2` | [`Producer`](../../../Producer/README.md) | A producer that produces object IDs of nodes. |

## Returns

An [`Expression`](../../../Expression.md) object that produces `int` values.

## Example
```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model named "weightedTransportationNetwork" with City and Road types.
model = rai.Model("weightedTransportationNetwork")
City = model.Type("City")
Road = model.Type("Road")

# Add cities and roads to the model.
with model.rule():
    new_york = City.add(name="New York")
    los_angeles = City.add(name="Los Angeles")
    chicago = City.add(name="Chicago")
    houston = City.add(name="Houston")
    Road.add(from_=new_york, to=los_angeles, distance=2500)
    Road.add(from_=new_york, to=chicago, distance=800)
    Road.add(from_=new_york, to=houston, distance=1600)
    Road.add(from_=los_angeles, to=chicago, distance=1100)
    Road.add(from_=los_angeles, to=houston, distance=1400)

# Create a graph with weighted edges.
graph = Graph(model, weighted=True)
graph.Node.extend(City)

# Add the roads to the graph as weighted edges.
with model.rule():
    r = Road()
    graph.Edge.add(r.from_, r.to, weight=r.distance)

# Compute the weighted distance between each pair of distinct locations.
with model.query() as select:
    r = Road()
    weighted_distance = graph.compute.weighted_distance(r.from_, r.to)
    response = select(r.from_.name, r.to.name, weighted_distance)

print(response.results)
# Output: 
#           name        name2       v
# 0  Los Angeles      Chicago  1100.0
# 1  Los Angeles      Houston  1400.0
# 2     New York      Chicago   800.0
# 3     New York      Houston  1600.0
# 4     New York  Los Angeles  2500.0
```

## See Also

[`distance()`](./distance.md)