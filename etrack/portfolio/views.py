from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from matplotlib import ticker
from .models import Portfolio, WatchItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import yfinance as yf
from datetime import datetime, time, timedelta


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
    
    for wi in WatchItem.objects.filter(user=response.user):
        obj = WatchItem.objects.get(id=wi.id)
        if obj.curr_price != 0 and not is_time_between(time(9,30), time(16, 0), datetime.now().time()):
            if  obj.last_update < (obj.last_update + timedelta(minutes=5)):
                continue
            if is_time_between(time(9,30), time(16, 0), obj.last_update.time()): # last update was before 4pm
                obj.last_update = datetime.now()
            else:
                continue
        obj.last_update = datetime.now().time()
        obj.curr_price = get_current_price(wi.ticker)
        print("hello")
        if obj.name is None:
            obj.name = yf.Ticker(wi.ticker).info['shortName']
        obj.save()
        
        #print(obj.curr_price)
    return render(response, 'portfolio/portfolioPage.html', context)


def get_current_price(symbol) -> float:
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'][0], 2)

def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time > begin_time and check_time < end_time
    else:
        return check_time > begin_time or check_time < end_time


