from django.shortcuts import render, redirect
from .models import *
from .forms import StockForm, AddQtyForm
from django.views.generic import DetailView, UpdateView, DeleteView


class ProductDetailView(DetailView):
    model = Stock
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    model = Stock
    template_name = 'update_product.html'
    form_class = StockForm
    context_object_name = 'product'


class ProductDeleteView(DeleteView):
    model = Stock
    success_url = '/stock/'
    template_name = 'delete_product.html'
    context_object_name = 'product'


def stock(request):
    context = {
        'category': AssortmentCategory.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Stock.objects.all()
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'stock.html', context)


# def stock_category_filter(request):
#     context = {
#         'category': AssortmentCategory.objects.all(),
#         'quality_category': AssortmentQualityCategory.objects.all(),
#         'stock': Stock.objects.filter(category=2)
#         # 'stock': Stock.objects.all(),
#         # 'qty_product': QuantityProducts.objects.all()
#     }
#     return render(request, 'stock.html', context)


def home(request):
    return render(request, 'home_page.html')


def history(request):
    context = {
        'transaction': Transaction.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Stock.objects.all(),
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'history.html', context)


def create(request):
    error = ''
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock')
        else:
            error = 'Форма неверная'

    form = StockForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'create_product.html', context)


class AddQtyView(DetailView):
    model = Stock
    template_name = 'add_qty.html'
    context_object_name = 'add_qty'

# def add(request):
#     error = ''
#     if request.method == 'POST':
#         form = AddQtyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('stock')
#         else:
#             error = 'Форма неверная'
#
#     form = AddQtyForm()
#     context = {
#         'form': form,
#         'error': error
#     }
#     return render(request, 'add_qty.html', context)
