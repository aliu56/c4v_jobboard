from .models import Company, Job
from playwright.sync_api import sync_playwright
import datetime
import pytz

# Reverse geocoding (get country from address)
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

def get_country(location):
    # Otherwise the function returns "United States"
    if location == "Asia Pacifica":
        return "Asia"
    else:
        res = str(geolocator.geocode(location, language="en"))
        country = res.split(',')[-1]
        return country

# CREATE A JOB AND SAVE IT ON THE DATABASE
def create_job(company_name, jobname_input, country_input, city_input, offerurl_input):
    c = Company.objects.get(company_name = company_name)
    j = Job(company = c
            , job_name = jobname_input
            , country = country_input
            , city = city_input
            , crawl_date = datetime.datetime.now(tz=pytz.utc)
            , offer_url= offerurl_input)
    j.save()


# ANGEL.CO : Fetch the data with Playwright
def fetch_angel_page(playwright, scraping_source_url):
    webkit = playwright.webkit
    browser = webkit.launch()
    context = browser.new_context(
            java_script_enabled = False
            #user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    )
    page = context.new_page()
    page.goto(scraping_source_url)
    html = page.content()
    browser.close()
    return html

# GREENHOUSE: Fetch the data of a job
def greenhouse_fetch_data(job):
    # JOB NAME
    job_name = job['title']
    # COUNTRY / CITY
    location = job['location']['name'].split(',')
    # Best case: the 2 fields are provided (or even 3):
    if len(location) >= 2:
        country = get_country(location[-1]).strip(' \n\t')
        city = location[0].strip(' \n\t')
    # But sometimes only the city or the country is provided: in that case, the length of citycountry is 1
    elif len(location) == 1:
        country = get_country(location[0]).strip(' \n\t')
        city = location[0].strip(' \n\t')
    else:
        country = 'Unknown'
        city = 'Unknown'
    # OFFER_URL
    offer_url = job['absolute_url']
    return ([job_name, country, city, offer_url])

# GREENHOUSE: Create THE JOB, only if job doesn't exist yet (based on offer_url)
def create_job_greenhouse(job, company_name):
    # CHECK IF JOB ALREADY EXISTS, BASED ON offer_url (which is job['absolute_url'])
    if Job.objects.filter(offer_url=job['absolute_url']).exists():
        # If the job already exists, no need to do anything
        comment = 'job already registered'
    else:
        data = greenhouse_fetch_data(job)
        (job_name, country, city, offer_url_scrapped) = (data[0], data[1], data[2], data[3])
        create_job(company_name, job_name, country, city, offer_url_scrapped)
        print(job_name)