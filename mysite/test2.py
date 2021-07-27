from bs4 import BeautifulSoup


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright


    def fetch(playwright):
        webkit = playwright.webkit
        browser = webkit.launch(headless=False)
        context = browser.new_context(
            java_script_enabled = False
            #user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        )
        page = context.new_page()
        page.goto("https://angel.co/company/beam-app-1/")
        html = page.content()
        browser.close()
        return html

    def call_fetch():
        with sync_playwright() as playwright:
            return fetch(playwright)

    source = call_fetch()
    # do crawler

    # #company = Company.objects.get(company_name=company_name)
    # # SCRAPING
    # print("Begin Scrapping")
    # print(company_name)
    # source = scrap(company.scraping_source_url)
    soup = BeautifulSoup(source, 'html.parser')
    # # PARSING
    # print("Begin Parsing")
    # print(company_name)
    offers = soup.find("div", class_='styles_section__2-RVo')
    positions = soup.find_all('div', class_='styles_head__2DUqs')

    for position in positions:
        # JOB_NAME
        job_name = position.find("h4").text
        # COUNTRY / CITY
        location = position.find("span").text.split("•")
        if location == '':
            country = 'Unknown'
            city = 'Unknown'
        else:
            city = location[0].strip(' \n\t')
            country = 'country to come'#c.get_country(location[0]).strip(' \n\t')
        # OFFER_URL
        url = position.a.get('href')
        offer_url = url #company.scraping_source_url + url

        # REGISTER THE JOB
        #c.create_job(company_name, job_name, country, city, offer_url)
        print(job_name)
        print(city)
        print(offer_url)


