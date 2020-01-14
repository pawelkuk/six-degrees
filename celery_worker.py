from app import celery, create_app  # noqa

app = create_app()
app.app_context().push()

from app.celery.tasks import (  # noqa
    check_if_target_reached,
    get_page,
    get_page_with_api,
    download_pages
)
