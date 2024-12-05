from django.shortcuts import render, redirect
from .models import MenuItem, OrderDetail, OrderSummary
from .forms import MenuForm, OrderForm

def home(request):
    if request.method == 'POST':
        # Handle MenuItem form submission
        form = MenuForm(request.POST or None)
        if form.is_valid():
            form.save()
    
    # Fetch all MenuItem and OrderDetail records
    all_items = MenuItem.objects.all()
    all_order_items = OrderDetail.objects.all()
    all_ordersum_items = OrderSummary.objects.all()

    print(all_ordersum_items)

    # Pass both datasets to the template
    context = {
        'all_items': all_items,
        'all_order_items': all_order_items,
        'all_ordersum_items': all_ordersum_items,
    }
    return render(request, 'home.html', context)


def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new item to the database
    context = {'form': form}
    return render(request, 'home.html', context)

def new_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()  # Saves the new item to the database

    all_items = MenuItem.objects.all()
    all_order_items = OrderDetail.objects.all()
    all_ordersum_items = OrderSummary.objects.all()
    context = {
        'all_items': all_items,
        'all_order_items': all_order_items,
        'all_ordersum_items': all_ordersum_items,
    }
    return render(request, 'neworder.html', context)

def create_new_order(request):
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        if orderform.is_valid():
            orderform.save()
    context = {'orderform':orderform}
    return render(request, 'neworder.html', context) 
