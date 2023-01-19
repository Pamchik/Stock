from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ProductForm, AddQtyForm, WriteOffQtyForm, MoveQtyFromForm, MoveQtyToForm
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.db.models import Q, Sum


def index(request):
    return render(request, 'tables.html')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):

        name = self.object.slug
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['quality'] = AssortmentQualityCategory.objects.all()
        context['location'] = Location.objects.all()
        context['transaction'] = Transaction.objects.filter(slug=name).order_by("-id")

        # query = Q(slug=name)
        # #query.add(Q(email='mark@test.com'), Q.OR)
        # query.add(Q(quality=1), Q.AND)
        context['transaction_1_1'] = Transaction.objects.filter(Q(slug=name) & Q(quality=1) & Q(location=1)).aggregate(Sum('quantity'))
        context['transaction_1_2'] = Transaction.objects.filter(Q(slug=name) & Q(quality=2) & Q(location=1)).aggregate(Sum('quantity'))
        context['transaction_1_3'] = Transaction.objects.filter(Q(slug=name) & Q(quality=3) & Q(location=1)).aggregate(Sum('quantity'))
        context['transaction_2_1'] = Transaction.objects.filter(Q(slug=name) & Q(quality=1) & Q(location=2)).aggregate(Sum('quantity'))
        context['transaction_2_2'] = Transaction.objects.filter(Q(slug=name) & Q(quality=2) & Q(location=2)).aggregate(Sum('quantity'))
        context['transaction_2_3'] = Transaction.objects.filter(Q(slug=name) & Q(quality=3) & Q(location=2)).aggregate(Sum('quantity'))
        context['transaction_sum_1'] = Transaction.objects.filter(Q(slug=name) & Q(quality=1)).aggregate(Sum('quantity'))
        context['transaction_sum_2'] = Transaction.objects.filter(Q(slug=name) & Q(quality=2)).aggregate(Sum('quantity'))
        context['transaction_sum_3'] = Transaction.objects.filter(Q(slug=name) & Q(quality=3)).aggregate(Sum('quantity'))

        # print(context['transaction_sum_1'])

        return context

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = ProductForm
    context_object_name = 'product'


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/stock/'
    template_name = 'delete_product.html'
    context_object_name = 'product'


def product_filter(request):
    context = {
        'category': AssortmentCategory.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Product.objects.all()
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'product_detail_.html', context)


def stock(request):
    context = {
        'category': AssortmentCategory.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Product.objects.all()
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'stock.html', context)


def home(request):
    return render(request, 'home_page.html')


def history(request):
    context = {
        'transaction': Transaction.objects.all(),
        'quality_category': AssortmentQualityCategory.objects.all(),
        'stock': Product.objects.all(),
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'history.html', context)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'create_product.html'
    form_class = ProductForm
    context_object_name = 'create_product'

    def get_success_url(self):
        return f'/stock/{self.object.slug}/add'


class AddQtyView(CreateView):
    model = Transaction
    template_name = 'add_qty.html'
    form_class = AddQtyForm
    context_object_name = 'add_qty'

    def get_initial(self):
        name = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return {
            'name': name
        }

    def get_success_url(self):
        return f'/stock/{self.object.name.slug}'


class WriteOffQtyView(CreateView):
    model = Transaction
    template_name = 'write-off_qty.html'
    form_class = WriteOffQtyForm
    context_object_name = 'write-off_qty'

    def get_initial(self):
        name = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return {
            'name': name
        }

    def get_success_url(self):
        return f'/stock/{self.object.name.slug}'


class MoveQtyFromView(CreateView):
    model = Transaction
    template_name = 'move_from_qty.html'
    form_class = MoveQtyFromForm
    context_object_name = 'move_from_qty'

    def get_initial(self):
        name = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return {
            'name': name
        }

    def get_success_url(self):
        return f'/stock/{self.object.name.slug}/move-to/'


class MoveQtyToView(CreateView):
    model = Transaction
    template_name = 'move_to_qty.html'
    form_class = MoveQtyToForm
    context_object_name = 'move_to_qty'

    def get_initial(self):
        name = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return {
            'name': name
        }

    def get_success_url(self):
        return f'/stock/{self.object.name.slug}'


def MoveQtyView(request):
    if request.method == 'POST':
        form1 = MoveQtyFromForm(request.POST, prefix="form1")
        form2 = MoveQtyToForm(request.POST, prefix="form2")


        if form1.is_valid() and form2.is_valid():
            qty_from = form1.save(commit=False)
            qty_from.save()
            qty_to = form2.save(commit=False)

            #name = form2.cleaned_data['name']
            quantity = form2.cleaned_data['quantity']
            reason = form2.cleaned_data['reason']

            #qty_to.name = Product.name(request.POST['form1-name'])
            qty_to.quantity = request.POST['form1-quantity']
            qty_to.reason = request.POST['form1-reason']

            qty_to.save()
            print(request.POST)
            return redirect('stock')
    else:
        form1 = MoveQtyFromForm(prefix="form1")
        form2 = MoveQtyToForm(prefix="form2")

    return render(request, 'move_qty.html', {
        'form1': form1, 'form2': form2,
    })



