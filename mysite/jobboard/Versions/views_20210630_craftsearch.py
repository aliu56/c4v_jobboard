from django.views import generic
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from jobboard.models import Company, Job

### FUNCTIONS
def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    qs = Job.objects.all()
    companies = Company.objects.all()
    name_contains_query = request.GET.get('q')
    company = request.GET.get('company')

    if is_valid_queryparam(name_contains_query):
        qs = qs.filter(job_name__icontains=name_contains_query)

    if is_valid_queryparam(company) and company != 'Company':
        qs = qs.filter(companies__name=company)

    return qs

def IndexView(request):
    qs = filter(request)
    context = {
        'queryset': qs,
        'companies': Company.objects.all()
    }
    return render(request, "jobboard/index.html", context)

### CLASSES
# class IndexView(generic.ListView):
#     model = Job
#     template_name = 'jobboard/index.html'
#     context_object_name = 'job_list'
#
#     def get_queryset(self):
#        result = super(IndexView, self).get_queryset()
#        query = self.request.GET.get('q')
#
#        if query:
#           postresult = Job.objects.filter(
#               Q(job_name__icontains=query) | Q(country__icontains=query)
#        )
#           result = postresult
#        else:
#            """Return the 20 last published jobs."""
#            result = Job.objects.order_by('-crawl_date')[:20]
#        return result

class PortfolioView(generic.ListView):
    template_name = 'jobboard/portfolio.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        """Return the list of companies"""
        return Company.objects.order_by('-company_name')

class CompanyView(generic.DetailView):
    model = Company
    template_name = 'jobboard/company.html'
