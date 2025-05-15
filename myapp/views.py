from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import connection

# Create your views here.

def scrape(request):
    error_message = None
    if request.method == "POST":
        site = request.POST.get('site', '').strip()
        validator = URLValidator()

        try:
            validator(site)

            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string
                Link.objects.create(address= link_address, name =link_text)
            return HttpResponseRedirect('/')
        except ValidationError:
            error_message = "You need to submit a valid website ex: http://www.google.com"
        
        except Exception:
            error_message = "An error occurred while trying to scrape the site. Try again"
    data = Link.objects.all()

    return render(request, 'myapp/result.html', {'data':data, 'error_message':error_message})

def clear(request):
    Link.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='myapp_link'")
    return render(request, 'myapp/result.html')

