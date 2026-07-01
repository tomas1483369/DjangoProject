from django.shortcuts import render


def catalogo(request):
    products = []
    return render(request, 'catalogo.html', {'products': products})
