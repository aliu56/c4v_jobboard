
from django.views import generic
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from jobboard.models import Company, Job


class IndexView(generic.ListView):
    model = Job
    template_name = 'jobboard/index.html'
    context_object_name = 'job_list'

    def get_queryset(self):
       result = super(IndexView, self).get_queryset()
       query = self.request.GET.get('q')

       if query:
          postresult = Job.objects.filter(
              Q(job_name__icontains=query) | Q(country__icontains=query)
       )
          result = postresult
       else:
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

# class SearchView(generic.ListView):
#     model = Job
#     template_name = 'jobboard/search.html'
#     context_object_name = 'all_search_results'
#
#     def get_queryset(self):
#        result = super(SearchView, self).get_queryset()
#        query = self.request.GET.get('q')
#
#        if query:
#           postresult = Job.objects.filter(
#               Q(job_name__icontains=query) | Q(country__icontains=query)
#        )
#           result = postresult
#        else:
#            result = None
#        return result