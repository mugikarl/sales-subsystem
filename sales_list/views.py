from django.shortcuts import render
from .models import MenuItem, OrderDetail
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

    # Pass both datasets to the template
    context = {
        'all_items': all_items,
        'all_order_items': all_order_items,
    }
    return render(request, 'home.html', context)


def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new item to the database
    context = {'form': form}
    return render(request, 'home.html', context)