from igraph import Graph
from typing import Dict, List


class Node:
    def __init__(self, title, url, links):
        self.title = title
        self.url = url
        self.links = links


class PageNetwork(Graph):
    def __init__(self, *args, **kwargs):
        kwargs["directed"] = True
        super(PageNetwork, self).__init__(*args, **kwargs)
        self.degree(mode="out")

    def addNodes(self, pages: List[Dict], field: str):
        self.add_vertices((map(lambda x: x[field], pages)))

    def addEdges(self, pages: List[Dict], source: str, target: List[str]):
        edges = [(page[source], tar) for page in pages for tar in page[target]]
        edges = list(set(edges))
        self.add_edges(edges)
