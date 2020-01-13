from app.graph import graph
import igraph as ig


def test_init():

    net = graph.PageNetwork()
    pages = [
        {"title": "0", "url": "0", "links": ["1", "3", "5"]},
        {"title": "1", "url": "1", "links": ["0", "2", "3"]},
        {"title": "2", "url": "2", "links": ["0", "3"]},
        {"title": "3", "url": "3", "links": ["4", "1"]},
        {"title": "4", "url": "4", "links": ["2"]},
        {"title": "5", "url": "5", "links": ["4"]},
    ]

    net.addNodes(pages, "url")
    net.addEdges(pages, source="url", target="links")

    source = pages[0]
    target = pages[4]
    path = net.get_shortest_paths(source["title"], to=target["title"])
    path = path[0]
    path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    visual_style = {
        "vertex_label": [page["title"] for page in pages],
        "vertex_label_color": [
            [0, 0, 0, 1]
            if page["title"] == source["title"]
            else [0, 0, 0, 1]
            if page["title"] == target["title"]
            else [0, 0, 0, 0.2]
            for page in pages
        ],
        "vertex_color": [
            [0, 1, 0, 1]
            if page["title"] == source["title"]
            else [1, 0, 0, 1]
            if page["title"] == target["title"]
            else [0, 0, 0, 0.2]
            for page in pages
        ],
        "edge_color": [
            [0, 0, 0, 1] if e in path else [0, 0, 0, 0.2]
            for e in net.get_edgelist()
        ],
    }
    ig.plot(
        net,
        f"tests/test_graph_init.png",
        **visual_style,
        vertex_frame_width=0.1,
        layout=net.layout("large"),
        bbox=(500, 500),
        autocurve=True,
    )
