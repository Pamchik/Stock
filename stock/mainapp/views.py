# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import *
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, TemplateView

from .forms import ProductForm, AddQtyForm, WriteOffQtyForm, MoveQtyFromForm, MoveQtyToForm, AuthenticationCustomForm, \
    PasswordChangeCustomForm
from .models import *
from django.utils.translation import gettext_lazy as _


class StockView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
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
        search_message = "Найти..."
        if search_by:
            search_message = search_by
            context["search_message"] = search_message
            context["object_list"] = Product.objects.filter(
                Q(name__iregex=search_by) | Q(number__iregex=search_by) | Q(description__iregex=search_by)
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Product
    template_name = 'update_product.html'
    form_class = ProductForm
    context_object_name = 'product'

    def get_success_url(self):
        return f'/{self.object.slug}'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Product
    success_url = '/'
    template_name = 'delete_product.html'
    context_object_name = 'product'


@login_required(login_url='/login/')
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



@login_required(login_url='/login/')
def history(request):
    context = {
        'transaction': Transaction.objects.all(),

    }
    return render(request, 'history.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Product
    template_name = 'create_product.html'
    form_class = ProductForm
    context_object_name = 'create_product'

    def get_success_url(self):
        return f'/{self.object.slug}/add'


class AddQtyView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Product
    template_name = 'add_qty.html'
    form_class = AddQtyForm
    context_object_name = 'product'

    def get_initial(self):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        author = self.request.user.id
        return {
            'author': author,
            'number': number,
        }

    def get_context_data(self, **kwargs):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        context = super(AddQtyView, self).get_context_data(**kwargs)
        context['prod'] = Product.objects.filter(number=number)

        return context

    def get_success_url(self):
        return f'/{self.object.number.slug}'


class WriteOffQtyView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Transaction
    template_name = 'write-off_qty.html'
    form_class = WriteOffQtyForm
    context_object_name = 'write-off_qty'

    def get_initial(self):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        author = self.request.user.id
        print(author)
        return {
            'author': author,
            'number': number,
        }

    def get_context_data(self, **kwargs):
        number = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        context = super(WriteOffQtyView, self).get_context_data(**kwargs)
        context['prod'] = Product.objects.filter(number=number)
        return context

    def get_success_url(self):
        return f'/{self.object.number.slug}'

@login_required(login_url='/login/')
def MoveQtyView(request, slug):
    number = get_object_or_404(Product, slug=slug)
    author = request.user.id
    prod = Product.objects.filter(number=number)

    if request.method == 'POST':
        form1 = MoveQtyFromForm(request.POST, prefix="form1", initial={'number': number, 'author': author})
        form2 = MoveQtyToForm(request.POST, prefix="form2", initial={'number': number, 'author': author})

        if form1.is_valid() and form2.is_valid():
            qty_from = form1.save(commit=False)
            qty_from.save()
            qty_to = form2.save(commit=False)

            qty_to.quantity = request.POST['form1-quantity']
            qty_to.reason = request.POST['form1-reason']

            qty_to.save()
            return redirect(f'/{slug}/')
    else:
        form1 = MoveQtyFromForm(prefix="form1", initial={'number': number, 'author': author})
        form2 = MoveQtyToForm(prefix="form2", initial={'number': number, 'author': author})

    return render(request, 'move_qty.html', {
        'form1': form1, 'form2': form2, 'number': number, 'author': author, 'prod': prod,
    })

@login_required(login_url='/login/')
def error_404_view(request, exception):
    return render(request, '404.html')



class LoginCustomView(RedirectURLMixin, FormView):
    """
    Display the login form and handle the login action.
    """

    form_class = AuthenticationCustomForm
    authentication_form = None
    template_name = "login.html"
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context


class PasswordChangeCustomView(PasswordContextMixin, FormView):
    form_class = PasswordChangeCustomForm
    success_url = reverse_lazy("password_change_done")
    template_name = "password_change_form.html"
    title = _("Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneCustomView(PasswordContextMixin, TemplateView):
    template_name = "password_change_done.html"
    title = _("Password change successful")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)