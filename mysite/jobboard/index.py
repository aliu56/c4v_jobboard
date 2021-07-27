import algoliasearch_django as algoliasearch

from .models import Job, Company

algoliasearch.register(Job)
algoliasearch.register(Company)
