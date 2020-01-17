from app.graphs import graph, network
from igraph.drawing import plot


def test_nonexistent_target():
    net = graph.PageNetwork()
    pages = [
        {"title": "00", "url": "0", "links": ["1", "3", "5", "6"]},
        {"title": "01", "url": "1", "links": ["0", "2", "3"]},
        {"title": "02", "url": "2", "links": ["0", "3"]},
        {"title": "03", "url": "3", "links": ["4", "1"]},
        {"title": "04", "url": "4", "links": ["2"]},
        {"title": "05", "url": "5", "links": ["4"]},
    ]

    net.addNodes(pages, "url")
    net.addEdges(pages, source="url", target="links")
