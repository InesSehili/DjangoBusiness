
from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from .models import Item


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"


class ItemDetailView(DeleteView):
    model = Item
    template_name = "product-page.html"


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context)


def products(request):
    context = {}
    return render(request, "product-page.html", context)


def checkout(request):
    context = {}
    return render(request, "checkout-page.html", context)
