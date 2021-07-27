
from django.views import generic

from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CompanySerializer, JobSerializer
from .models import Company, Job

from dateutil.relativedelta import relativedelta
from django.utils import timezone

# class IndexView(generic.ListView):
#     model = Job
#     template_name = 'jobboard/index.html'
#     context_object_name = 'job_list'
#
#     def get_queryset(self):
#          """Return the 20 last published jobs."""
#          result = Job.objects.order_by('-crawl_date')[:20]
#          return result
#
# class PortfolioView(generic.ListView):
#     template_name = 'jobboard/portfolio.html'
#     context_object_name = 'company_list'
#
#     def get_queryset(self):
#         """Return the list of companies"""
#         return Company.objects.order_by('-company_name')
#
#
# class CompanyView(generic.DetailView):
#     model = Company
#     template_name = 'jobboard/company.html'



class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all().order_by('company_name')
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

# A job crawled on 21/07/2021 will be off on 22/10/2021
some_day_last_3_months = timezone.now().date() - relativedelta(months=3)

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Job.objects.all().filter(crawl_date__gte=some_day_last_3_months).order_by('company__company_name')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]