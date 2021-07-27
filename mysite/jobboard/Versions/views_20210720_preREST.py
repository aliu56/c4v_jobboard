
from django.views import generic
from jobboard.models import Company, Job


class IndexView(generic.ListView):
    model = Job
    template_name = 'jobboard/index.html'
    context_object_name = 'job_list'

    def get_queryset(self):
         """Return the 20 last published jobs."""
         result = Job.objects.order_by('-crawl_date')[:20]
         return result

class PortfolioView(generic.ListView):
    template_name = 'jobboard/portfolio.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        """Return the list of companies"""
        return Company.objects.order_by('-company_name')


class CompanyView(generic.DetailView):
    model = Company
    template_name = 'jobboard/company.html'