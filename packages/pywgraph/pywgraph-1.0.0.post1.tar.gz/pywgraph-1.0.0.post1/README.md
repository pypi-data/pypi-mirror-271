# pywgraph
A library to manipulate weighted graphs in python. This library focus on directed graphs whose edges have weights. The weights of the graph can be any elements of a fixed mathematical group. By default, the underlying group is set to be the real numbers with the multiplication. Thus, when trasversing the graph, the weight of the path is the product of the weights of the edges, but in general, it is the product under the binary operation of the group. 

For this reason, this package also includes a basic abstraction of a group. The group definition is base on:
*  The a function of two variables that return one element (the binary operation of the group).
*  The inverse function of an element. This is, the function that given an element of the group returns it inverse. 
*  The identity element of the group.
*  Optional, a hash function for the elements of the group. By default it is taken the standard python hash function. If your group contains not hashable elements you should provide one. 

## QUICKSTART

### Edges

The main object to construct the graph is the `WeightedDirectedEdge` class. This represents a directed edge with a weight. The construction basic construction is as follows: 

```python
from pywgraph import WeightedDirectedEdge

edge = WeightedDirectedEdge("A", "B", 0.5)
```

The first two parameters are the nodes that the edge connects. The last parameter is the weight. It is important to notice that, since this is a directed edge, the order of the nodes is important. Since we do have not specify any group, the default group is the real numbers with the multiplication. 

You can call the start and end nodes with `edge.start` and `edge.end`, respectevely. To get the weight, simply use `edge.weight`. You can also get the *inverse edge* with `edge.inverse`. This is, the edge that connects the end node of `edge` to the start node of `edge` and has `1/edge.weight` as weight (as said previously, in the future this is meant to be the inverse of the weight in the underlying group).

Also, this class is hashable and iterable, yielding the start node, end node and weight. 


### Graph

The graph is represented by the `WeightedDirectedGraph` class. This is the main class of the package. The graph itself is a set of nodes and a set of `WeightedDirectedEdge`s. If you don`t specify it, the underlying group for the weights as said would be the real numbers with the multiplication. 

It is also possible, and more comfortable, to create the graph using the `WeightedDirectedGraph.from_dict` method, which instantiates the graph from a dictionary. The keys of the dictionary are the starting nodes. The values must consists of another dictionary, where the keys are the ending nodes and the value is the weight of the edge. It is important that all nodes of the graph must be keys in the dictionary. If, for example, there is a node "C" that has no children nodes, then the dictionary must have a key "C" with a value of `{}`.
As always, if you want to use another group for the weights you should specify it here. 

```python
from pywgraph import WeightedDirectedGraph

g = WeightedDirectedGraph.from_dict({
    "A": {"B": 0.5},
    "B": {"A": 0.5, "C": 1.0},
    "C": {}
})
```

The equivalent construction using set of nodes and set of edges is as follows: 

```python 
from pywgraph import WeightedDirectedGraph

graph = WeightedDirectedGraph(
    nodes={"A", "B", "C"},
    edges={
        WeightedDirectedEdge("A", "B", 0.5),
        WeightedDirectedEdge("B", "A", 0.5),
        WeightedDirectedEdge("B", "C", 1.0)
    }
)
``` 

You can instantiate a bad define graph by not writting all the nodes that appear in the edges in the nodes set. There is a method `check_defintion` that checks if the graph is well defined, but the check is not enforce. You can retrieve the nodes and edges by `graph.nodes` and `graph.edges`, respectively.

You can also acces the children and the parents of a nodes with the methods `children` and `parents`, respectively.

```python
graph.children("A")
# {"B"}

graph.parents("A")
# {}

graph.children("B")
# {"A", "C"}
```

The main use of this graph object is to work with their weights as group elements, so you should not add the reverse edge of an existing edge with a bad inverse weight. For this, there is the method `add_reverse_edges` that returns a new graph with the original graph with all the reverse edges added. You can also modify the graph directly with the paremeter `inplace=True`. 

```python
graph_w_inverse_edges = graph.add_reverse_edges()

# Updating the graph 
graph.add_reverse_edges(inplace=True)
```

### Path finding

There is a method `find_path` that finds one of the shortest path between two nodes. This method returns a list of edges that represents the path. The method has two parameters: `start` and `end`. Both must be nodes of the graph. If not, an error is raised. If there is not path between the given nodes the empty list will be return. 

```python
dictionary = {
    "A": {"B": 1.0, "C": 2.5},
    "B": {"C": 2.5},
    "C": {"A": 1 / 2.5, "D": 1.3},
    "D": {"E": 3.4},
    "E": {"C": 1 / (1.3 * 3.4), "A": 13.0},
    "Z": {},
}
graph = WeightedDirectedGraph.from_dict(dictionary)

graph.find_path("A", "B")
# ["A", "B]

graph.find_path("A", "Z")
# []

graph.find_path("A", "E")
# ["A", "C", "D", "E"]

graph.find_path("A", "A")
# ["A"]
```

There are also methods to get the weight of following a path. This methods are `path_weight` and `weight_between`. The first one receives a path (a list of consecutive nodes) and returns the weight of the path (the product of the weights). If the given path does not exists an exception will be raised. If the empty path is given the return weight will be `0`. The second method receives the start and end nodes and returns the weight of one of the shortest paths between them. If there is not path between the given nodes the return weight will be `0`. The weight between a node an itself will be `1`. 

```python
graph.path_weight([])
# 0.0

graph.path_weight(["A", "B"])
# 1.0

graph.path_weight(["A", "B", "C"])
# 2.5

grap.weight_between("A", "C")
# 2.5

grap.weight_between("A", "Z")
# 0.0

grap.weight_between("A", "A")
# 1.0
```

**WARNING**: Currently, if a path that contains a cycle is given the method `path_weight` will raise an error. In future this behaviour will be change to allow cycles. 

### Graphs and groups

#### Introduction to the `Group` class
As said in the introduction, there is also an abstraction of a mathematical group. This object is call simply `Group`. To initialize it you need to provide a description of the group (string), the binary operation, the inverse operation and the identity element. If the elements of the group are not hashable, you should provide a hash function. One example could be an implementation of $\mathbb{R^2}$ under addition. For this we could represent vectors with numpy arrays, which are not hashable. We can construct this group as follows. 

```python
from pywgraph import Group

group = Group(
    name="R^2 under addition",
    operation=lambda x, y: x + y,
    inverse_function=lambda x: -x,
    identity=np.zeros(2),
    hash_function=lambda x: hash(tuple(x))
)
```

This group instance is callable. The call gets two variables as inputs and return the operation between them. Since there is no type checking, the user is responsible of using it with valid inputs. You can also call the group operation with the property `Group.operation` and the inverse operation by `Group.inverse_function`. The identity element is stored in the property `Group.identity`. If you need to, you can also get back the hash function with the property `Group.hash_function`. 

```python
import numpy as np 
vector_1 = np.array([1, 3])
vector_2 = np.arra([-1, 7])

group(vector_1, vector_2)
# np.array([0, 10])

group.operation(vector_1, vector_2)
# np.array([0, 10])

group.inverse_operation(vector_1, vector_2)
# np.array([2, -4])

group.neutral_element
# np.array([0, 0])
```

#### General weights for edges

Now that we introduce how to construct a group we will se how to use it to provide elements of an arbitrary group as weights of an edge. To do so you just need to create the group and add it as a parameter in the constructor of edge.

```python
from pywgraph import WeightedDirectedEdge, Group
import numpy as np 
group = Group(
    name="R^2 under addition",
    operation=lambda x, y: x + y,
    inverse_function=lambda x: -x,
    identity=np.zeros(2),
    hash_function=lambda x: hash(tuple(x))
)
weight_of_edge = np.array([1, 2])

edge = WeightedDirectedEdge("A", "B", weight_of_edge, group)
```

With the group information given, now this edge instance knows how to construct the inverse edge. 

```python
edge.inverse
# WeightedDirectedEdge("B", "A", np.array([-1, -2]), group)
```

Is important to notice that there is no checking of wether the provide weight is a valid element of the given group. In the future there will be an option to implement an element checker in the group definition. 

#### General weighted graphs

Now for constructing a weighted directed graph whose weights are elements of a specific group you just need to define the group and create the graph adding the group as parameter. The edges of the graph need to include the group as well, as seen before. A better way to construct the graph is to use the method `WeightedDirectedGraph.from_dict`. Now this works exactly the same but adding the group as a new parameter. 

With this implementation any method that concerns weights uses the group operation to handle it. For example, the weight of a given path that the `WeightedDirectedGraph.path_weight` yields is obtain with the consecutive application of the group operation. The same happens with the `WeightedDirectedGraph.weight_between` method. 

```python
from pywgraph import WeightedDirectedGraph, Group
import numpy as np 
group = Group(
    "R^2 under addition",
    lambda x, y: x + y,
    lambda x, y: x - y,
    np.zeros(2),
    hash_function=lambda x: hash(tuple(x))
)

dictionary = {
    "A": {"B": np.array([1, 2.5]), "C": np.array([-1, 3.4])},
    "B": {"C": np.array([2.5, -1])},
    "C": {"A": np.array([1 / 2.5, 1 / 3.4]), "D": np.array([1.3, 3.4])},
    "D": {"E": np.array([3.4, 1.3])},
    "E": {},
}

graph = WeightedDirectedGraph.from_dict(dictionary, group)
# Creates the graph

graph.path_weight(["A", "C"])
# np.array([-1, 3.4])

graph.path_weight(["A", "B", "C"])
# np.array([1, 2.5]) + np.array([2.5, -1]) = np.array([3.5, 1.5])

graph.weight_between("A", "C")
# np.array([-1, 3.4])

graph.weight_between("A", "Z")
# np.array([0, 0])

graph.weight_between("A", "Z")
# None

graph.weight_between("A", "Z", np.array([1,1]))
# np.array([1,1])
```

Notice that this graph is not conmutative since the weight of the path `["A", "C"]` is different from the weight of the path `["A", "B", "C]`.
