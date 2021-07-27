from django.contrib import admin
from django.http import HttpResponse
from .models import Company, Job
import csv

# Lining
class JobInline(admin.TabularInline):
    model = Job
    extra = 1

class CompanyInLine(admin.TabularInline):
    model = Company
    extra = 1

# Registering the models
# class PortfolioAdmin(admin.ModelAdmin):
# 	fields = ['portfolio_name']
# 	inlines = [CompanyInline]
#
# 	list_display = ('portfolio_name','vc_website_url')
# 	search_fields = ['portfolio_name']


### ADMIN ACTIONS

def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response


export_as_csv.short_description = "Export selected"

### MODEL ADMIN
class CompanyAdmin(admin.ModelAdmin):
    fields = ['company_name', 'logo', 'stage', 'sector', 'company_website_url', 'scraping_source_url']
    inlines = [JobInline]

    list_display = ('company_name', 'logo', 'stage', 'sector', 'company_website_url', 'scraping_source_url')
    list_filter = ['company_name', 'stage', 'sector']
    search_fields = ['company_name', 'stage', 'sector', 'company_website_url', 'scraping_source_url']

    actions = [export_as_csv]

class JobAdmin(admin.ModelAdmin):
    fields = ['job_name', 'company', 'country', 'city', 'offer_url','crawl_date']

    list_display = ('job_name', 'company', 'country', 'city', 'offer_url', 'crawl_date', 'was_published_recently')
    list_filter = ['company', 'country', 'city', 'crawl_date']
    search_fields = ['job_name', 'company', 'country', 'city', 'crawl_date']

    actions = [export_as_csv]

#admin.site.register(Portfolio)#, PortfolioAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
