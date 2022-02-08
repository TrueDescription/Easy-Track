from django.shortcuts import render, redirect
from .models import Portfolio, WatchItem
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def portfolioView(response):
    if response.method == "POST":
        print(response.POST)
        if response.POST.get('currency'):
            print(response.POST.get('name'))
            p = Portfolio(name=response.POST.get('name'), balance=0)
            p.save()
            response.user.portfolio.add(p)
            return redirect('http://127.0.0.1:8000/portfolio/')
        else:
            w = WatchItem(ticker=response.POST.get('name'))
            w.save()
            response.user.WatchItem.add(w)
            return redirect('http://127.0.0.1:8000/portfolio/')


    return render(response, 'portfolio/portfolioPage.html', {})
