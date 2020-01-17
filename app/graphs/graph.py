from igraph import Graph
from igraph.drawing import plot
from typing import Dict, List
from itertools import groupby


class PageNetwork(Graph):
    def __init__(self, *args, **kwargs):
        kwargs["directed"] = True
        super(PageNetwork, self).__init__(*args, **kwargs)
        self.degree(mode="out")

    def addAdjacency(self, pages: List[Dict]):
        nodes = list(set(p[field] for p in pages))
        titles = [n["title"] for n in nodes]

    def addNodes(self, pages: List[Dict], field: str = "url"):
        """
        Select subset of pages with unique values in `field` and 
        add them to graph.
        """
        nodes = list(set(p[field] for p in pages))
        self.add_vertices(nodes)

    def addEdges(
        self, pages: List[Dict], source: str = "url", target: str = "links"
    ):
        """
        Create edges between `pages`. `Source` field specifies node name,
        `target` specifies names of adjacent nodes. If `target` does not 
        exist in list of pages field `source` then new node is created.  
        """
        nodes = [v["name"] for v in self.vs]
        # List of unique edges as tuples: (source, target)
        edges = [(page[source], tar) for page in pages for tar in page[target]]
        edges = list(set(edges))
        # If target in list of edges does not exist in list of nodes create new node
        new_nodes = [(e[1], e[0]) for e in edges if e[1] not in nodes]
        # self.add_vertices({"title": "", "url": e[1], "link": })
        new_nodes.sort(key=lambda x: x[0])
        add_nodes = [
            {"title": "", "url": key, "links": [i[1] for i in item]}
            for key, item in groupby(new_nodes, lambda x: x[0])
        ]
        self.addNodes(add_nodes)
        pages.extend(add_nodes)
        edges = [(page[source], tar) for page in pages for tar in page[target]]
        edges = list(set(edges))
        self.add_edges(edges)

    def plotNetwork(self, source: str, target: str, filename: str = None):
        path = self.get_shortest_paths(source, to=target)
        path = path[0]
        path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        visual_style = {
            "vertex_label": [n["name"] for n in self.vs],
            "vertex_size": [
                10 if n["name"] == source or n["name"] == target else 5
                for n in self.vs
            ],
            "vertex_label_color": [
                [0, 0, 0, 1]
                if n["name"] == source
                else [0, 0, 0, 1]
                if n["name"] == target
                else [0, 0, 0, 0]
                for n in self.vs
            ],
            "vertex_color": [
                [0, 1, 0, 1]
                if n["name"] == source
                else [1, 0, 0, 1]
                if n["name"] == target
                else [0, 0, 0, 0.2]
                for n in self.vs
            ],
            "edge_color": [
                [0, 0, 0, 1] if e in path else [0, 0, 0, 0.2]
                for e in self.get_edgelist()
            ],
        }
        layout_name = "fr"
        bbox = (1000, 1000)
        if filename:
            plot(
                self,
                filename,
                **visual_style,
                vertex_frame_width=0.1,
                layout=self.layout(layout_name),
                bbox=bbox,
                autocurve=True,
            )
        else:
            plot(
                self,
                **visual_style,
                vertex_frame_width=0.1,
                layout=self.layout(layout_name),
                bbox=bbox,
                autocurve=True,
            )
