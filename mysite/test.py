
print("A")

if __name__ == '__main__':
    print("dans main")


# IMPORTS
#from .models import Company, Job
import jobboard.crawler_enablers as crawler_enablers
import requests

from bs4 import BeautifulSoup

# SCRAPER
def scrap(syncing_url):
    response = requests.get(syncing_url)
    source = None  # Le code source de la page

    if response.status_code == 200:
        # Si la requete s'est bien passee
        source = response.text
    else:
        print("Error in parsing")
    return source

# PARSERS

print("Begin Scrapping Everli")
# SCRAPING
source = scrap("https://everli.recruitee.com/")
soup = BeautifulSoup(source, 'html.parser')
# PARSING
print("Begin Parsing Everli")
offers = soup.find('div', class_='list-container list')
positions = offers.find_all('div', class_='job')

for position in positions:
    # JOB_NAME
    job_name = position.find("a").text.strip(' \n\t')

    # COUNTRY / CITY
    citycountry = position.find("li").text.strip(' \n\t')
    citycountry_list = citycountry.split(",")

    # Best case: the 2 fields are provided:
    if len(citycountry_list) == 2:
        country = crawler_enablers.get_country(citycountry_list[1]).strip(' \n\t')
        city = citycountry_list[0].strip(' \n\t')
    # But sometimes only the city or the country is provided: in that case, the length of citycountry is 1
    elif len(citycountry_list) == 1:
        country = crawler_enablers.get_country(citycountry_list[0]).strip(' \n\t')
        city = ' '
    else:
        country = ' '
        city = ' '

    # REMOTE CASE
    if citycountry == 'Remote job':
        country = 'Remote'
        city = ' '

    # OFFER_URL
    url = position.a.get('href')
    offer_url = "https://everli.recruitee.com" + url

    # REGISTER THE JOB
    crawler_enablers.create_job("Everli", job_name, country, city, offer_url)
    print("added")
    print(job_name)
