from __future__ import unicode_literals
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product
# start of mpesa related imports

from django_daraja.mpesa import utils
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime
# end of mpesa related imports


# start of mpesa instances and variables
cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = ""
# end of mpesa instances and variables


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "account created successfully")
            return redirect('register')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')



@login_required
def add_product(request):
    if request.method == "POST":
        p_name = request.POST.get("jina")
        p_quantity = request.POST.get("kiasi")
        p_price = request.POST.get("bei")
        product = Product(prod_name=p_name, prod_quantity=p_quantity, prod_price=p_price)
        product.save()
        messages.success(request, 'saved successfully')
        return redirect('add-product')
    return render(request, 'add-product.html')

@login_required


def view_products(request):

    products = Product.objects.all()

    return render(request, "products.html", {'products': products})

@login_required


def delete_product(request, id):
    product =Product.objects.get(id=id)
    product.delete()
    messages.success(request, "product deleted successfully")
    return redirect('products')


@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        updated_name = request.POST.get('jina')
        updated_quantity = request.POST.get('kiasi')
        updated_price = request.POST.get('bei')

        product.prod_name = updated_name
        product.prod_quantity = updated_quantity
        product.prod_price = updated_price
        # return the updated data to the database

        product.save()

        messages.success(request, 'product updated successfully')
        return redirect('products')

    return render(request, "update-product.html",{'product':product})

def auth_success(request):
    token = cl.access_token()
    return JsonResponse(token, safe=False)
@login_required
def payment(request, id):
    products = Product.objects.get(id=id)

    # checking if the form has a post method
    if request.method == 'POST':
        phone_number = request.POST.get('nambari')
        amount = request.POST.get('bei')
        amount = int(amount)
        # proceed with payment by launching sim toolkit
        account_ref = "DONALD0001"
        transaction_description = 'payment for a product'
        call_back_url = stk_push_callback_url
        stk = cl.stk_push(phone_number,amount, account_ref, transaction_description, stk_push_callback_url)

        mpesa_response = stk.response_description
        messages.success(request, mpesa_response)
        return JsonResponse(mpesa_response, safe=False)

    return render(request, 'payment.html', {'product': products})
