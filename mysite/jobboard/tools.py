# IMPORTS
from .models import Company, Job
import jobboard.crawler_enablers as c

from datetime import date
from datetime import datetime, timezone
import pytz

import requests
from bs4 import BeautifulSoup
import json
from playwright.sync_api import sync_playwright

# SCRAPERS
def scrap(company_name):
    company = Company.objects.get(company_name=company_name)
    print("Begin Scrapping " + company.company_name)
    response = requests.get(company.scraping_source_url)
    source = None  # Le code source de la page
    if response.status_code == 200:
        # Si la requete s'est bien passee
        source = response.text
    return source

def scrap_post(company_name):
    company = Company.objects.get(company_name=company_name)
    print("Begin Scrapping " + company.company_name)
    response = requests.post(company.scraping_source_url)
    source = None  # Le code source de la page
    if response.status_code == 200:
        # Si la requete s'est bien passee
        source = response.text
    return source

def scrap_angel(company_name):
    company = Company.objects.get(company_name=company_name)
    print("Begin Scrapping " + company_name)
    with sync_playwright() as playwright:
        return c.fetch_angel_page(playwright, company.scraping_source_url)

def scrap_welcome(company_name):
    company = Company.objects.get(company_name=company_name)
    print("Begin Scrapping " + company_name)
    company_name_in_url = company_name.replace(" ", "-").lower()
    # HitsPerPage set to 1000 (max.) in "params"
    # To see infos about other parameters, see Algolia doc: https://www.algolia.com/doc/api-reference/api-parameters/
    data = '{"requests":[{"indexName":"wk_cms_jobs_production","params":"query=&hitsPerPage=1000&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&filters=organization.slug%3A'+company_name_in_url+'&facets=%5B%5D&tagFilters="}]}'

    response = requests.post(company.scraping_source_url, data=data)
    source = None
    if response.status_code == 200:
        source = response.text
    return source

def scrap_fisker(i):
    print("Begin Scrapping for Fisker")
    print('Scraping jobs no ' + str(20 * i) + ' to ' + str(20 * (i + 1)))
    skip = str(20 * i)
    url = "https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions?cid=4d18d99e-9909-471d-ad01-1320c70fa0e5&timeStamp=1624631991798&lang=en_US&iccFlag=yes&eccFlag=yes&ccId=19000101_000001&locale=en_US&$skip="+skip+"&$top=20"

    response = requests.get(url)
    source = None
    if response.status_code == 200 :
        source = response.text
    return source

# CRAWLERS
# For almost of the crawlers: Create the job only if it doesn't exist in the database yet, based on offer_url.
# The boucle if has been put outside the create_job() function so as to avoid scraping data for nothing
# (since the function requires all parameters of the job before being able to create the instance)

def crawl_centrical(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    offers = soup.find('div', class_='col-12 col-sm-9 col-md-8 col-lg-9')
    positions = offers.find_all('a')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        offer_url_scrapped = position.get('href')

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("h3").text.strip(' \n\t')
            # COUNTRY / CITY
            location = position.find("span").text.split(',')
            # Best case: the 3 fields are provided
            if len(location) == 3:
            # location looks like "Customer Success, Raanana, Israel"
                country = c.get_country(location[2]).strip(' \n\t')
                city = location[1].strip(' \n\t')
            elif len(location) == 2:
            # location looks like "Customer Success, Israel"
                country = c.get_country(location[1]).strip(' \n\t')
                city = "Unknown"
            else:
                country = 'Unknown'
                city = 'Unknown'
            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for "+company_name)
    print("Added "+str(count_new_jobs)+" new jobs for " + company_name)

def crawl_cleeng(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    positions = soup.find_all('article')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped = "http://cleeng.com" + url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            span_content = position.find("span", class_="_2FV7e")
            job_name = span_content.text

            # COUNTRY / CITY
            ## The separator is preceded by the city and followed by the country in the source page
            separator = position.find("span", class_="_3uSDU")
            # country
            country = c.get_country(separator.next_sibling.text).strip(' \n\t')
            # city
            city = separator.previous_sibling.text.strip(' \n\t')

            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_clippings(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    offers = soup.find('script', id='positionData').string
    positions = json.loads(offers)
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        offer_url_scrapped = "https://clippings.bamboohr.com/jobs/view.php?id=" + str(position['id'])

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position['jobOpeningName']
            # COUNTRY / CITY
            country = c.get_country(position['location']['country']).strip(' \n\t')
            city = position['location']['city'].strip(' \n\t')

            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_drivenets(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    offers = soup.find('div', class_='positions__table')
    positions = offers.find_all('li')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped = "https://drivenets.com" + url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists():
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("p").text.strip(' \n\t')
            # COUNTRY / CITY
            location = position.find("p").next_sibling.next_sibling.next_sibling.next_sibling.text.split(',')
            # Best case: the 2 fields are provided
            if len(location) >= 2:
                country = c.get_country(location[1]).strip(' \n\t')
                city = location[0].strip(' \n\t')
            elif len(location) == 1:
                country = c.get_country(location[0]).strip(' \n\t')
                city = "Unknown"
            else:
                country = 'Unknown'
                city = 'Unknown'
            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_everli(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    offers = soup.find('div', class_='list-container list')
    positions = offers.find_all('div', class_='job')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped= "https://everli.recruitee.com" + url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("a").text.strip(' \n\t')

            # COUNTRY / CITY
            citycountry = position.find("li").text.strip(' \n\t')
            citycountry_list = citycountry.split(",")
            # Best case: the 2 fields are provided:
            if len(citycountry_list) == 2:
                country = c.get_country(citycountry_list[1]).strip(' \n\t')
                city = citycountry_list[0].strip(' \n\t')
            # But sometimes only the city or the country is provided: in that case, the length of citycountry is 1
            elif len(citycountry_list) == 1:
                country = c.get_country(citycountry_list[0]).strip(' \n\t')
                city = 'Unknown'
            else:
                country = 'Unknown'
                city = 'Unknown'
            # REMOTE CASE
            if citycountry == 'Remote job':
                country = 'Remote'
                city = 'Remote'

            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_fisker(company_name):
    company = Company.objects.get(company_name=company_name)
    offer_url = company.scraping_source_url
    count_new_jobs = 0

    # We are going to proceed 20 jobs by 20, until 20*20 = 400 (current max.)
    for i in range(20):
        # SCRAPING
        source_i = scrap_fisker(i)
        # REFORMATTING
        print("Reformatting scrapped data for Fisker")
        print('Reformatting jobs no '+ str(20*i)+' to '+str(20*(i+1)))
        positions_int = json.loads(source_i)
        positions = positions_int['jobRequisitions']
        # PARSING
        print("Begin Parsing for Fisker")
        print('Parsing jobs no '+ str(20*i)+' to '+str(20*(i+1)))

        for position in positions:
            # JOB_NAME
            job_name_scrapped = position['requisitionTitle']

            # CHECK IF JOB ALREADY EXISTS, BASED ON job_name (since offer_url will be the same for all)
            if Job.objects.filter(job_name=job_name_scrapped).exists():
                # If the job already exists, no need to do anything
                comment = 'job already registered'
            else:
                # COUNTRY / CITY
                if position['requisitionLocations'] == []:
                    city = 'Unknown'
                    country = 'Unknown'
                else:
                    city = position['requisitionLocations'][0]['address']['cityName'].strip(' \n\t')
                    if city == '':
                        city = 'Unknown'
                    country = c.get_country(city).strip(' \n\t')
                    if country == '':
                        country = 'Unknown'
                # URL of an offer in particular is not available so will redirect to the list of jobs
                # REGISTER THE JOB
                c.create_job(company_name, job_name_scrapped, country, city, offer_url)
                print(job_name_scrapped)
                count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_foursquare(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    positions = soup.find_all('div', class_='opening')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped = "https://boards.greenhouse.io" + url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("a").text.strip(' \n\t')

            # COUNTRY / CITY
            if position.find("span").text == '':
                city = 'Remote'
                country = 'Remote'
            else:
                city = position.find("span").text.strip(' \n\t')
                country = c.get_country(city).strip(' \n\t')

            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_upmem(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    offers = soup.find('div', class_='block cms-block cms-block-jobs_by_department')
    positions = offers.find_all('li', class_='jobs-list-item')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped = "https://upmem.welcomekit.co" + url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("h3").text.strip(' \n\t')
            # COUNTRY / CITY
            city = position.find("li", class_='jobs-list-item-office').text.strip(' \n\t')
            country = c.get_country(city)
            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_angel_company(company_name):
    # SCRAPING
    source = scrap_angel(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    positions = soup.find_all('div', class_='styles_head__2DUqs')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped = "https://angel.co"+url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("h4").text
            # COUNTRY / CITY
            location = position.find("span").text.split("•")
            if location == '':
                country = 'Unknown'
                city = 'Unknown'
            else:
                city = location[0].strip(' \n\t')
                country = c.get_country(city)

            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added "+str(count_new_jobs)+" new jobs for " + company_name)

def crawl_breezy_company(company_name):
    company = Company.objects.get(company_name=company_name)
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # PARSING
    print("Begin Parsing " + company_name)
    positions = soup.find_all('li', class_='position transition')
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        url = position.a.get('href')
        offer_url_scrapped = company.scraping_source_url + url

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position.find("h2").text
            # COUNTRY / CITY
            location = position.find("span").text.split(",")
            # Best case: the 2 fields are provided (or even 3):
            if len(location) >= 2:
                country = c.get_country(location[1]).strip(' \n\t')
                city = location[0].strip(' \n\t')
            # But sometimes only the city or the country is provided: in that case, the length of citycountry is 1
            elif len(location) == 1:
                country = c.get_country(location[0]).strip(' \n\t')
                city = location[0].strip(' \n\t')
            else:
                country = 'Unknown'
                city = 'Unknown'
            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs for " + company_name)

def crawl_greenhouse_company(company_name):
    # SCRAPING
    source = scrap(company_name)
    soup = BeautifulSoup(source, 'html.parser')
    # REFORMATTING
    print("Reformatting scrapped data for " + company_name)
    positions_int = json.loads(source)
    positions = positions_int['departments']
    # PARSING
    print("Begin Parsing " + company_name)

    for position in positions:
        # some categories can have "nested" tables of jobs in 'children' so we have to make sure we are not missing the jobs in children
        if position['children'] == []:
            for job in position['jobs']:
                c.create_job_greenhouse(job, company_name)
        else:
            for position_children in position['children']:
                for job in position_children['jobs']:
                    c.create_job_greenhouse(job, company_name)
            for job in position['jobs']:
                c.create_job_greenhouse(job, company_name)
    print("Done for " + company_name)

def crawl_welcome_company(company_name):
    # SCRAPING
    source = scrap_welcome(company_name)
    # PARSING
    print("Begin Parsing " + company_name)
    company_name_in_url = company_name.replace(" ", "-").lower()
    positions_int = json.loads(source)
    positions = positions_int['results'][0]['hits']
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        offer_url_scrapped = "https://www.welcometothejungle.com/en/companies/" + company_name_in_url + "/jobs/" + position[
            'slug']
        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position['name']
            # COUNTRY / CITY
            country = c.get_country(position['office']['country']).strip(' \n\t')
            city = position['office']['city'].strip(' \n\t')

            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added "+str(count_new_jobs)+" new jobs for " + company_name)

def crawl_workable_company(company_name):
    # SCRAPING
    source = scrap_post(company_name)
    # REFORMATTING
    print("Reformatting scrapped data for " + company_name)
    positions_int = json.loads(source)
    positions = positions_int['jobs']
    # PARSING
    print("Begin Parsing " + company_name)
    count_new_jobs = 0

    for position in positions:
        # OFFER_URL
        company_name_in_url = company_name.replace(" ", "").lower()
        offer_url_scrapped = "https://apply.workable.com/" + company_name_in_url + "/j/" + position['shortcode']

        # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url
        if Job.objects.filter(offer_url=offer_url_scrapped).exists() :
            # If the job already exists, no need to do anything
            comment = 'job already registered'
        else:
            # JOB_NAME
            job_name = position['title']
            # COUNTRY / CITY
            if position['country'] == '':
                country = 'Unknown'
                city = 'Unknown'
            else:
                country = c.get_country(position['country']).strip(' \n\t')
                if position['city'] == '':
                    city = 'Unknown'
                else:
                    city = position['city'].strip(' \n\t')
            # REGISTER THE JOB
            c.create_job(company_name, job_name, country, city, offer_url_scrapped)
            print(job_name)
            count_new_jobs += 1
    print("Done for " + company_name)
    print("Added " + str(count_new_jobs) + " new jobs")


######################### MAIN #############################
now_begin = datetime.now(pytz.timezone('Europe/Paris'))
now_begin_f = now_begin.strftime("%d/%m/%Y %H:%M:%S")
print("Script began running at", now_begin_f)

# ### DELETING JOBS
# print("Deleting all jobs from database")
# Job.objects.filter().delete()
# print("All jobs deleted from database")

### CRAWLING
print("Starting crawling")
crawl_centrical("Centrical")
crawl_cleeng("Cleeng")
crawl_clippings("Clippings")
crawl_drivenets("Drivenets")
crawl_everli("Everli")
crawl_fisker("Fisker")
crawl_foursquare("Foursquare")
crawl_upmem("Upmem")

## Let's crawl companies using ANGEL.CO
angel_companies = ["Beam"]
for company_name in angel_companies:
     crawl_angel_company(company_name)

## Let's crawl companies using BREEZY.HR
breezy_companies = ["Norbert Health", "Unmade"]
for company_name in breezy_companies:
     crawl_breezy_company(company_name)

## Let's crawl companies using GREENHOUSE
# Foursquare also uses Greenhouse but its case is special so lets deal with apart
greenhouse_companies = ["Formlabs", "Graphcore", "Riskified", "Tulip", "Via"
    , "Duda", "Mixtiles"]
for company_name in greenhouse_companies:
    crawl_greenhouse_company(company_name)

## Let's crawl companies using WELCOME
welcome_companies = ["Jus Mundi", "Zoov"]
for company_name in welcome_companies:
    crawl_welcome_company(company_name)

## Let's crawl companies using WORKABLE
workable_companies = ["Procure Ai"
    , "Lyst", "Trouva"]
for company_name in workable_companies:
    crawl_workable_company(company_name)

now_end = datetime.now(pytz.timezone('Europe/Paris'))
now_end_f = now_end.strftime("%d/%m/%Y %H:%M:%S")
print("Script finished at", now_end_f)