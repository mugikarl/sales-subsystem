from django.shortcuts import render, redirect
from .models import MenuItem, OrderDetail, OrderSummary
from .forms import MenuForm, OrderForm
from decimal import Decimal
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

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


#Create New Order Functions

def create_new_order(request):
    # Create a new OrderSummary instance
    new_order_summary = OrderSummary.objects.create(payment_amount=0.00)
    
    # Redirect to the new order page, passing the new order summary ID
    return redirect('neworder', order_id=new_order_summary.id)

def new_order(request, order_id):
    order_summary = OrderSummary.objects.get(id=order_id)
    all_items = MenuItem.objects.all()
    # all_order_items = OrderDetail.objects.filter(order_summary=order_summary)

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
        # elif 'payment_amount' in request.POST:
        #     # Handling payment
        #     payment_amount = request.POST.get('payment_amount')
        #     if payment_amount:
        #         order_summary.payment_amount = float(payment_amount)
        #         order_summary.save()
        #     return redirect('home')  # Redirect to home after placing the order
        # else:
        #     # Update quantities
        #     for key, value in request.POST.items():
        #         if key.startswith('quantity_'):
        #             order_item_id = key.split('_')[1]  # Extract the order item ID
        #             order_item = OrderDetail.objects.get(id=order_item_id)
        #             order_item.quantity = int(value)
        #             order_item.save()

            # Recalculate the total order amount
            # total = sum(item.menu_item.price * item.quantity for item in all_order_items)
            # order_summary.order_total = total
            # order_summary.change = order_summary.payment_amount - total
            # order_summary.save()

    context = {
        'order_summary': order_summary,
        'all_items': all_items,
        'all_order_items': OrderDetail.objects.filter(order_summary=order_summary),
    }
    return render(request, 'neworder.html', context)


def update_quantity(request, id):
    if request.method == 'POST':
        order_item = OrderDetail.objects.get(pk=id)  # Directly fetch the object
        
        adjustment = request.POST.get('adjustment')
        if adjustment == 'increase':
            order_item.quantity += 1
        elif adjustment == 'decrease' and order_item.quantity > 1:
            order_item.quantity -= 1
        
        order_item.save()
    
    return redirect('neworder', order_id=order_item.order_summary.id)


def process_payment(request, order_id):
    # Retrieve the order summary for the given order_id
    order_summary = OrderSummary.objects.get(id=order_id)
    
    # Retrieve the order details (items in the order)
    all_order_items = OrderDetail.objects.filter(order_summary=order_summary)

    if request.method == 'POST':
        # Get the payment amount from the POST data
        payment_amount = Decimal(request.POST.get('payment_amount', 0.0))

        # Update the payment amount in the order summary
        order_summary.payment_amount = payment_amount
        order_summary.save()

        # Calculate change dynamically
        change = payment_amount - order_summary.order_total

        # Get all the menu items to display
        all_items = MenuItem.objects.all()

        # Pass the change, order summary, all menu items, and order items to the template
        return render(request, 'neworder.html', {
            'order_summary': order_summary,
            'change': change,
            'all_items': all_items,  # Pass all menu items to the template
            'all_order_items': all_order_items  # Pass the current order items to the template
        })

    # If it's a GET request, render the page normally with the order details and menu items
    all_items = MenuItem.objects.all()
    return render(request, 'neworder.html', {
        'order_summary': order_summary,
        'all_items': all_items,  # Display all menu items on GET request
        'all_order_items': all_order_items  # Display current order items
    })
    
    
def deleteOrderItem(request, id):
    order_item = OrderDetail.objects.get(pk=id)
    order_summary = order_item.order_summary
    order_item.delete()
    return redirect('neworder', order_id=order_summary.id)


def deleteOrderSummary(request, id):
    order_summary = OrderSummary.objects.get(pk=id)
    order_summary.delete()
    return redirect('home')

#Menu Item Functions
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

#Print Pdf

def generate_invoice(order_summary, order_items):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 50, f"Invoice for Order {order_summary.id}")

    # Order Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Order ID: {order_summary.id}")
    c.drawString(50, height - 120, f"Date: {order_summary.date}")
    c.drawString(50, height - 140, f"Total Amount: PHP{order_summary.order_total}")
    c.drawString(50, height - 160, f"Payment: PHP{order_summary.payment_amount}")
    c.drawString(50, height - 180, f"Change: PHP{order_summary.change}")

    # Table for Order Items
    table_data = [["Item Name", "Quantity", "Price", "Total"]]
    for item in order_items:
        table_data.append([
            item.menu_item.name,
            item.quantity,
            f"PHP{item.menu_item.price}",
            f"PHP{item.total_price}"
        ])

    table = Table(table_data, colWidths=[150, 70, 100, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Render Table
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    # Footer
    c.drawString(50, 50, "Thank you for buying in BawkBawk! Come again!")
    c.save()

    buffer.seek(0)
    return buffer

def report_preview(request, order_id):
    order_summary = OrderSummary.objects.get(id=order_id)
    order_items = OrderDetail.objects.filter(order_summary=order_summary)

    # Generate the PDF
    buffer = generate_invoice(order_summary, order_items)

    # Return the PDF as an HTTP response
    return HttpResponse(buffer, content_type='application/pdf')


def report_download(request, order_id):
    order_summary = OrderSummary.objects.get(id=order_id)
    order_items = OrderDetail.objects.filter(order_summary=order_summary)

    # Generate the PDF
    buffer = generate_invoice(order_summary, order_items)

    # Return the PDF as a downloadable file
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order_summary.id}.pdf"'
    return response
    