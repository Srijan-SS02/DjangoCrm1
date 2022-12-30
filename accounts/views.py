from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm 

# Create your views here.

def home(request):
	orders= Order.objects.all()
	customers = Customer.objects.all()

	total_customer= customers.count()
	total_orders= orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	return render(request, 'accounts/dashboard.html',{
		"orders" : orders,
		"customers" : customers,
		"total_orders":total_orders,
		"delivered": delivered,
		"pending": pending,
	})

def products(request):
	products = Product.objects.all() 

	return render(request, 'accounts/products.html', {
		"products" : products

	})



def customer(request, pk_test):
	customer=Customer.objects.get(id=pk_test)
	orders= customer.order_set.all()
	order_count=orders.count()

	return render(request, 'accounts/customer.html' ,{
		"customer":customer,
		"orders" : orders, 
		"order_count": order_count,

	})


def createOrder(request):
	
	form = OrderForm
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save() 
			return redirect('/')  


	return render(request, 'accounts/order_forms.html',{
		'form' : form,
	})


def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form= OrderForm(instance=order)    ##############

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)  ###############
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'accounts/order_forms.html', {
		'form':form
	})



def deleteOrder(request, pk):

	# order = Order.objects.get(id=pk)
	# form= OrderForm(instance=order)

	# if request.method == 'POST':
	# 	form = OrderForm(request.POST, instance=order)
	# 	if form.is_valid():
	# 		...
		

		return render(request, 'accounts/delete.html')