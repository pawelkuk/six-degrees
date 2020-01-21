from app.main import bp
from app.main.forms import WikiNodesForm
from flask import render_template, flash, redirect
from app.celery.tasks import download_pages, get_page, get_page_with_api
from app.graphs import graph, network
import re
import json


reg = re.compile(
    r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\."
    r"[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    form = WikiNodesForm()
    if form.validate_on_submit():
        source = form.source.data
        target = form.target.data

        source_match = reg.search(source) is not None
        target_match = reg.search(target) is not None
        if source_match and target_match:
            func = get_page
        elif not source_match and not target_match:
            func = get_page_with_api
        else:
            flash("Mixed pages formats, use name of article or url")
            return redirect("/index")

        pages = download_pages(func, source, target, "url")
        net = network.PageNetwork()
        net.addNodes(pages, "url")
        net.addEdges(pages, source="url", target="links")
        min_path_network = net.plotNetwork(
            source, target, size=(800, 1800), filename="graph.html"
        )
        return render_template(
            "index.html",
            title="Home",
            form=form,
            nodes=json.dumps(min_path_network.nodes),
            edges=json.dumps(min_path_network.edges),
            options=json.dumps(min_path_network.options),
        )

    return render_template(
        "index.html",
        title="Home",
        form=form,
        nodes=None,
        edges=None,
        options=None,
    )
