from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"
    
@login_required
def myview(request):
    print(request)
    return HttpResponse("You're looking at question %s." % request)

