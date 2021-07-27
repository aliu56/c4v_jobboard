import datetime

from django.db import models
from django.utils import timezone 

class Company(models.Model):
	company_name = models.CharField('Company', max_length=200)
	logo = models.ImageField('Logo', upload_to=None, max_length=200)

	DEFAULT = 'N'
	OTHER = 'O'

	SEED = 'S'
	SERIES_A = 'A'
	SERIES_B = 'B'
	SERIES_C = 'C'

	STAGE_CHOICES = [
	(DEFAULT, '-'),
	(SEED, 'Seed'),
	(SERIES_A, 'Series A'),
	(SERIES_B, 'Series B'),
	(SERIES_C, 'Series C'),
	(OTHER, 'Other'),
]
	stage = models.CharField(
		'Stage',
		max_length=100,
		choices=STAGE_CHOICES,
		default=DEFAULT,
	)

	B2B_SERVICES_OPERATION = 'B2BO'
	CONSUMER = 'CONS'
	DATA = 'DATA'
	HEALTH = 'HEAL'
	INSURTECH = 'INSU'
	NEW_INFRASTRUCTURE_COMPUTING = 'NEWI'
	SAAS = 'SAAS'
	TECH = 'TECH'

	SECTOR_CHOICES = [
		(DEFAULT, '-'),
		(B2B_SERVICES_OPERATION, 'B2B Services / Operation'),
		(CONSUMER, 'Consumer'),
		(DATA, 'Data'),
		(HEALTH, 'Health'),
		(INSURTECH, 'InsurTech'),
		(NEW_INFRASTRUCTURE_COMPUTING, 'New Infrastructure / Computing'),
		(SAAS, 'SaaS'),
		(TECH, 'Tech'),
		(OTHER, 'Other'),
	]
	sector = models.CharField(
		'Sector',
		max_length=100,
		choices=SECTOR_CHOICES,
		default=DEFAULT,
	)

	company_website_url = models.CharField('Website', max_length=200)
	scraping_source_url = models.CharField('Syncing source:', max_length=1000)

	def __str__(self):
		return self.company_name.capitalize()

	class Meta:
		verbose_name_plural = "Companies"


class Job(models.Model):
	company = models.ForeignKey(Company, related_name='jobs', on_delete=models.CASCADE)

	job_name = models.CharField('Job', max_length=200)
	country = models.CharField('Country', max_length=50, null=True, blank=True)
	city = models.CharField('City', max_length=50, null=True, blank=True)
	crawl_date = models.DateTimeField('Date of the crawl')
	offer_url = models.CharField('Offer Link', max_length=500, null=True, blank=True)

	def __str__(self):
		return self.job_name

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.crawl_date <= now
	was_published_recently.admin_order_field = 'crawl_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Is new?'