from networkx import DiGraph
import networkx as nx
from typing import Dict, List, Tuple
from itertools import groupby, chain
from pyvis.network import Network


class PageNetwork(DiGraph):
    def __init__(self, *args, **kwargs):
        super(PageNetwork, self).__init__(*args, **kwargs)

    def addNodes(self, pages: List[Dict], field: str = "url"):
        """
        Select subset of pages with unique values in `field` and
        add them to graph.
        """
        nodes = list(set(p[field] for p in pages))
        self.add_nodes_from(nodes)

    def addEdges(
        self, pages: List[Dict], source: str = "url", target: str = "links"
    ):
        """
        Create edges between `pages`. `Source` field specifies node name,
        `target` specifies names of adjacent nodes. If `target` does not
        exist in list of pages field `source` then new node is created.
        """
        nodes = list(self.nodes)
        # List of unique edges as tuples: (source, target)
        edges = [(page[source], tar) for page in pages for tar in page[target]]
        edges = list(set(edges))
        # If target in list of edges does not exist in list of
        # nodes create new node
        new_nodes = [(e[1], e[0]) for e in edges if e[1] not in nodes]
        new_nodes.sort(key=lambda x: x[0])
        add_nodes = [
            {"title": "", "url": key, "links": [i[1] for i in item]}
            for key, item in groupby(new_nodes, lambda x: x[0])
        ]
        self.addNodes(add_nodes)
        pages.extend(add_nodes)
        edges = [(page[source], tar) for page in pages for tar in page[target]]
        edges = list(set(edges))
        self.add_edges_from(edges)

    def plotNetwork(
        self,
        source: str,
        target: str,
        filename: str = "net.html",
        size: Tuple[int, int] = (500, 500),
    ):
        try:
            paths = nx.all_shortest_paths(self, source, target)
        except nx.NetworkXNoPath as e:
            print("No path")
        finally:
            paths = list(paths)
            nodes = list(set(chain.from_iterable(paths)))
            edges = [
                (p[i], p[i + 1]) for p in paths for i in range(0, len(p) - 1)
            ]

            g = Network(height=size[0], width=size[1], directed=True)
            g.add_nodes(
                nodes,
                color=[
                    "red"
                    if n == source
                    else "green"
                    if n == target
                    else "blue"
                    for n in nodes
                ],
            )
            g.add_edges(edges)
            g.set_options(
                """
            {
"nodes": {
    "font": {
        "size": 9
    },
    "scaling": {
        "max": 36
    },
    "shadow": {
        "enabled": true
    }
},
"edges": {
    "arrows": {
        "to": {
            "enabled": true,
            "scaleFactor": 1.4
        }
    },
    "smooth": false
},
"layout": {
    "hierarchical": {
        "enabled": true,
        "sortMethod": "directed"
    }
},
"interaction": {
    "keyboard": {
        "enabled": true
    }
},
"physics": {
    "hierarchicalRepulsion": {
        "centralGravity": 0,
        "nodeDistance": 225
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
}
}"""
            )
            return g
