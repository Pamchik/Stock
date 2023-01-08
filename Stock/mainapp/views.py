from django.shortcuts import render, redirect
from .models import *
from .forms import StockForm, AddQtyForm
from django.views.generic import DetailView, UpdateView, DeleteView


class ProductDetailView(DetailView):
    model = Stock
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):

        name = self.object.slug
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['quality'] = AssortmentQualityCategory.objects.all()
        context['location'] = Location.objects.all()
        context['transaction'] = Transaction.objects.filter(slug=name)
        return context


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


def product_filter(request):
    context = {
        'category': AssortmentCategory.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Stock.objects.all()
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'product_detail_.html', context)


def stock(request):
    context = {
        'category': AssortmentCategory.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Stock.objects.all()
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'stock.html', context)


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
