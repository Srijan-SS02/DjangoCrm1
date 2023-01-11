from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm
from .filters import Orderfilter
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import *

# Create your views here.

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    return render(request, 'accounts/register.html', {
        'form': form
    })

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('username')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def userPage(request):
    return render(request, 'accounts/user.html', {

    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/dashboard.html', {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
    })


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {
        "products": products

    })


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = Orderfilter(request.GET, queryset=orders)
    orders = myFilter.qs

    return render(request, 'accounts/customer.html', {
        "customer": customer,
        "orders": orders,
        "order_count": order_count,
        'myFilter': myFilter

    })


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, 'accounts/order_forms.html', {
        'formset': formset
    })


@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_forms.html', {
        'form': form
    })


@login_required(login_url='login')
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', {
        'item': order,
    })
