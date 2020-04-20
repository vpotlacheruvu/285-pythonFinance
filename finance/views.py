from django.views.generic import TemplateView
import requests
from django.shortcuts import render
from finance.forms import Finance
from iexfinance.stocks import Stock
from django.http import HttpResponse
from iexfinance.utils.exceptions import IEXQueryError
import datetime

now = datetime.datetime.now()


# Create your views here.

class FinanceView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        form = Finance()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = Finance(request.POST)
            if form.is_valid():
                stock = form.cleaned_data['symbol']
                try:
                    symbol = Stock(stock, token="sk_811c037d41194d5a813e26af7d465358")
                    name = symbol.get_company_name() + " (" + str(stock) + ")\n\n"
                except IEXQueryError:
                    return HttpResponse('This symbol does not exist or is unavailable. Please go back and try again!')
                curr_date_time = now

        url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&interval=5min&apikey=XHUBBJ82VU4ZCE6J"
        r = requests.get(url.format(stock)).json()

        finance_information = {
            'form': form,
            'symbol': symbol,
            'curr_date_time': curr_date_time,
            'price': r['Global Quote']['05. price'],
            'change': r['Global Quote']['09. change'],
            'change_percentage': r['Global Quote']['10. change percent'],
            'name': name,
        }

        context = {'finance_information': finance_information}
        return render(request, "index.html", context)

