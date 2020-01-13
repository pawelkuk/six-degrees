from app.celery.tasks import find_path, find_path_with_sessions
from time import time


target_url = "https://en.wikipedia.org/wiki/Deflection_(engineering)"
# target_url = "https://en.wikipedia.org/wiki/Castigliano%27s_method"
source_url = "https://en.wikipedia.org/wiki/Span_(engineering)"


start = time()
flag = find_path(source_url, target_url)
end = time()
assert flag
print(end - start)

start = time()
flag = find_path_with_sessions(source_url, target_url)
end = time()
assert flag
print(end - start)
