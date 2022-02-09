from unicodedata import name
from django.shortcuts import render, redirect
from matplotlib import ticker
from .models import Portfolio, WatchItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

@login_required(login_url='login')
def portfolioView(response):
    total_mv = 0
    for pf in Portfolio.objects.filter(user=response.user):
        total_mv += pf.balance

    total_mv = "{:,.2f}".format(total_mv)
    context = {'total' : total_mv}

    if response.method == "POST":
        if response.POST.get('deletepf'):
            Portfolio.objects.filter(name=response.POST.get('deletepf')).delete()
        if response.POST.get('currency'):
            p = Portfolio(name=response.POST.get('name'), balance=0)
            p.save()
            response.user.portfolio.add(p)
            return redirect('http://127.0.0.1:8000/portfolio/')
        else:
            if response.POST.get('delete'):
                WatchItem.objects.filter(ticker=response.POST.get('deletewi')).delete()
                return redirect('http://127.0.0.1:8000/portfolio/')
            else:
                if WatchItem.objects.filter(user=response.user).filter(ticker=response.POST.get('name').upper()).count() > 0:
                    return redirect('http://127.0.0.1:8000/portfolio/')
                
                n = response.POST.get('name').upper()
                w = WatchItem(ticker=n)
                w.save()
                response.user.WatchItem.add(w)
                return redirect('http://127.0.0.1:8000/portfolio/')
    
    return render(response, 'portfolio/portfolioPage.html', context)
