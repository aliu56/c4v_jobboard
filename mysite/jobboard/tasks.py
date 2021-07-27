

# IMPORTS
from .models import Company, Job
import jobboard.crawler_enablers as c

from datetime import datetime
import pytz

import celery

# import requests
# from bs4 import BeautifulSoup

app = celery.Celery('tasks', broker='redis://localhost//')#, backend='redis')

@app.task(bind=True)
def begin(self):
    now_begin = datetime.now(pytz.timezone('Europe/Paris'))
    now_begin_f = now_begin.strftime("%d/%m/%Y %H:%M:%S")
    print("Script began running at", now_begin_f)
    return 'it worked'

@app.task(bind=True)
def delete(self):
    ### DELETING JOBS
    print("Deleting all jobs from database")
    Job.objects.filter().delete()
    print("All jobs deleted from database")

# # SCRAPERS
# @app.task(bind=True)
# def scrap(company_name):
#     company = Company.objects.get(company_name=company_name)
#     print("Begin Scrapping " + company.company_name)
#     response = requests.get(company.scraping_source_url)
#     source = None  # Le code source de la page
#     if response.status_code == 200:
#         # Si la requete s'est bien passee
#         source = response.text
#     return source
#
# # CRAWLERS
# @app.task(bind=True)
# def crawl_centrical(company_name):
#     # SCRAPING
#     source = scrap(company_name)
#     soup = BeautifulSoup(source, 'html.parser')
#     # PARSING
#     print("Begin Parsing " + company_name)
#     offers = soup.find('div', class_='col-12 col-sm-9 col-md-8 col-lg-9')
#     positions = offers.find_all('a')
#     count_new_jobs = 0
#
#     for position in positions:
#         # OFFER_URL
#         offer_url_scrapped = position.get('href')
#
#         # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
#         if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
#             # If the job already exists, no need to do anything
#             comment = 'job already registered'
#         else:
#             # JOB_NAME
#             job_name = position.find("h3").text.strip(' \n\t')
#             # COUNTRY / CITY
#             location = position.find("span").text.split(',')
#             # Best case: the 3 fields are provided
#             if len(location) == 3:
#             # location looks like "Customer Success, Raanana, Israel"
#                 country = c.get_country(location[2]).strip(' \n\t')
#                 city = location[1].strip(' \n\t')
#             elif len(location) == 2:
#             # location looks like "Customer Success, Israel"
#                 country = c.get_country(location[1]).strip(' \n\t')
#                 city = "Unknown"
#             else:
#                 country = 'Unknown'
#                 city = 'Unknown'
#             # REGISTER THE JOB
#             c.create_job(company_name, job_name, country, city, offer_url_scrapped)
#             print(job_name)
#             count_new_jobs += 1
#     print("Done for "+company_name)
#     print("Added "+str(count_new_jobs)+" new jobs for " + company_name)
