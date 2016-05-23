from datetime import datetime
from decimal import Decimal
from getpass import getpass
import requests


# Only accessible from 137.194.0.0/16
server = 'https://babar.rezel.net/api/'


def get_fullname(customer):
    return customer['firstname'] + ' ' + customer['lastname']

def api(path):
    res = requests.get(server + path + '/')
    assert res.status_code == 200
    return res.json()


# Load DB
customers = api('customer')
statuses = api('status')

# Mine DB
total = 0
for customer in customers:
    real_balance = customer['balance']
    for status in statuses:
        if customer['status']['id'] == status['pk']:
            real_balance += status['overdraft']
            break
    else:
        raise RuntimeError("Status not found")
    if real_balance < 0:
        print(get_fullname(customer), round(real_balance, 2))
        total += real_balance
print("\nthis add up to ", round(total, 2), "€ in loss")
