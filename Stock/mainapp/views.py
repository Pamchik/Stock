from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, TemplateView

from .forms import ProductForm, AddQtyForm, WriteOffQtyForm, MoveQtyFromForm, MoveQtyToForm
from .models import *


class StockView(TemplateView):
    model = Product
    template_name = 'stock.html'

    def get_context_data(self, **kwargs):
        quality_list = [p.name for p in AssortmentQualityCategory.objects.all()]
        location_list = [p.name for p in Location.objects.all()]
        quantity_dict = [[p.number, p.location, p.quality, p.quantity] for p in Transaction.objects.all()]
        quantity_list = [(str(i[0]), str(i[1]), str(i[2]), int(i[3])) for i in quantity_dict]
        product_list = [p.number for p in Product.objects.all()]

        context = super().get_context_data(**kwargs)
        context["total_table"] = list_value_product(
            product_list,
            location_list,
            quality_list,
            quantity_list,
        )
        context["category"] = AssortmentCategory.objects.all()
        context["quality"] = AssortmentQualityCategory.objects.all()
        context["product"] = Product.objects.all()
        context["location"] = Location.objects.all()

        search_by = self.request.GET.get('query')
        search_message = "Search..."
        if search_by:
            search_message = search_by
            context["search_message"] = search_message
            context["object_list"] = Product.objects.filter(
                Q(name__icontains=search_by) | Q(number__icontains=search_by) | Q(description__icontains=search_by)
            )
            return context
        context["search_message"] = search_message
        context["object_list"] = Product.objects.all()

        return context


def list_value_product(product_list, location_list, quality_list, quantity_list):
    list_value = []
    i = 0
    for i_product in product_list:
        list_value_lvl1 = []
        for i_location in location_list:
            list_value_lvl2 = []
            for i_quality in quality_list:
                sum_i = 0
                for i_quantity in quantity_list:
                    if i_quantity[0] == i_product and i_quantity[1] == i_location and i_quantity[2] == i_quality:
                        sum_i += int(i_quantity[3])
                list_value_lvl2.append(sum_i)
            list_value_lvl1.append([i_location, list_value_lvl2])
        list_value.append([i_product, list_value_lvl1])
        i += 1
    return list_value


def list_value(location_list, quality_list, quantity_list, **kwargs):
    list_value = []
    for i_location in location_list:
        list_value_lvl2 = []
        for i_quality in quality_list:
            sum_i = 0
            for i_quantity in quantity_list:
                if i_quantity[0] == i_location and i_quantity[1] == i_quality:
                    sum_i += int(i_quantity[2])
            list_value_lvl2.append(sum_i)
        list_value.append([i_location, list_value_lvl2])
    return list_value


def list_value_total(quality_list, quantity_list, **kwargs):
    list_value_total = []
    for i_quality in quality_list:
        sum_total = 0
        for i_quantity in quantity_list:
            if i_quantity[1] == i_quality:
                sum_total += int(i_quantity[2])
        list_value_total.append(sum_total)
    return list_value_total


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

        quality_list = [p.name for p in AssortmentQualityCategory.objects.all()]
        location_list = [p.name for p in Location.objects.all()]
        quantity_dict = [[p.location, p.quality, p.quantity] for p in Transaction.objects.filter(slug=name)]
        quantity_list = [(str(i[0]), str(i[1]), int(i[2])) for i in quantity_dict]

        context['sum_location_quality'] = list_value(location_list, quality_list, quantity_list, **kwargs)
        context['sum_total'] = list_value_total(quality_list, quantity_list, **kwargs)

        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        return f'/{self.object.slug}'


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'
    template_name = 'delete_product.html'
    context_object_name = 'product'


def stock(request):
    quality_list = [p.name for p in AssortmentQualityCategory.objects.all()]
    location_list = [p.name for p in Location.objects.all()]
    quantity_dict = [[p.number, p.location, p.quality, p.quantity] for p in Transaction.objects.all()]
    quantity_list = [(str(i[0]), str(i[1]), str(i[2]), int(i[3])) for i in quantity_dict]
    product_list = [p.number for p in Product.objects.all()]

    context = {
        'total_table': list_value_product(
            product_list,
            location_list,
            quality_list,
            quantity_list,

        ),
        'category': AssortmentCategory.objects.all(),
        'quality': AssortmentQualityCategory.objects.all(),
        'stock': Product.objects.all(),
        'product': Product.objects.all(),
        'location': Location.objects.all(),
    }

    return render(request, 'stock.html', context)


def table(request):
    quality_list = [p.name for p in AssortmentQualityCategory.objects.all()]
    location_list = [p.name for p in Location.objects.all()]
    quantity_dict = [[p.number, p.location, p.quality, p.quantity] for p in Transaction.objects.all()]
    quantity_list = [(str(i[0]), str(i[1]), str(i[2]), int(i[3])) for i in quantity_dict]
    product_list = [p.number for p in Product.objects.all()]

    context = {
        'total_table': list_value_product(
            product_list,
            location_list,
            quality_list,
            quantity_list,

        ),
        'product': Product.objects.all(),
        'quality': AssortmentQualityCategory.objects.all(),
        'location': Location.objects.all(),
        # 'qty_product': QuantityProducts.objects.all()
    }
    return render(request, 'product_table.html', context)


def home(request):
    return render(request, 'home_page.html')


def history(request):
    context = {
        'transaction': Transaction.objects.all(),

    }
    return render(request, 'history.html', context)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'create_product.html'
    form_class = ProductForm
    context_object_name = 'create_product'

    def get_success_url(self):
        return f'/{self.object.slug}/add'



class AddQtyView(CreateView):
    model = Product
    template_name = 'add_qty.html'
    form_class = AddQtyForm
    context_object_name = 'product'

    def get_initial(self):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return {
            'number': number
        }

    def get_context_data(self, **kwargs):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        context = super(AddQtyView, self).get_context_data(**kwargs)
        context['prod'] = Product.objects.filter(number=number)
        return context
    def get_success_url(self):
        return f'/{self.object.number.slug}'


class WriteOffQtyView(CreateView):
    model = Transaction
    template_name = 'write-off_qty.html'
    form_class = WriteOffQtyForm
    context_object_name = 'write-off_qty'

    def get_initial(self):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return {
            'number': number
        }

    def get_context_data(self, **kwargs):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        context = super(WriteOffQtyView, self).get_context_data(**kwargs)
        context['prod'] = Product.objects.filter(number=number)
        return context

    def get_success_url(self):
        return f'/{self.object.number.slug}'


def MoveQtyView(request, slug):
    number = get_object_or_404(Product, slug=slug)
    prod = Product.objects.filter(number=number)

    if request.method == 'POST':
        form1 = MoveQtyFromForm(request.POST, prefix="form1", initial={'number': number})
        form2 = MoveQtyToForm(request.POST, prefix="form2", initial={'number': number})

        if form1.is_valid() and form2.is_valid():
            qty_from = form1.save(commit=False)
            qty_from.save()
            qty_to = form2.save(commit=False)

            qty_to.quantity = request.POST['form1-quantity']
            qty_to.reason = request.POST['form1-reason']

            qty_to.save()
            return redirect(f'/{slug}/')
    else:
        form1 = MoveQtyFromForm(prefix="form1", initial={'number': number})
        form2 = MoveQtyToForm(prefix="form2", initial={'number': number})

    return render(request, 'move_qty.html', {
        'form1': form1, 'form2': form2, 'number': number, 'prod': prod,
    })


def error_404_view(request, exception):
    return render(request, '404.html')