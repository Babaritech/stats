from datetime import datetime
from decimal import Decimal
from getpass import getpass
import requests


server = 'https://babar.rezel.net/api/'
user = getpass("API username: ")
password = getpass("API password: ")


def get_fullname(customer):
    return customer['firstname'] + ' (' + customer['nickname'] + ') ' + customer['lastname']

def api(path):
    return requests.get(server + path + '/', auth=(user, password)).json()


# Load DB
customers = api('customer')
payments = api('payment')
purchases = api('purchase')
years = list(range(2012, datetime.now().year+4))
print('DB loaded.')


# Biggest customer per class
customers_by_year = {str(year):list(filter(lambda c: c['year'] == year, customers)) for year in years}
res = []
for y in sorted(customers_by_year):
    big = None
    for c in customers_by_year[y]:
        cp = list(filter(lambda p: p['customer'] == c['pk'], payments))
        c['total'] = round(sum([float(p['amount']) for p in cp]), 2)
        big = c if big is None or c['total'] > big['total'] else big
    res.append((y, big))

with open('./html/customers.txt', 'w') as f:
    for (y, b) in res:
        if b is not None:
            msg = "The biggest customer of class " + y + " is " + get_fullname(b) + " with " + str(b['total']) + "€ spended."
            print(msg)
            print(msg, file=f)
