# The Six Degrees of Separation Project (works with english wiki)

## To get the app running:

- Clone the repo: `git clone https://github.com/pawelkuk/six-degrees`
- Assuming docker is installed: `docker run -d -p 6379:6379 redis`
- Assuming a fresh virtual environment (python 3.7+ required): `pip install -r requirements.txt`
- Run a celery worker: `celery -A celery_worker.celery  worker --loglevel=INFO --concurrency=20 -n worker1@%h`
- Run the development server in debug mode: `flask run`. Now you can go to `localhost:5000` and pass in the forms either urls to wiki pages or you can just type the articles you are interested in
- To run tests type: `pytest` in the project root directory 

### Dev info
 
- To run the async version of the scraper type: `python wiki_scraper.py` in the root directory
- To run the aiohttp version of the scraper type: `python aiohttp_scraper.py` in the root directory
- To delete all task from celery task queue type: `celery -A celery_worker.celery purge`