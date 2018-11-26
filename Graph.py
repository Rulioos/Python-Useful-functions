class Graph:
    def __init__(self, edges):
        """
        Init function.
        :param edges:Dictionnary
        """
        self.edges = dict()
        self.nodes = dict()
        self._construct_edges(edges)
        pass

    def _construct_edges(self, edges):
        """
        Initialize the graph with edges and nodes
        :param edges: dict from edges
        :return: nothing
        """
        for key, item in edges.items():
            if key not in self.edges.keys():
                A = self._nodes_exists(item["node_init"])
                B = self._nodes_exists(item["node_end"])
                self.edges[key] = Edge(key, A, B, item["value"],item["oriented"])

    def _nodes_exists(self, item, override=False):
        """
        Check if a node exists and if it doesn't creates one.
        If it does exist then it'll return the existing node if not override.
        If override, replace the existing node.
        :param item: a tuple of data (id,value)
        :param override: boolean
        :return: A node
        """
        node_id = item[0]
        if node_id not in self.nodes.keys() or override:
            node = Node(item[0], item[1])
            self.nodes[item[0]] = node
            return node
        else:

            node = self.nodes[item[0]]
            return node

    def add_edge(self, edge, override=False):
        """
        Implements a new edge. If override replace existing edge
        :param edge: dict
        :param override: boolean
        :return: nothing
        """
        pass


class Node:
    def __init__(self,
                 id,
                 value):
        """
        Initialize node
        :param id: Unique id to identify the node
        :param value: value of the node
        """
        self.value = value
        self.id = id


class Edge:
    def __init__(self,
                 id,
                 node_init,
                 node_end,
                 value,
                 oriented):
        """
        Initialize Edge
        :param id: Unique id to identify edge
        :param node_init: the start node
        :param node_end: the end node
        :param value: value of the edge
        :param oriented: boolean
        """
        self.id = id
        self.value = value
        self.node_init = node_init
        self.node_end = node_end
        self.oriented=oriented


edges = {
    "myFirstEdge":
        {
            "node_init": ("bonjour", 2),
            "node_end": ("au revoir", 0),
            "value": 5,
            "oriented":True
        },
    "mySecondEdge":
        {
            "node_init": ("bonjour", 2),
            "node_end": ("au revoir", 0),
            "value": 5,
            "oriented":False
        }
}


g = Graph(edges)
print(g.edges["myFirstEdge"].oriented)

