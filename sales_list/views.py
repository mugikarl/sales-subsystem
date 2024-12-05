from django.shortcuts import render, redirect
from .models import MenuItem, OrderDetail, OrderSummary
from .forms import MenuForm, OrderForm

def home(request):
    order_summary = OrderSummary.objects.all()
    all_items = MenuItem.objects.all()
    all_order_items = OrderDetail.objects.all()

    if request.method == 'POST':
        # Handle MenuItem form submission
        form = MenuForm(request.POST or None)
        if form.is_valid():
            form.save()

    print(order_summary)

    # Pass both datasets to the template
    context = {
        'order_summary': order_summary,
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

def create_new_order(request):
    # Create a new OrderSummary instance
    new_order_summary = OrderSummary.objects.create(payment_amount=0.00)
    
    # Redirect to the new order page, passing the new order summary ID
    return redirect('neworder', order_id=new_order_summary.id)

def new_order(request, order_id):
    order_summary = OrderSummary.objects.get(id=order_id)
    all_items = MenuItem.objects.all()
    all_order_items = OrderDetail.objects.filter(order_summary=order_summary)

    if request.method == 'POST':
        if 'menu_item' in request.POST:
            # Adding menu items to the order
            menu_item_id = request.POST.get('menu_item')
            menu_item = MenuItem.objects.get(id=menu_item_id)
            order_detail, created = OrderDetail.objects.get_or_create(
                menu_item=menu_item,
                order_summary=order_summary,
                defaults={'quantity': 1}
            )
            if not created:
                order_detail.quantity += 1
                order_detail.save()
        elif 'payment_amount' in request.POST:
            # Handling payment
            payment_amount = request.POST.get('payment_amount')
            if payment_amount:
                order_summary.payment_amount = float(payment_amount)
                order_summary.save()
            return redirect('home')  # Redirect to home after placing the order
        else:
            # Update quantities
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    order_item_id = key.split('_')[1]  # Extract the order item ID
                    order_item = OrderDetail.objects.get(id=order_item_id)
                    order_item.quantity = int(value)
                    order_item.save()

            # Recalculate the total order amount
            total = sum(item.menu_item.price * item.quantity for item in all_order_items)
            order_summary.order_total = total
            order_summary.change = order_summary.payment_amount - total
            order_summary.save()

    context = {
        'order_summary': order_summary,
        'all_items': all_items,
        'all_order_items': OrderDetail.objects.filter(order_summary=order_summary),
    }
    return render(request, 'neworder.html', context)


def deleteOrderItem(request, id):
    order_item = OrderDetail.objects.get(pk=id)
    order_summary = order_item.order_summary
    order_item.delete()
    return redirect('neworder', order_id=order_summary.id)


def deleteOrderSummary(request, id):
    order_summary = OrderSummary.objects.get(pk=id)
    order_summary.delete()
    return redirect('home')

def menu_list(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
    
    # Fetch all MenuItem records
    all_items = MenuItem.objects.all()
    
    context = {
        'all_items': all_items,
    }
    return render(request, 'menulist.html', context)

def deleteMenuItem(request, id):
    item = MenuItem.objects.get(pk=id)
    item.delete()  # Delete the item
    return redirect('menu_list')

def editMenuItem(request, id):
    item = MenuItem.objects.get(pk=id)  # Fetch the item to be edited
    all_items = MenuItem.objects.all()  # Fetch all items for the list

    if request.method == 'POST':
        item_id = request.POST.get('item_id')  # Get item ID if editing
        if item_id:  # Update existing item
            item = MenuItem.objects.get(pk=id)
            form = MenuForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('menu_list')
                
    context = {
        'item_to_edit': item,
        'all_items': all_items,
    }
    return render(request, 'menulist.html', context)