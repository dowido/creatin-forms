from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product


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


@login_required
def payment(request, id):
    products = Product.objects.get(id=id)

    # checking if the form has a post method
    if request.method == 'POST':
        phone_number = request.POST.get('nambari')
        amount = request.POST.get('bei')
        # proceed with payment by launching sim toolkit

    return render(request, 'payment.html', {'product': products})
