# The Six Degrees of Separation Project

## To get the app running:

- Clone the repo: `git clone https://github.com/pawelkuk/six-degrees`
- Assuming docker is installed: `docker run -d -p 6379:6379 redis`
- Assuming a fresh virtual environment: `pip install -r requirements.txt`
- Run a celery worker: `celery -A celery_worker.celery  worker --loglevel=INFO --concurrency=20 -n worker1@%h`
- Run the development server in debug mode: `flask run`
- To run tests type: `pytest` in the project root directory 

### Dev info
 
- To run the async version of the scraper type: `python wiki_scraper.py` in the root directory