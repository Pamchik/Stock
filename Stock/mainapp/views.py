from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ProductForm, AddQtyForm, WriteOffQtyForm, MoveQtyFromForm, MoveQtyToForm, FormatForm
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView, FormView
from django.db.models import Q, Sum
from .admin import TestResource
from django.http import HttpResponse


# def test(request):
#     return render(request, 'test.html')

# def test(request):
#     quality_list = [p.name for p in AssortmentQualityCategory.objects.all()]
#     location_list = [p.name for p in Location.objects.all()]
#     quantity_dict = [[p.name, p.location, p.quality, p.quantity] for p in Transaction.objects.all()]
#     quantity_list = [(str(i[0]), str(i[1]), str(i[2]), int(i[3])) for i in quantity_dict]
#     product_list = [p.name for p in Product.objects.all()]
#     print(list_value_product(
#         product_list,
#         location_list,
#         quality_list,
#         quantity_list
#     ))
#     context = {
#         'total_table': list_value_product(
#             product_list,
#             location_list,
#             quality_list,
#             quantity_list,
#
#         ),
#         'category': AssortmentCategory.objects.all(),
#         'quality': AssortmentQualityCategory.objects.all(),
#         'stock': Product.objects.all(),
#     }
#     return render(request, 'test.html', context)


def list_value_product(product_list, location_list, quality_list, quantity_list):
    list_value = []
    i = 0
    for i_product in product_list:
        list_value_lvl1 = []
        for i_location in location_list:
            list_value_lvl2 = []
            for i_quality in quality_list:
                sum = 0
                for i_quantity in quantity_list:
                    if i_quantity[0] == i_product and i_quantity[1] == i_location and i_quantity[2] == i_quality:
                        sum += int(i_quantity[3])
                list_value_lvl2.append(sum)
            list_value_lvl1.append([i_location, list_value_lvl2])
        list_value.append([i_product, list_value_lvl1])
        i += 1

    return list_value

def list_value(location_list, quality_list, quantity_list, **kwargs):
    list_value = []
    for i_location in location_list:
        list_value_lvl2 = []
        for i_quality in quality_list:
            sum = 0
            for i_quantity in quantity_list:
                if i_quantity[0] == i_location and i_quantity[1] == i_quality:
                    sum += int(i_quantity[2])
            list_value_lvl2.append(sum)
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
        # #query.add(Q(email='mark@test.com'), Q.OR)
        # query.add(Q(quality=1), Q.AND)
        # context['transaction_1_1'] = Transaction.objects.filter(Q(slug=name) & Q(quality=1) & Q(location=1)).aggregate(Sum('quantity'))

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


# def product_filter(request):
#     context = {
#         'category': AssortmentCategory.objects.all(),
#         'quality_category': AssortmentQualityCategory.objects.all(),
#         'stock': Product.objects.all()
#         # 'qty_product': QuantityProducts.objects.all()
#     }
#     return render(request, 'product_detail_.html', context)


def stock(request):
    quality_list = [p.name for p in AssortmentQualityCategory.objects.all()]
    location_list = [p.name for p in Location.objects.all()]
    quantity_dict = [[p.name, p.location, p.quality, p.quantity] for p in Transaction.objects.all()]
    quantity_list = [(str(i[0]), str(i[1]), str(i[2]), int(i[3])) for i in quantity_dict]
    product_list = [p.name for p in Product.objects.all()]
    # product_list = [p.number for p in Product.objects.all()]


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
    }

    return render(request, 'stock.html', context)


def home(request):
    return render(request, 'home_page.html')


def history(request):
    context = {
        'transaction': Transaction.objects.all(),
        # 'quality_category': AssortmentQualityCategory.objects.all(),
        # 'stock': Product.objects.all(),
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
    model = Product
    template_name = 'add_qty.html'
    form_class = AddQtyForm
    context_object_name = 'product'

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


def MoveQtyView(request, slug):
    name = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form1 = MoveQtyFromForm(request.POST, prefix="form1", initial={'name': name})
        form2 = MoveQtyToForm(request.POST, prefix="form2", initial={'name': name})

        if form1.is_valid() and form2.is_valid():
            qty_from = form1.save(commit=False)
            qty_from.save()
            qty_to = form2.save(commit=False)

            qty_to.quantity = request.POST['form1-quantity']
            qty_to.reason = request.POST['form1-reason']

            qty_to.save()
            return redirect('stock')
    else:
        form1 = MoveQtyFromForm(prefix="form1", initial={'name': name})
        form2 = MoveQtyToForm(prefix="form2", initial={'name': name})

    return render(request, 'move_qty.html', {
        'form1': form1, 'form2': form2, 'name': name
    })



# def export_data(request):
#
#     if request.method == 'POST':
#         form = FormatForm(request.POST)
#         # Get selected option from form
#         file_format = request.POST['format']
#         test_resource = TestResource()
#         dataset = test_resource.export()
#         if file_format == 'csv':
#             response = HttpResponse(dataset.csv, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
#             return response
#         elif file_format == 'json':
#             response = HttpResponse(dataset.json, content_type='application/json')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
#             return response
#         elif file_format == 'xls':
#             response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
#             return response
#     else:
#         form = FormatForm()
#
#     context = {
#         'transaction': Transaction.objects.all(),
#         'form': form
#     }
#
#     return render(request, 'test.html', context)
