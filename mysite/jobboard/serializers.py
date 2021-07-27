from .models import Company, Job
from rest_framework import serializers


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    jobs = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = ['company_name', 'logo', 'stage', 'sector', 'company_website_url', 'scraping_source_url', 'jobs']


class JobSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only = True)

    class Meta:
        model = Job
        fields = ['job_name', 'company_name', 'country', 'city', 'crawl_date', 'offer_url']