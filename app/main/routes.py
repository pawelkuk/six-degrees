from app.main import bp
from app.main.forms import WikiNodesForm
from flask import render_template, flash, redirect


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    form = WikiNodesForm()
    if form.validate_on_submit():
        flash(f"This is the data you've sent: {form.source.data}, {form.destination.data}")
        return redirect('/index')
    return render_template("index.html", title="Home", form=form)
