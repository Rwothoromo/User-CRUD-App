from flask_caching import Cache

# Caching data in the application allows reduction of calls to database,
# additional computation, etc. Flask-Cache helps solve this problem.
cache = Cache(config={'CACHE_TYPE': 'simple'})
