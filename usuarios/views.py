from django.shortcuts import render


def dashboard(request):
    context = {
        'total_users': 0,
        'total_products': 0,
        'low_stock_products': 0,
        'out_of_stock_products': 0,
        'recent_users': [],
        'recent_products': [],
    }
    return render(request, 'dashboard.html', context)
