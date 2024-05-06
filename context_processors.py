# context_processors.py

from flask import request, session

def sidebar():
    sidebar_items = [
        {
            'name': 'Home',
            'link': 'dashboard',
            'page': 'dashboard',
            'icon': 'home',
            'indicator': request.endpoint
        },
        {
            'name': 'Cashbook',
            'link': 'cashbook',
            'page': 'cashbook',
            'icon': 'calculate',
            'indicator': request.endpoint
        },
        {
            'name': 'New Payment',
            'link': 'new_payment',
            'page': 'new_payment',
            'icon': 'payments',
            'indicator': request.endpoint
        },
        {
            'name': 'Payment List',
            'link': 'payment_list',
            'page': 'payment_list',
            'icon': 'receipt',
            'indicator': request.endpoint
        },
        {
            'name': 'Category',
            'link': 'category',
            'page': 'category',
            'icon': 'category',
            'indicator': request.endpoint
        },
        {
            'name':'Income',
            'link':'income',
            'page':'income',
            'icon': 'move_to_inbox',
            'indicator': request.endpoint
        },
        {
            'name':'Accounts',
            'link':'accounts',
            'page':'accounts',
            'icon': 'account_balance',
            'indicator': request.endpoint
        }

        # Add more sidebar items as needed
    ]
    return {'sidebar': sidebar_items}

def username():
    return {'username': session.get('username')}
