# `relationalai.std.graphs.Compute.distance()`

```python
relationalai.std.graphs.Compute.distance(node1: Producer, node2: Producer) -> Expression
```

Returns an [`Expression`](../../../Expression.md) that computes the
the shortest path length from `node1` and `node2`.
Note: Be careful using `distance` on the entire graph, since for large graphs, this may be infeasible. 

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Weights are ignored.   |

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
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "transportationNetwork" with City and Road types.
model = rai.Model("transportationNetwork")
City = model.Type("City")
Road = model.Type("Road")

# Add cities and roads to the model.
with model.rule():
    new_york = City.add(name="New York")
    los_angeles = City.add(name="Los Angeles")
    chicago = City.add(name="Chicago")
    houston = City.add(name="Houston")
    Road.add(city1=new_york, city2=chicago)
    Road.add(city1=new_york, city2=houston)
    Road.add(city1=chicago, city2=los_angeles)
    Road.add(city1=houston, city2=los_angeles)

# Create a graph with nodes from City and edges from Road.
graph = Graph(model, undirected=True) 
graph.Node.extend(City)
with model.rule():
    road = Road()
    graph.Edge.add(road.city1, road.city2)

# Compute smallest number of roads you must take to get from Los Angeles and New York.
with model.query() as select:
    los_angeles = City(name="Los Angeles")
    new_york = City(name="New York")
    distance = graph.compute.distance(los_angeles, new_york)
    response = select(alias(distance, "distance"))

print(response.results)
# Output:
#    distance
# 0         2
```

## See Also

[`weighted_distance()`](./weighted_distance.md)
