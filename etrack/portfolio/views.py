from django.shortcuts import render


# Create your views here.

def portfolioView(response):
    return render(response, 'portfolio/portfolioPage.html', {})
