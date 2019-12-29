# The Six Degrees of Separation Project

## To get the app running:

- Clone the repo: `git clone https://github.com/pawelkuk/six-degrees`
- Assuming docker is installed: `docker run -d -p 6379:6379 redis`
- Assuming a fresh virtual environment: `pip install -r requirements.txt`
- Run a celery worker: `celery worker -A celery_worker.celery --loglevel=info`
- Run the development server in debug mode: `flask run`