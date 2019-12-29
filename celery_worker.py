import os
from app import celery, create_app

app = create_app()
app.app_context().push()

from app.celery.tasks import (
    xsum,
    add,
    mul,
    check_if_target_reached,
    concatenate_lists_of_urls,
    get_article_name,
    get_wikilinks,
)